import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.research_data import (
    ResearchDataError,
    load_and_validate_metadata,
    parse_two_column_series,
    sha256_file,
)


class ResearchDataTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.directory = Path(self.temporary_directory.name)

    def test_sha256_file_uses_original_bytes(self):
        source = self.directory / "source.dat"
        source.write_bytes(b"scientific source\n")

        self.assertEqual(
            sha256_file(source),
            hashlib.sha256(b"scientific source\n").hexdigest(),
        )

    def test_metadata_contract_accepts_a_complete_record(self):
        metadata_path = self.directory / "metadata.json"
        metadata = {
            "id": "example-series",
            "event_id": "us20003k7a",
            "authority": "Example authority",
            "source_url": "https://example.org/source.dat",
            "retrieved_at": "2026-10-18T00:00:00Z",
            "sha256": "a" * 64,
            "evidence": "measured_or_modeled",
            "variable": "example",
            "unit": "unknown",
            "sample_interval_seconds": None,
            "location": None,
            "missing_values": None,
            "notes": "Synthetic test metadata, not event data.",
        }
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        self.assertEqual(load_and_validate_metadata(metadata_path), metadata)

    def test_metadata_contract_rejects_an_insecure_source_url(self):
        metadata_path = self.directory / "metadata.json"
        metadata = {field: None for field in {
            "id", "event_id", "authority", "source_url", "retrieved_at", "sha256",
            "evidence", "variable", "unit", "sample_interval_seconds", "location",
            "missing_values", "notes",
        }}
        metadata.update({
            "source_url": "http://example.org/source.dat",
            "sha256": "a" * 64,
            "evidence": "documented",
        })
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        with self.assertRaisesRegex(ResearchDataError, "HTTPS"):
            load_and_validate_metadata(metadata_path)

    def test_parser_accepts_comments_header_and_two_numeric_columns(self):
        source = self.directory / "synthetic-series.txt"
        source.write_text(
            "# Synthetic fixture; it is not earthquake data.\n"
            "time value\n"
            "0.0 0.0\n"
            "0.4 12.5 extra-column\n"
            "0.8,20.0\n",
            encoding="utf-8",
        )

        samples = parse_two_column_series(source)

        self.assertEqual([sample.time_seconds for sample in samples], [0.0, 0.4, 0.8])
        self.assertEqual([sample.value for sample in samples], [0.0, 12.5, 20.0])

    def test_parser_rejects_malformed_rows_after_data_begins(self):
        source = self.directory / "bad-series.txt"
        source.write_text("0.0 1.0\nnot-a-number 2.0\n", encoding="utf-8")

        with self.assertRaisesRegex(ResearchDataError, "Line 2"):
            parse_two_column_series(source)

    def test_parser_rejects_non_increasing_time(self):
        source = self.directory / "bad-time.txt"
        source.write_text("0.0 1.0\n0.0 2.0\n", encoding="utf-8")

        with self.assertRaisesRegex(ResearchDataError, "strictly increasing"):
            parse_two_column_series(source)


if __name__ == "__main__":
    unittest.main()
