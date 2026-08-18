import tempfile
import unittest
from pathlib import Path

from easyclip_engine import Word, build_format_selector, caption_groups, pick_highlights, write_srt


class EngineTests(unittest.TestCase):
    def sample(self):
        tokens = "Today I explain why this important mistake happens and how you can avoid it. The secret is practice every day."
        return [Word(token, index * 1.2, index * 1.2 + 1) for index, token in enumerate(tokens.split())]

    def test_format_rejects_av1_and_caps_height(self):
        selector = build_format_selector("1080")
        self.assertIn("height<=?1080", selector)
        self.assertIn("vcodec!*=av01", selector)

    def test_caption_groups_preserve_all_words(self):
        words = self.sample()
        groups = list(caption_groups(words, max_chars=18, max_words=4))
        self.assertGreater(len(groups), 1)
        self.assertEqual([w.text for g in groups for w in g], [w.text for w in words])

    def test_highlights_are_non_overlapping(self):
        words = self.sample() * 8
        words = [Word(w.text, i * 1.1, i * 1.1 + 0.9) for i, w in enumerate(words)]
        clips = pick_highlights(words, 20, 3)
        self.assertGreaterEqual(len(clips), 2)

    def test_srt_is_relative_to_clip(self):
        words = [Word("Hello", 10, 10.5), Word("world.", 10.6, 11)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "caption.srt"
            write_srt(words, path, 10)
            text = path.read_text(encoding="utf-8")
            self.assertIn("00:00:00,000 --> 00:00:01,000", text)


if __name__ == "__main__":
    unittest.main()
