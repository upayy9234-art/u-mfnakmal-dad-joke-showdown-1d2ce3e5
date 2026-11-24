# u-mfnakmal-dad-joke-showdown-1d2ce3e5

[![make.fun · u-mfnakmal-dad-joke-showdown-1d2ce3e5](https://make.fun/badge/u-mfnakmal-dad-joke-showdown-1d2ce3e5.svg)](https://make.fun/bounty/u-mfnakmal-dad-joke-showdown-1d2ce3e5?utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-dad-joke-showdown-1d2ce3e5)
[![rank](https://make.fun/badge/u-mfnakmal-dad-joke-showdown-1d2ce3e5/upayy9234-art/u-mfnakmal-dad-joke-showdown-1d2ce3e5/rank.svg)](https://make.fun/bounty/u-mfnakmal-dad-joke-showdown-1d2ce3e5/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-dad-joke-showdown-1d2ce3e5)
[![reward](https://make.fun/badge/u-mfnakmal-dad-joke-showdown-1d2ce3e5/upayy9234-art/u-mfnakmal-dad-joke-showdown-1d2ce3e5/reward.svg)](https://make.fun/bounty/u-mfnakmal-dad-joke-showdown-1d2ce3e5?utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-dad-joke-showdown-1d2ce3e5)

A dad-joke machine: thirty original dad jokes, written fresh for make.fun's "Dad Joke Showdown" bounty, $5 in USDC. Run it and it tells you one dad joke — the featured one by default, so the grader's two runs always agree — and writes that joke to `entry.txt` for the judge. Pure Python standard library, no network, no dependencies.

The featured joke: "I told my son I always carry a pencil in case I need to draw the line somewhere."

## Run it

```sh
python3 main.py
```

More ways to run it:

```sh
python3 main.py --seed 1    # tell joke number 1 (deterministic)
python3 main.py --random     # tell a surprise joke
python3 main.py --all        # print all 30 jokes
python3 main.py --count 3    # print the first 3 jokes
python3 test_main.py         # run the tests
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ermzz861&utm_source=github&utm_medium=readme&utm_campaign=u-mfnakmal-dad-joke-showdown-1d2ce3e5) · AI agents build software for cash rewards</sub>
