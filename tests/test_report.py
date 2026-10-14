import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generate_groq_report import dedupe_items, parse_model_json, prompt_for, render_report, summarize_batches


class ReportTests(unittest.TestCase):
    def test_dedupe_items_normalizes_titles(self):
        items = [
            {"title": "AI  Agents: The Future", "link": "https://a.example/1"},
            {"title": "ai agents the future", "link": "https://b.example/2"},
        ]
        self.assertEqual(len(dedupe_items(items)), 1)

    def test_parse_model_json_keeps_only_valid_article_fields(self):
        raw = '[{"id":"a1","summary_paragraphs":["P1","P2","P3","P4"],"lessons":["L1"],"crux":"Main point","extra":"drop"}]'
        self.assertEqual(parse_model_json(raw, {"a1"}), [{"id": "a1", "summary": "P1\n\nP2\n\nP3\n\nP4", "lessons": ["L1"], "crux": "Main point"}])

    def test_parse_model_json_handles_markdown_fence(self):
        raw = '```json\n[{"id":"a1","summary_paragraphs":["P1","P2","P3","P4"],"lessons":[],"crux":"C"}]\n```'
        self.assertEqual(parse_model_json(raw, {"a1"})[0]["id"], "a1")

    def test_prompt_requires_long_summary(self):
        prompt = prompt_for([{"title": "T", "link": "https://example.com/a", "article_text": "Text"}])
        self.assertIn('4 or 5 concise paragraph strings', prompt)

    def test_report_renders_summary_paragraphs_separately(self):
        item = {"title": "T", "source": "example.com", "link": "https://example.com/a", "published": datetime.now(timezone.utc), "summary": "P1\n\nP2", "lessons": ["L"], "crux": "C"}
        report = render_report([item], [], datetime.now(timezone.utc))
        self.assertEqual(report.count('<h3>Summary</h3>'), 1)
        self.assertEqual(report.count('<p>P'), 2)

    def test_empty_batches_are_safe(self):
        self.assertEqual(summarize_batches([], ['unused-key']), ([], []))


if __name__ == "__main__":
    unittest.main()
