from __future__ import annotations

import numpy as np

from litcompare.embed import ChunkCache, ConceptEmbedder


def test_second_encode_is_a_cache_hit(tmp_path):
    emb = ConceptEmbedder()
    cache = ChunkCache(emb, root=tmp_path)
    texts = ["hello world", "pd hazard default"]

    v1 = cache.encode(texts)
    assert cache.misses == 2
    assert cache.hits == 0

    v2 = cache.encode(texts)
    assert cache.hits == 2
    assert np.array_equal(v1, v2)


def test_editing_source_text_misses_rather_than_reusing_the_old_vector(tmp_path):
    emb = ConceptEmbedder()
    cache = ChunkCache(emb, root=tmp_path)
    cache.encode(["original text"])

    cache2 = ChunkCache(emb, root=tmp_path)
    cache2.encode(["edited text"])
    assert cache2.misses == 1
    assert cache2.hits == 0


def test_fingerprint_and_cache_dir_differ_by_model_id(tmp_path):
    class OtherEmbedder(ConceptEmbedder):
        model_id = "other-model"

    c1 = ChunkCache(ConceptEmbedder(), root=tmp_path)
    c2 = ChunkCache(OtherEmbedder(), root=tmp_path)
    assert c1.fingerprint != c2.fingerprint
    assert c1.root != c2.root


def test_cached_vectors_are_valid_npy_files(tmp_path):
    emb = ConceptEmbedder()
    cache = ChunkCache(emb, root=tmp_path)
    cache.encode(["some text to embed"])

    npy_files = list(tmp_path.rglob("*.npy"))
    assert npy_files, "expected at least one cached vector file on disk"
    for p in npy_files:
        arr = np.load(p)
        assert arr.shape == (emb.dim,)
        assert not np.isnan(arr).any()


def test_disabled_cache_writes_nothing(tmp_path):
    emb = ConceptEmbedder()
    cache = ChunkCache(emb, root=tmp_path, enabled=False)
    cache.encode(["text"])
    assert not any(tmp_path.rglob("*.npy"))
