"""Embedding-based side-by-side comparison of markdown papers."""

__version__ = "0.1.0"

# Bumped whenever parsing/normalization/chunking changes in a way that
# invalidates cached vectors. Part of the cache fingerprint.
PARSER_VERSION = 3
NORMALIZER_VERSION = 2
