"""Utilities for keeping scientific source data traceable and reproducible."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


EVIDENCE_CATEGORIES = {
    "measured_or_modeled",
    "documented",
    "testimony",
    "inferred",
    "artistic",
}

REQUIRED_METADATA_FIELDS = {
    "id",
    "event_id",
    "authority",
    "source_url",
    "retrieved_at",
    "sha256",
    "evidence",
    "variable",
    "unit",
    "sample_interval_seconds",
    "location",
    "missing_values",
    "notes",
}


class ResearchDataError(ValueError):
    """Raised when source data or its provenance metadata is invalid."""


@dataclass(frozen=True)
class SeriesSample:
    """One unmodified value from a time series."""

    time_seconds: float
    value: float


def sha256_file(path: str | Path) -> str:
    """Return the SHA-256 digest of a file without loading it all into memory."""

    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(64 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_and_validate_metadata(path: str | Path) -> dict[str, Any]:
    """Load the minimum provenance contract used by the sonification lab."""

    with Path(path).open(encoding="utf-8") as source:
        metadata = json.load(source)

    if not isinstance(metadata, dict):
        raise ResearchDataError("Metadata must be a JSON object.")

    missing = sorted(REQUIRED_METADATA_FIELDS - metadata.keys())
    if missing:
        raise ResearchDataError(f"Missing metadata fields: {', '.join(missing)}")

    parsed_url = urlparse(str(metadata["source_url"]))
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        raise ResearchDataError("source_url must be an absolute HTTPS URL.")

    if metadata["evidence"] not in EVIDENCE_CATEGORIES:
        raise ResearchDataError("Unknown evidence category.")

    if not re.fullmatch(r"[0-9a-f]{64}", str(metadata["sha256"])):
        raise ResearchDataError("sha256 must contain 64 lowercase hexadecimal characters.")

    return metadata


def parse_two_column_series(path: str | Path) -> tuple[SeriesSample, ...]:
    """Parse a time/value text file while rejecting ambiguous data rows.

    Blank lines and lines beginning with ``#`` or ``%`` are ignored. Textual
    headers are accepted only before the first numeric row. Extra columns are
    preserved in the original file but intentionally ignored by this reader.
    """

    samples: list[SeriesSample] = []
    with Path(path).open(encoding="utf-8") as source:
        for line_number, raw_line in enumerate(source, start=1):
            line = raw_line.strip()
            if not line or line.startswith(("#", "%")):
                continue

            fields = line.replace(",", " ").split()
            if len(fields) < 2:
                if not samples:
                    continue
                raise ResearchDataError(f"Line {line_number} has fewer than two columns.")

            try:
                time_seconds = float(fields[0])
                value = float(fields[1])
            except ValueError as exc:
                if not samples:
                    continue
                raise ResearchDataError(f"Line {line_number} is not numeric.") from exc

            if not math.isfinite(time_seconds) or not math.isfinite(value):
                raise ResearchDataError(f"Line {line_number} contains a non-finite value.")
            if samples and time_seconds <= samples[-1].time_seconds:
                raise ResearchDataError(
                    f"Line {line_number} does not have a strictly increasing time."
                )

            samples.append(SeriesSample(time_seconds=time_seconds, value=value))

    if len(samples) < 2:
        raise ResearchDataError("The series must contain at least two numeric samples.")

    return tuple(samples)
