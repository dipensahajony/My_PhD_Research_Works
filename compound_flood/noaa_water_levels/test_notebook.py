"""Offline regression tests for the notebook; no NOAA requests are made."""
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

notebook = json.loads(Path(__file__).with_name("download_noaa_water_levels.ipynb").read_text(encoding="utf-8"))
namespace = {}
exec("".join(notebook["cells"][1]["source"]), namespace)
date_ranges = namespace["date_ranges"]
download = namespace["download_water_levels"]
save_csv = namespace["save_csv"]

HEADER = "Date Time, Water Level, Sigma, O or I (for verified), F, R, L, Quality\n"


def response(text):
    result = MagicMock()
    result.text = text
    return result


class DownloadTests(unittest.TestCase):
    def fetch(self, responses, start="20220101", end="20220101"):
        with patch.object(namespace["requests"], "Session") as factory:
            session = factory.return_value.__enter__.return_value
            session.get.side_effect = responses
            result = download("8774230", start, end)
            self.assertEqual(session.get.call_args.kwargs["timeout"], (10, 60))
            return result

    def test_single_day(self):
        self.assertEqual(list(date_ranges("20220101", "20220101")), [("20220101", "20220101")])

    def test_final_single_day_and_leap_year(self):
        self.assertEqual(list(date_ranges("20240201", "20240229")),
                         [("20240201", "20240228"), ("20240229", "20240229")])

    def test_reversed_and_invalid_dates(self):
        for start, end in [("20220102", "20220101"), ("20220230", "20220301")]:
            with self.assertRaises(ValueError):
                list(date_ranges(start, end))

    def test_sorted_deduplicated_and_quality_preserved(self):
        first = "2022-01-01 00:00, 1.2, 0.01, , 0, 0, 0, v\n"
        missing = "2022-01-01 00:06, , 0.01, , 1, 0, 0, p\n"
        columns, rows = self.fetch([response(HEADER + missing + first + first)])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Water Level"], "1.2")
        self.assertEqual(rows[1]["Water Level"], "")
        self.assertEqual(rows[1]["Quality"], "p")
        self.assertIn("F", columns)

    def test_all_chunks_and_last_day(self):
        columns, rows = self.fetch([
            response(HEADER + "2022-01-01 00:00, 1, , , 0, 0, 0, v\n"),
            response(HEADER + "2022-01-29 00:00, 2, , , 0, 0, 0, v\n"),
        ], end="20220129")
        self.assertEqual(len(rows), 2)

    def test_api_error_empty_malformed_and_out_of_range(self):
        for content in ['{"error":{"message":"No data"}}', HEADER,
                        HEADER + "2022-01-01 00:00,1\n",
                        HEADER + "2022-01-02 00:00,1,,,,,,v\n"]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                self.fetch([response(content)])

    def test_conflicting_duplicates(self):
        with self.assertRaises(ValueError):
            self.fetch([response(HEADER + "2022-01-01 00:00,1,,,,,,v\n"
                                 + "2022-01-01 00:00,2,,,,,,v\n")])

    def test_http_and_network_failures(self):
        bad = response("server error")
        bad.raise_for_status.side_effect = namespace["requests"].HTTPError("500")
        for failure in [bad, namespace["requests"].Timeout("timeout")]:
            with self.assertRaises(namespace["requests"].RequestException):
                self.fetch([failure])

    def test_later_chunk_failure_does_not_return_partial_data(self):
        with self.assertRaises(ValueError):
            self.fetch([response(HEADER + "2022-01-01 00:00,1,,,,,,v\n"),
                        response('{"error":{"message":"No data"}}')], end="20220129")

    def test_invalid_station_and_datum(self):
        for station, datum in [("bad", "MSL"), ("8774230", "invalid")]:
            with self.assertRaises(ValueError):
                download(station, "20220101", "20220101", datum)

    def test_save_refuses_empty_or_existing_output(self):
        with self.assertRaises(ValueError):
            save_csv(["Date Time"], [], "unused.csv")
        with patch.object(namespace["Path"], "mkdir"), patch.object(namespace["Path"], "open") as open_file:
            open_file.side_effect = FileExistsError("already exists")
            with self.assertRaises(FileExistsError):
                save_csv(["Date Time"], [{"Date Time": "2022-01-01 00:00"}], "existing.csv")
            self.assertEqual(open_file.call_args.args[0], "x")


if __name__ == "__main__":
    unittest.main()
