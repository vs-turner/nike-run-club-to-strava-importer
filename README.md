# Nike Run Club → Strava TCX Fixer

This tool batch-processes `.tcx` files exported from the Nike Run Club app and fixes common formatting issues so they can be uploaded cleanly to Strava.

---

## Why This Exists

Nike’s `.tcx` exports often include broken or malformed data:

- Missing GPS (`<Position>`) or timestamp (`<Time>`) in `<Trackpoint>` entries
- Corrupted or inaccurate `<DistanceMeters>` fields
- Inconsistent sampling (e.g. multiple entries per second)
- Poor formatting or XML noise

These issues can cause Strava to display:

- Distances in the tens of thousands of miles
- Incorrect durations or pace
- Missing or broken route maps

---

## What the Script Does

The script:

- Removes all `<DistanceMeters>` tags to let Strava recalculate distance from GPS
- Keeps only valid `<Trackpoint>` entries with both timestamp and position
- Writes clean, well-formed `.tcx` files that work reliably in Strava
- Generates a `tcx_summary.txt` with distance, duration, and pace for each run

---

## Output

After running, you’ll get:

- Cleaned `.tcx` files saved to a `strava_ready/` folder
- A `tcx_summary.txt` file with basic info for each activity

Example summary entry:

```
File: run1.tcx
  Start Time    : 2023-11-07T03:56:18Z
  Duration      : 0:45:12
  Distance (mi) : 3.21
  Pace          : 14:04 min/mi
```

---

## How to Use

1. Clone this repo or download the script.
2. Run from the command line:

   ```bash
   python strava_batch_fix_tcx_with_summary.py
   ```

3. When prompted, enter the folder containing your `.tcx` files (e.g., from a Nike data export).
4. The cleaned files will appear in a `strava_ready/` folder in the same directory.

---

## Getting Your Nike Run Club Data

To retrieve your actual runs:

1. Visit the [Nike Privacy Portal](https://privacy.nike.com)
2. Request a data export under **“Access Your Data”**
3. Select **Nike Run Club** when prompted
4. You need to confirm via email that you want the download, then you'll receive a download link via email (usually a ZIP with `.tcx` files)

Note: The download link typically expires in 7 days, so save your data locally.


