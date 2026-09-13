# Academic Literature Compare

This project compares 2 academic literature papers and generates a report on their similarities and differences. It uses natural language processing techniques to analyze the content of the papers and provides insights into their structure, themes, and key findings.

## Requirements

The concrete task this repo solves: given a **champion** paper and a **challenger**
paper — both converted to markdown — produce a **side-by-side report** showing
what corresponds between them, how closely, what exists on only one side, and
where matched passages disagree on specifics (numbers, terminology, conclusions).
This needs to work for many pairs drawn from a larger corpus (A↔B, C↔D, C↔E, C↔F,
G↔H, …), not just one hand-picked pair, so the same paper (C) may be embedded once
and reused across several comparisons.

### Papers cannot be assumed to share a structure

This is the constraint that shapes everything else in the design. Two papers on
the same topic — even the same *kind* of paper, e.g. two credit-risk model
white papers — are written by different authors, for different audiences, under
different house styles. In this repo's own test fixtures (`lit_md/champion.md`,
`lit_md/challenger.md`), both papers price the same PD × EAD × LGD credit-card
loss model, but:

- `champion.md` uses a conventional academic skeleton: Abstract → numbered
  sections 1–8 with decimal subsections (3.1, 4.2, …) → References → Appendix A/B.
- `challenger.md` uses a deliberately different skeleton: a pull-quote →
  Executive Summary → Part I/II/III with unnumbered descriptive subsection
  headers → a "Box 1" callout → Selected References → Annexes 1–3.

The same concept shows up under completely unrelated headings — champion's
`4.2 Probability of default` is challenger's `Default hazard`; champion's
`4.3 Exposure at default` is challenger's `Exposure simulation`. Heading text,
heading depth, section order, and section count all diverge. Relationships are
frequently many-to-many rather than 1:1 — challenger's single `Part II — The
Framework` section covers everything champion spreads across `§4.1`–`§4.5`, and
champion's five `§7 Limitations` bullets scatter across all three of
challenger's Parts.

**Consequence:** any comparison strategy that keys off headings, heading
numbering, section order, or document position is guaranteed to fail on real
papers, not just as an edge case. It would work on a toy pair the author wrote
to demonstrate the approach and then break the first time it saw a real pair
with a different house style. So this project does not attempt structural or
positional matching at all — no heading-text lookup, no "compare section N of A
to section N of B," no outline-diffing. Alignment is driven entirely by the
*semantic content* of each chunk of text, via vector embeddings, and section/
block correspondence is discovered from the resulting similarity matrix rather
than assumed from the document skeleton.

This has a second-order effect worth calling out explicitly: because matching
is content-driven, it should also be *order-free* (a section can match its
counterpart regardless of where either one sits in its document) and it must
tolerate **many-to-many** relationships (split/merge), not just 1:1 pairs —
forcing 1:1 assignment on real papers actively produces wrong answers (see
"Why not a naive embedding-similarity match" below).

### Why not a naive embedding-similarity match

Embeddings alone are necessary but not sufficient. Two failure modes showed up
immediately when the design was tested against the fixtures instead of assumed
to work:

1. **Forced one-to-one assignment cascades.** Papers routinely contain sections
   with no true counterpart at all (an "Related Work" section on one side, a
   "Governance" section on the other). An optimal 1:1 assignment (e.g. the
   Hungarian algorithm on raw cosine similarity) will still pair those off with
   *something*, because it's forced to — and a single strong false pair (two
   citation-dense "References" sections, matched purely on register rather than
   content) can evict the correct pair elsewhere in the matrix, cascading into
   more wrong matches. The correspondence needs to be many-to-many and needs a
   way to decline a match entirely, not just find the best available partner.
2. **Absolute similarity thresholds don't transfer across model/pair.**
   Sentence embedding models have a similarity floor that varies by model and
   by how similar the two documents are in general (register, domain
   vocabulary), so a fixed cosine cutoff tuned on one pair is wrong on the
   next. On the test fixtures, the highest-scoring pair in the whole matrix was
   a *false* one (two citation lists matching on shared academic register),
   while the correct, hoped-for pair (`4.2 Probability of default` ↔
   `Default hazard`) scored *lower* than that false positive. Absolute cutoffs
   are therefore anti-correlated with correctness here, not just imprecise.
   Thresholds are calibrated per comparison run instead — every run builds a
   null distribution from its own cross-document similarity matrix and expresses
   cutoffs as percentiles/ranks against that distribution (or as a mutual
   top-k + margin gate), so the tool doesn't need re-tuned magic numbers for
   every new pair of papers.

### Other requirements that follow from the above

- **Two independent signals, not one.** A pure embedding channel misses things
  embeddings are structurally bad at — a verbatim-quoted number, a shared
  citation, a repeated named quantity. A lexical (TF-IDF) channel is blended in
  alongside the embedding channel specifically to catch this.
- **Tables and equations are first-class content, not noise to strip.** In the
  fixtures, roughly a quarter of all non-blank lines are table rows, and the
  numeric payload of a table (e.g. the covariate list backing a PD model) is
  often *the* thing that should drive a match — dropping tables measurably
  hurt alignment quality when tested.
- **Numeric facts get their own extraction pass, independent of embeddings.**
  Whether two papers report the *same* LGD (0.851 vs 0.853 vs 0.879) or the
  *same* Gini/AUC/KS is exactly what a validation reviewer wants surfaced, and
  it needs no vector similarity to find — it's a deterministic numeral/unit
  extraction and cross-index, reported as agreements as well as disagreements
  (including a paper's own internal inconsistencies).
- **Bibliographies are handled lexically, not semantically.** Citation-dense
  text has a distinctive register that embeddings latch onto regardless of
  which citations are actually shared, so reference sections are matched and
  compared by normalized `(surname, year)` keys, not by embedding similarity.
- **Local, CPU-only embeddings.** No API keys, no per-run inference cost, and
  no dependency on GPU hardware — the model must run acceptably on a plain
  CPU box.
- **The product is a navigable comparison, not a re-typeset copy of both
  papers.** The output is a markdown report: a header (paths, model, all
  parameters, calibration stats — for reproducibility), a scorecard, an
  alignment map, per-pair side-by-side excerpts with similarity scores and
  source-line references, "only in champion" / "only in challenger" sections,
  and a numeral/citation/terminology cross-index.
- **The corpus-batch use case is first-class, not an afterthought.** Comparing
  many pairs (`C` against `D`, `E`, and `F`) should reuse `C`'s embeddings
  rather than recomputing them — a content-addressed on-disk cache, not a
  vector database (an exhaustive pairwise comparison needs the full similarity
  matrix, which a top-k vector-DB index would only approximate).

## Setup

This project uses uv for environment management. To set up the environment:

```bash
uv sync
```

Dependencies are declared in `pyproject.toml`. To add a package:

```bash
uv add marker-pdf
```

## Approach

1. **PDF → Markdown**, if the source papers aren't already markdown. Marker is
   the conversion step — it preserves headings, tables, code, and equations
   far better than a naive text extraction, which matters because those are
   exactly the structures the comparison pipeline downstream depends on. The
   `marker-pdf` package provides the `marker_single` CLI:

   ```bash
   uv run marker_single input.pdf --output_dir output
   ```

2. **Compare**, via the `litcompare` package (`litcompare/`) — parses each
   markdown file into sections/blocks, embeds them (local
   `sentence-transformers`, cached on disk, content-addressed so a paper reused
   across multiple pairs is only embedded once), blends the embedding
   similarity with a TF-IDF lexical signal, calibrates thresholds per pair, and
   aligns sections/blocks via a gate + capacity-k b-matching step (not a forced
   1:1 assignment — see Requirements above for why). Numeral, citation, and
   table facts are extracted separately and layered on top. The result is
   rendered as a markdown report with an embedded HTML side-by-side table
   (`--layout=html-table`, the default) or a full-markdown-fidelity fallback
   (`--layout=stacked`).

## Usage

Compare a single champion/challenger pair:

```bash
uv run python -m litcompare compare lit_md/champion.md lit_md/challenger.md -o reports/
```

This writes `reports/champion__vs__challenger.md` (the report) and a
`.json` sidecar (the complete structured result, for any future renderer or
downstream tooling).

Compare every pair in a batch manifest (`pairs.yaml`) — this is the
corpus-comparison entry point (A↔B, C↔D, C↔E, C↔F, …), and shares one
in-process embedder plus the on-disk vector cache across all pairs so a
reused paper is only embedded once:

```bash
uv run python -m litcompare batch pairs.yaml -o reports/
```

Inspect or clear the embedding cache:

```bash
uv run python -m litcompare cache info
uv run python -m litcompare cache clear
```

Useful flags on `compare`/`batch`: `--model` (sentence-transformers model id),
`--layout` (`html-table` | `stacked`), `--calibration` (`percentile` |
`absolute`), `--top-k`, `--margin`, `--capacity` (alignment tuning — see
`litcompare/config.py`'s `Params` for the full parameter set and defaults),
`--excerpt-chars`, `--include-matrix`, `--no-cache`, `--config` (a YAML file
of `Params` overrides).

Run the test suite (fully offline — tests use a small deterministic concept
embedder, not the real model):

```bash
uv run pytest -q
```
