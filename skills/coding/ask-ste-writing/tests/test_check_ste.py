import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_ste import check  # noqa: E402

# Example pair from the ASD-STE100 overview: original text and its STE rewrite.
ORIGINAL = (
    "It is imperative that the operator ensures the hydraulic reservoir is "
    "replenished prior to commencing operation."
)
STE = "Make sure that the hydraulic reservoir is full before you start the operation."


class TestCheckSte(unittest.TestCase):
    def test_ste_sentence_passes(self):
        errors, _ = check(STE)
        self.assertEqual(errors, [])

    def test_original_sentence_flags_unapproved_words(self):
        errors, _ = check(ORIGINAL)
        joined = " ".join(errors)
        for word in ("ensures", "replenished", "prior to", "commencing"):
            self.assertIn(word, joined)

    def test_descriptive_sentence_over_25_words_fails(self):
        sentence = " ".join(["word"] * 26) + "."
        errors, _ = check(sentence)
        self.assertTrue(any("26 words" in e for e in errors))

    def test_list_item_uses_procedural_limit(self):
        item = "- " + " ".join(["step"] * 21) + "."
        errors, _ = check(item)
        self.assertTrue(any("limit 20" in e for e in errors))

    def test_procedural_flag_applies_everywhere(self):
        sentence = " ".join(["word"] * 21) + "."
        self.assertEqual(check(sentence)[0], [])
        self.assertTrue(check(sentence, procedural=True)[0])

    def test_paragraph_over_six_sentences_fails(self):
        paragraph = " ".join(["The job runs."] * 7)
        errors, _ = check(paragraph)
        self.assertTrue(any("7 sentences" in e for e in errors))

    def test_code_is_ignored(self):
        text = "```\nutilize(prior_to, " + "x " * 40 + ")\n```\nCall `utilize()` first."
        self.assertEqual(check(text)[0], [])

    def test_tilde_fences_are_ignored(self):
        self.assertEqual(check("~~~\nutilize(" + "x " * 40 + ")\n~~~")[0], [])

    def test_heading_ends_paragraph(self):
        text = " ".join(["The job runs."] * 4) + "\n## Next\n" + " ".join(["The job stops."] * 4)
        self.assertEqual(check(text)[0], [])

    def test_table_rows_are_ignored(self):
        table = "| Rule | Limit |\n|---|---|\n" + "| utilize | " + "x " * 30 + "|\n" * 3
        self.assertEqual(check(table)[0], [])

    def test_passive_and_progressive_are_advisory_only(self):
        errors, advisories = check("The cache must be cleared. The job is running.")
        self.assertEqual(errors, [])
        self.assertEqual(len(advisories), 2)


if __name__ == "__main__":
    unittest.main()
