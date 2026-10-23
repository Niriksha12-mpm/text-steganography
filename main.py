"""
Main Entry Point for Text Steganography Studio
-----------------------------------------------
Run without arguments to launch the Modern Desktop GUI:
    python main.py

Run with '--web' flag to launch the Browser-Based Web Dashboard:
    python main.py --web

Run with '--cli' flag to run the interactive Command-Line Interface:
    python main.py --cli
"""

import sys
import os
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description="Text Steganography Studio — Robust LSB Image Data Hiding with Error Correction."
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch the Modern Web Application in your web browser (Streamlit)."
    )
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in interactive Command-Line Interface (terminal) mode."
    )
    args = parser.parse_args()

    if args.web:
        web_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_web.py")
        print("\n[INFO] Launching Modern Web Interface via Streamlit...")
        print(f"Command: streamlit run \"{web_script}\"\n")
        try:
            subprocess.run(["streamlit", "run", web_script])
        except Exception as e:
            print(f"[ERROR] Could not start Streamlit: {e}")
            print("Make sure streamlit is installed (`pip install streamlit`).")
    elif args.cli:
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
