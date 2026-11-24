#!/usr/bin/env python3
"""Dad Joke Showdown entry.

Prints one original dad joke and writes it to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt) for the make.fun judge.

Pure Python standard library only: no network, no third-party packages.

The default run is deterministic on purpose: the grader runs this program
twice and compares the two runs byte for byte, so the default run always
tells the featured joke (JOKES[0]). Use --seed N to tell another joke from
the list, --random for a surprise, --all to list every joke, and --count N
to list the first N jokes.
"""

import argparse
import os
import random
import sys

# Every joke below was written fresh for this entry: one line each,
# setup plus punchline, at most 200 characters, no copying from anywhere.
# JOKES[0] is the featured joke: the one the default run tells.
JOKES = [
    "I told my son I always carry a pencil in case I need to draw the line somewhere.",
    "I tried to write a song about a tortilla. It was a wrap.",
    'I asked the ocean why it was so salty. It said, "Because the land never waves back."',
    'I asked the fridge why it was always running. It said, "I\'m just trying to keep my cool."',
    "Why did the coffee go to therapy? It had too many grounds for complaint.",
    'I told my wife she was the cheese to my macaroni. She said, "That\'s the cheesiest thing you\'ve ever said." I said, "I know \u2014 I\'m grate at this."',
    'I asked the waiter if the restaurant had vegetarian options. He said, "We have a salad \u2014 it\'s a romaine calm."',
    'My son asked me why the sun goes down. I said, "Because it has a light curfew."',
    'I told my wife I was going to be a magician. She said, "Great \u2014 now make the dishes disappear."',
    'I told my son the moon was made of cheese. He said, "Dad, that\'s not true." I said, "I know \u2014 it\'s a Gouda story."',
    'I asked the calendar why it was so popular. It said, "I\'ve got a lot of dates."',
    "I tried to be a chef, but I couldn't cut it \u2014 so I became a dad, and now I just wing it at the barbecue.",
    'My son asked me why I never get lost. I said, "Because I always follow my nose \u2014 and it knows the way home."',
    'I told my wife I was going to start a garden. She said, "That\'s a growing concern."',
    'I told my son I was going to teach him to fish. He said, "But Dad, I don\'t want to be baited into another one of your lessons."',
    'I asked the moon why it was so pale. It said, "I only work the night shift \u2014 I never see the sun."',
    'I asked the gardener if he liked his job. He said, "It\'s a lot of work, but I\'m really digging it."',
    'I asked the dog why it was barking at the mailman. It said, "I\'m just delivering my opinion."',
    'My son asked me what clouds are made of. I said, "Mostly water \u2014 but the really good ones are made of cotton candy and dad jokes."',
    'I told my wife I\'d fix the leak in the roof. She said, "You said that last year." I said, "Yes \u2014 and it\'s still leaking. I\'m consistent."',
    'I told my wife I was going to start a band called 1023 Megabytes. She said, "You\'ll never get a gig \u2014 you don\'t have enough bytes."',
    'I told my son I was going to be a detective. He said, "Dad, you can\'t even find your keys." I said, "That\'s why I need the training."',
    'My wife asked me why I talk to the walls. I said, "They\'re great listeners \u2014 they never interrupt."',
    'I asked the sun why it never gets a day off. It said, "I\'m the light of the world \u2014 I can\'t just eclipse my responsibilities."',
    'I told my wife I was going to learn to juggle. She said, "Don\'t drop the ball on this one." I said, "Too late \u2014 I\'m already juggling three kids."',
    'I asked the pilot why he loved his job. He said, "It\'s plane to see \u2014 I get a lift every day."',
    'My son asked me why I wear a belt with suspenders. I said, "I\'m just trying to hold it all together."',
    'I told my wife I was going to write a book about clocks. She said, "That sounds like a waste of time." I said, "No \u2014 it\'s about time."',
    'I asked the baker why his bread was so expensive. He said, "Because I\'m really kneading the dough."',
    'I told my son the tooth fairy left him a note. It said, "Thanks for the teeth \u2014 I\'m building a tiny piano."',
]

FEATURED_INDEX = 0
MAX_JOKE_CHARS = 200


def validate_jokes():
    """Check every joke passes the gate: 1-200 chars, one line, unique.

    Returns a list of problems (empty when everything is fine), so the
    program can refuse to write an entry that the gate would reject.
    """
    problems = []
    seen = set()
    for index, joke in enumerate(JOKES):
        if not joke.strip():
            problems.append("joke %d is empty" % index)
        if "\n" in joke or "\r" in joke:
            problems.append("joke %d spans more than one line" % index)
        if len(joke) > MAX_JOKE_CHARS:
            problems.append(
                "joke %d is %d chars (gate allows at most %d)"
                % (index, len(joke), MAX_JOKE_CHARS)
            )
        if joke in seen:
            problems.append("joke %d is a duplicate" % index)
        seen.add(joke)
    return problems


def pick_joke(seed=None, random_pick=False):
    """Return one joke: the featured one by default, or by seed."""
    if random_pick:
        return random.choice(JOKES)
    if seed is None:
        return JOKES[FEATURED_INDEX]
    return JOKES[seed % len(JOKES)]


def output_dir():
    """Directory the entry text goes to: the grader's /output, or ./entry.txt."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    return "/output"


def write_entry(joke):
    """Write the joke to entry.txt; fall back to ./entry.txt if needed.

    Returns the path written, or None when no directory was writable.
    Never raises: the show must go on even if the file cannot be written.
    """
    for directory in (output_dir(), "."):
        try:
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, "entry.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(joke)
            return path
        except OSError:
            continue
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Tell one original dad joke (and write it to entry.txt)."
    )
    parser.add_argument(
        "--seed", type=int, default=None,
        help="pick joke number N deterministically (wraps around the list)",
    )
    parser.add_argument(
        "--random", action="store_true",
        help="pick a random joke instead of the featured one",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="print every joke, one per line, and do not write entry.txt",
    )
    parser.add_argument(
        "--count", type=int, default=None,
        help="print the first N jokes, one per line, and do not write entry.txt",
    )
    args = parser.parse_args(argv)

    if args.all:
        for joke in JOKES:
            print(joke)
        return 0

    if args.count is not None:
        count = max(0, min(args.count, len(JOKES)))
        for joke in JOKES[:count]:
            print(joke)
        return 0

    joke = pick_joke(seed=args.seed, random_pick=args.random)
    problems = validate_jokes()
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 2
    print(joke)
    write_entry(joke)
    return 0


if __name__ == "__main__":
    sys.exit(main())
