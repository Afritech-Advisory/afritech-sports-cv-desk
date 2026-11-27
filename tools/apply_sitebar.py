"""Kept for habit: stamping the site bar is now part of the language build.
Run from the repo root:  python3 tools/build.py   (this file just runs it)."""
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).resolve().parent / "build.py"), run_name="__main__")
