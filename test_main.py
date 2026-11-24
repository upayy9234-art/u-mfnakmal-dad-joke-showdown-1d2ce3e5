#!/usr/bin/env python3
"""Tests for main.py: the dad-joke list and the command line interface.

Pure standard library (unittest + subprocess). Run with:
    python3 test_main.py
"""

import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main as joke_module


class TestJokeList(unittest.TestCase):
    def test_enough_jokes(self):
        self.assertGreaterEqual(len(joke_module.JOKES), 30)

    def test_every_joke_nonempty_single_line(self):
        for joke in joke_module.JOKES:
            self.assertTrue(joke.strip(), "empty joke in list")
            self.assertNotIn("\n", joke, "joke spans more than one line: %r" % joke)
            self.assertNotIn("\r", joke, "joke has a carriage return: %r" % joke)

    def test_every_joke_within_gate(self):
        # The gate accepts 1 to 200 characters of UTF-8 text.
        for joke in joke_module.JOKES:
            self.assertGreaterEqual(len(joke), 1)
            self.assertLessEqual(
                len(joke), joke_module.MAX_JOKE_CHARS,
                "joke over 200 chars (%d): %r" % (len(joke), joke),
            )

    def test_jokes_unique(self):
        self.assertEqual(len(set(joke_module.JOKES)), len(joke_module.JOKES))

    def test_featured_joke_is_a_dad_joke(self):
        featured = joke_module.JOKES[joke_module.FEATURED_INDEX]
        self.assertTrue(featured.strip())
        self.assertLessEqual(len(featured), joke_module.MAX_JOKE_CHARS)

    def test_validate_jokes_passes(self):
        self.assertEqual(joke_module.validate_jokes(), [])

    def test_validate_jokes_catches_a_long_joke(self):
        original = joke_module.JOKES[0]
        try:
            joke_module.JOKES[0] = "x" * 201
            problems = joke_module.validate_jokes()
            self.assertTrue(any("201 chars" in p for p in problems))
        finally:
            joke_module.JOKES[0] = original

    def test_pick_is_deterministic(self):
        self.assertEqual(
            joke_module.pick_joke(), joke_module.JOKES[joke_module.FEATURED_INDEX]
        )
        self.assertEqual(joke_module.pick_joke(seed=1), joke_module.JOKES[1])
        self.assertEqual(joke_module.pick_joke(seed=1), joke_module.pick_joke(seed=1))
        self.assertEqual(
            joke_module.pick_joke(seed=len(joke_module.JOKES)),
            joke_module.JOKES[0],
        )


def run_cli(*args, env=None):
    full_env = dict(os.environ)
    full_env.pop("MAKEFUN_OUTPUT_DIR", None)
    if env:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, "main.py", *args],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True, text=True, env=full_env, timeout=30,
    )


class TestCli(unittest.TestCase):
    def test_default_run_prints_featured_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli(env={"MAKEFUN_OUTPUT_DIR": tmp})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                result.stdout.strip(),
                joke_module.JOKES[joke_module.FEATURED_INDEX],
            )
            with open(os.path.join(tmp, "entry.txt"), encoding="utf-8") as handle:
                self.assertEqual(
                    handle.read(),
                    joke_module.JOKES[joke_module.FEATURED_INDEX],
                )

    def test_default_run_is_deterministic(self):
        first = run_cli()
        second = run_cli()
        self.assertEqual(first.returncode, 0)
        self.assertEqual(second.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)

    def test_seed_is_deterministic(self):
        first = run_cli("--seed", "1")
        second = run_cli("--seed", "1")
        self.assertEqual(first.returncode, 0)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(first.stdout.strip(), joke_module.JOKES[1])

    def test_all_prints_every_joke(self):
        result = run_cli("--all")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.strip().split("\n")
        self.assertEqual(len(lines), len(joke_module.JOKES))
        self.assertEqual(lines, joke_module.JOKES)

    def test_count_prints_n_jokes(self):
        result = run_cli("--count", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.strip().split("\n")
        self.assertEqual(lines, joke_module.JOKES[:3])

    def test_never_raises_on_bad_count(self):
        result = run_cli("--count", "-5")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
