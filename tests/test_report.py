import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generate_groq_report import dedupe_items, parse_model_json


class ReportTests(unittest.TestCase):
    def test_dedupe_items_normalizes_titles(self):
        items = [
            {"title": "AI  Agents: The Future", "link": "https://a.example/1"},
            {"title": "ai agents the future", "link": "https://b.example/2"},
        ]
        self.assertEqual(len(dedupe_items(items)), 1)

    def test_parse_model_json_keeps_only_valid_article_fields(self):
        raw = '[{"id":"a1","summary":"Short summary.","lessons":["L1"],"crux":"Main point","extra":"drop"}]'
        self.assertEqual(parse_model_json(raw, {"a1"}), [{"id": "a1", "summary": "Short summary.", "lessons": ["L1"], "crux": "Main point"}])

    def test_parse_model_json_handles_markdown_fence(self):
        raw = '```json\n[{"id":"a1","summary":"S","lessons":[],"crux":"C"}]\n```'
        self.assertEqual(parse_model_json(raw, {"a1"})[0]["id"], "a1")


if __name__ == "__main__":
    unittest.main()
