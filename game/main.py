import argparse

from game.window.game_manager import GameManager


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug UI helpers such as the in-level menu button.",
    )
    args = parser.parse_args()

    game = GameManager(debug=args.debug)
    game.start()


if __name__ == "__main__":
    main()
