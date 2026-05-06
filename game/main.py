# comment at top of each file
# also format/organize files again cause they all over the place

# names will, albert etc ..
# group thirteen
# https://github/repo link

import argparse

from game.window.env_manager import EnvManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug UI helpers such as the in-level menu button.",
    )
    args = parser.parse_args()

    game = EnvManager(debug=args.debug)
    game.start()


if __name__ == "__main__":
    main()
