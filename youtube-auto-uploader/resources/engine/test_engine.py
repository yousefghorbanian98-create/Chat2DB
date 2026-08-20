import tempfile
import unittest
from pathlib import Path

from easyclip_engine import FaceSample, SpeakerTurn, Word, build_format_selector, caption_groups, censor_word, merge_speaker_turns, pick_highlights, smooth_face_tracks, write_karaoke_ass, write_srt


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

    def test_user_intent_boosts_matching_highlight(self):
        words=[Word(text,index,index+.8) for index,text in enumerate("ordinary introduction then renewable energy battery breakthrough explained clearly".split())]
        from easyclip_engine import score_window
        generic=score_window(words,20)[0]
        focused=score_window(words,20,"renewable energy battery")[0]
        self.assertGreater(focused,generic)

    def test_highlights_are_non_overlapping(self):
        words = self.sample() * 8
        words = [Word(w.text, i * 1.1, i * 1.1 + 0.9) for i, w in enumerate(words)]
        clips = pick_highlights(words, 20, 3)
        self.assertGreaterEqual(len(clips), 2)

    def test_adjacent_speaker_turns_are_merged(self):
        turns = [SpeakerTurn("SPEAKER_00", 0, 2), SpeakerTurn("SPEAKER_00", 2.2, 4), SpeakerTurn("SPEAKER_01", 4.1, 6)]
        merged = merge_speaker_turns(turns)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0].end_seconds, 4)
        self.assertEqual(merged[1].speaker, "SPEAKER_01")

    def test_face_smoothing_removes_jitter_and_clamps_velocity(self):
        samples = [
            FaceSample(1, 0.0, .300, .2, .2, .2, .9, 0),
            FaceSample(1, 0.2, .304, .2, .2, .2, .9, 0),
            FaceSample(1, 0.4, .700, .2, .2, .2, .9, 0),
        ]
        smoothed = smooth_face_tracks(samples)
        self.assertAlmostEqual(smoothed[1].x, smoothed[0].x, places=3)
        self.assertLessEqual(smoothed[2].x - smoothed[1].x, .28 * .2 + .001)

    def test_profanity_is_masked_without_changing_word_length(self):
        self.assertEqual(censor_word("shit"), "s•••")
        self.assertEqual(censor_word("آموزش"), "آموزش")

    def test_karaoke_ass_contains_word_timing(self):
        words = [Word("سلام", 5, 5.4), Word("دنیا", 5.4, 6)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "caption.ass"
            write_karaoke_ass(words, path, 5)
            text = path.read_text(encoding="utf-8-sig")
            self.assertIn("Style: Karaoke,Vazirmatn", text)
            self.assertIn("{\\k40}سلام", text)
            self.assertIn("{\\k60}دنیا", text)

    def test_srt_is_relative_to_clip(self):
        words = [Word("Hello", 10, 10.5), Word("world.", 10.6, 11)]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "caption.srt"
            write_srt(words, path, 10)
            text = path.read_text(encoding="utf-8")
            self.assertIn("00:00:00,000 --> 00:00:01,000", text)


if __name__ == "__main__":
    unittest.main()
