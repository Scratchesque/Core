# Rabbit Rush - main.py
#
# Created By: VizzWizz, BoredHF, HJParker2802, KamranBasra, TafaraMangombe, Vladikusss
#
# Source: https://github.com/Scratchesque/Core

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
