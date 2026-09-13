"""`python -m litcompare` -- compare CHAMPION CHALLENGER | batch pairs.yaml | cache info|clear."""

from __future__ import annotations

import argparse
import dataclasses
import json
import shutil
import time
from pathlib import Path

import yaml

from .config import Params
from .embed import CACHE_ROOT, ChunkCache, Embedder, SentenceTransformerEmbedder
from .pipeline import compare as run_pipeline
from .render import render as render_report

_VALID_FIELDS = set(Params.__dataclass_fields__)


def _add_common_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--model", help="sentence-transformers model id")
    p.add_argument("--layout", choices=["html-table", "stacked"])
    p.add_argument("--calibration", choices=["percentile", "absolute"])
    p.add_argument("--top-k", type=int, dest="top_k", help="overrides section and block top-k")
    p.add_argument("--margin", type=float, help="overrides section and block margin")
    p.add_argument("--capacity", type=int, help="overrides section and block b-matching capacity")
    p.add_argument("--excerpt-chars", type=int, dest="excerpt_chars")
    p.add_argument("--include-matrix", action="store_true", default=False)
    p.add_argument("--no-cache", action="store_true", default=False)
    p.add_argument("--config", help="YAML file with a `defaults:` block of Params fields")


def _apply_cli_overrides(p: Params, args: argparse.Namespace) -> Params:
    if getattr(args, "model", None):
        p.model = args.model
    if getattr(args, "layout", None):
        p.layout = args.layout
    if getattr(args, "calibration", None):
        p.calibration = args.calibration
    if getattr(args, "top_k", None) is not None:
        p.section_top_k = args.top_k
        p.block_top_k = args.top_k
    if getattr(args, "margin", None) is not None:
        p.section_margin = args.margin
        p.block_margin = args.margin
    if getattr(args, "capacity", None) is not None:
        p.section_capacity = args.capacity
        p.block_capacity = args.capacity
    if getattr(args, "excerpt_chars", None) is not None:
        p.excerpt_chars = args.excerpt_chars
    if getattr(args, "include_matrix", False):
        p.include_matrix = True
    if getattr(args, "no_cache", False):
        p.cache = False
    return p


def _build_params(args: argparse.Namespace) -> Params:
    p = Params.load(getattr(args, "config", None))
    return _apply_cli_overrides(p, args)


def _stem(path: str) -> str:
    return Path(path).stem


def run_pair(
    champion: str,
    challenger: str,
    params: Params,
    *,
    out_dir: str | Path | None = None,
    base_path: str | Path | None = None,
    embedder: Embedder | None = None,
):
    result, left_doc, right_doc = run_pipeline(champion, challenger, params, embedder=embedder)
    report_text = render_report(result, left_doc, right_doc, params)

    if base_path is not None:
        base = Path(base_path)
        if base.suffix:
            base = base.with_suffix("")
    else:
        out_dir = Path(out_dir or "reports")
        base = out_dir / f"{_stem(champion)}__vs__{_stem(challenger)}"
    base.parent.mkdir(parents=True, exist_ok=True)

    md_path = base.with_suffix(".md")
    json_path = base.with_suffix(".json")
    md_path.write_text(report_text, encoding="utf-8")
    json_path.write_text(json.dumps(result.to_json_dict(), indent=2, default=str), encoding="utf-8")
    return result, md_path, json_path


def cmd_compare(args: argparse.Namespace) -> None:
    params = _build_params(args)
    t0 = time.time()
    result, md_path, json_path = run_pair(args.champion, args.challenger, params, out_dir=args.out)
    dt = time.time() - t0
    print(f"Wrote {md_path} and {json_path} ({dt:.1f}s)")
    print(f"mean_accepted_score={result.metrics['mean_accepted_score']} "
          f"accepted_pairs={result.metrics['accepted_pairs']} "
          f"coverage_left={result.metrics['coverage_left']['overall']} "
          f"coverage_right={result.metrics['coverage_right']['overall']}")
    for w in result.warnings:
        print(f"WARNING: {w}")


def cmd_batch(args: argparse.Namespace) -> None:
    with open(args.manifest, encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh) or {}

    base_params = Params.load(None)
    for k, v in (manifest.get("defaults") or {}).items():
        if k in _VALID_FIELDS:
            setattr(base_params, k, v)
    base_params = _apply_cli_overrides(base_params, args)

    embedders: dict[tuple[str, str | None], Embedder] = {}

    def _embedder_for(p: Params) -> Embedder:
        key = (p.model, p.revision)
        if key not in embedders:
            embedders[key] = SentenceTransformerEmbedder(
                p.model, revision=p.revision, device=p.device, batch_size=p.batch_size, threads=p.threads
            )
        return embedders[key]

    index_rows = []
    for pair in manifest.get("pairs") or []:
        overrides = {k: v for k, v in pair.items() if k in _VALID_FIELDS}
        p = dataclasses.replace(base_params, **overrides)
        champion, challenger = pair["champion"], pair["challenger"]
        out = pair.get("out")
        t0 = time.time()
        result, md_path, json_path = run_pair(
            champion, challenger, p,
            out_dir=args.out, base_path=out, embedder=_embedder_for(p),
        )
        dt = time.time() - t0
        print(f"{champion} vs {challenger}: {md_path} ({dt:.1f}s)")
        index_rows.append(
            {
                "champion": champion, "challenger": challenger, "report": str(md_path),
                "mean_accepted_score": result.metrics["mean_accepted_score"],
                "accepted_pairs": result.metrics["accepted_pairs"],
                "coverage_left": result.metrics["coverage_left"]["overall"],
                "coverage_right": result.metrics["coverage_right"]["overall"],
                "warnings": len(result.warnings),
            }
        )

    out_dir = Path(args.out or "reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Batch comparison index", "",
        "| Champion | Challenger | Report | Mean score | Pairs | Cov L | Cov R | Warnings |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in index_rows:
        lines.append(
            f"| {r['champion']} | {r['challenger']} | [{Path(r['report']).name}]({r['report']}) | "
            f"{r['mean_accepted_score']} | {r['accepted_pairs']} | {r['coverage_left']} | "
            f"{r['coverage_right']} | {r['warnings']} |"
        )
    (out_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_dir / 'index.md'}")


def cmd_cache(args: argparse.Namespace) -> None:
    if args.action == "clear":
        shutil.rmtree(CACHE_ROOT, ignore_errors=True)
        print(f"Cleared {CACHE_ROOT}")
        return
    emb = SentenceTransformerEmbedder(args.model or Params().model)
    cache = ChunkCache(emb, enabled=True)
    print(json.dumps(cache.stats(), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="litcompare", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_compare = sub.add_parser("compare", help="compare one champion/challenger pair")
    p_compare.add_argument("champion")
    p_compare.add_argument("challenger")
    p_compare.add_argument("-o", "--out", default="reports")
    _add_common_flags(p_compare)
    p_compare.set_defaults(func=cmd_compare)

    p_batch = sub.add_parser("batch", help="compare every pair in a pairs.yaml manifest")
    p_batch.add_argument("manifest")
    p_batch.add_argument("-o", "--out", default="reports")
    _add_common_flags(p_batch)
    p_batch.set_defaults(func=cmd_batch)

    p_cache = sub.add_parser("cache", help="inspect or clear the embedding vector cache")
    p_cache.add_argument("action", choices=["info", "clear"])
    p_cache.add_argument("--model")
    p_cache.set_defaults(func=cmd_cache)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
