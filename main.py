"""
Main Entry Point for Text Steganography Project
-----------------------------------------------
Run without arguments to launch the Graphical User Interface (GUI):
    python main.py

Run with '--cli' flag to run the interactive Command-Line Interface:
    python main.py --cli
"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Text Steganography using Least Significant Bit (LSB) Data Hiding."
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in interactive Command-Line Interface (terminal) mode."
    )
    args = parser.parse_args()

    if args.cli:
        import cli
        cli.main_menu()
    else:
        try:
            import gui
            gui.main()
        except Exception as e:
            print(f"[NOTE] GUI could not be initialized ({e}). Falling back to CLI mode.\n")
            import cli
            cli.main_menu()


if __name__ == "__main__":
    main()
