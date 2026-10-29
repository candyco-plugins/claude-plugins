"""Locate the RCA Tracker data folder and master workbook on Windows or Mac.

The data lives in SharePoint at S Drive/Operations/Continuous Improvement/Root Cause Analysis (RCA)/RCA Tracker data,
synced to the computer through a OneDrive "Add shortcut to My files" on the Root Cause Analysis (RCA) folder.
Override with RCA_TRACKER_HOME (the data folder) and RCA_TRACKER_MASTER (the workbook) if it lives elsewhere.
"""
import os
import sys
from pathlib import Path

# Windows consoles default to cp1252; RCA text has em dashes, accents and middle dots.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

FOLDER = "Root Cause Analysis (RCA)"
DATA = "RCA Tracker data"


def _onedrive_roots():
    roots = [Path(os.environ[v]) for v in ("OneDriveCommercial", "OneDrive") if os.environ.get(v)]
    home = Path.home()
    roots += list(home.glob("OneDrive*"))                          # Windows: C:\Users\<name>\OneDrive - Mrs. Call's...
    roots += list(home.glob("Mrs. Call*"))                         # Windows: synced SharePoint libraries
    roots += list((home / "Library" / "CloudStorage").glob("*"))   # Mac
    return [r for r in roots if r.is_dir()]


def find_home():
    if os.environ.get("RCA_TRACKER_HOME"):
        return Path(os.environ["RCA_TRACKER_HOME"]).expanduser()
    for root in _onedrive_roots():
        for pattern in (f"{FOLDER}/{DATA}", f"*/{FOLDER}/{DATA}", f"*/*/{FOLDER}/{DATA}", f"*{FOLDER}*/{DATA}"):
            for cand in root.glob(pattern):
                if cand.is_dir():
                    return cand
    sys.exit(f'RCA Tracker data folder not found. In SharePoint, open Continuous Improvement, find "{FOLDER}", '
             f'choose "Add shortcut to My files", let OneDrive sync, then retry. Or set RCA_TRACKER_HOME.')


HOME = find_home()
MASTER = Path(os.environ["RCA_TRACKER_MASTER"]).expanduser() if os.environ.get("RCA_TRACKER_MASTER") \
    else HOME.parent / "RCA Master Database.xlsx"

if __name__ == "__main__":
    print(f"data:   {HOME}")
    print(f"master: {MASTER} ({'found' if MASTER.exists() else 'NOT FOUND'})")
