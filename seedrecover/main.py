"""Command line interface including input and output."""
import argparse
import sys

from seedrecover.wordlist import Wordlist


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", nargs="*",
                        help="known words of seed phrase", metavar="WORD")
    parser.add_argument("-w", "--wordlist",
                        help="wordlist to use (default: english)",
                        metavar="FILE")
    parser.add_argument("-s", "--similar", type=int, default=0,
                        help="try similar words up to edit distance",
                        metavar="EDIT DISTANCE")
    parser.add_argument("-o", "--order", default=False, action="store_true",
                        help="try different orders of seed words")
    parser.add_argument("-l", "--length", type=int,
                        help="length of seed phrase", metavar="LENGTH")
    parser.add_argument("-m", "--missing", type=int, nargs="+", default=[],
                        help="missing word positions", metavar="POSITION")
    parser.add_argument("-k", "--key", nargs="+", default=[],
                        help="check for stake keys", metavar="STAKE KEY")
    parser.add_argument("-b", "--blockfrost",
                        help="check on blockfrost", metavar="API KEY")
    return parser.parse_args()


def main() -> None:
    """Execute the main control flow of the seedrecover script."""
    args = parse_args()
    wordlist = Wordlist(args.wordlist)
    seed = []
    for word in args.seed:
        if not wordlist.contains(word):
            print(f"'{word}' not in wordlist!", file=sys.stderr)
        words = wordlist.get_words(word, args.similar)
        print(f"{word} => {', '.join(words)}", file=sys.stderr)
        seed.append(words)
