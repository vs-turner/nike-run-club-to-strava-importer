# Nike2StravaFix
## Nike Run Club → Strava TCX Importer

This tool batch-processes `.tcx` files exported from the Nike Run Club app and fixes common formatting issues so they can be uploaded cleanly to Strava.

---

## Why This Exists

Nike’s `.tcx` exports often include broken or malformed data:

- Missing GPS (`<Position>`) or timestamp (`<Time>`) in `<Trackpoint>` entries
- Corrupted or inaccurate `<DistanceMeters>` fields
- Inconsistent sampling (e.g. multiple entries per second)
- Poor formatting or XML noise

These formatting and corruption issues can cause Strava to display:

- Distances in the tens of thousands of miles
- Incorrect durations or pace
- Broken route maps

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

## Requesting Nike Run Club Data

To retrieve your run data:

1. Visit the [Nike Privacy Help Form](https://www.nike.com/help/privacy)
2. Request a data export under **“Export My Personal Data”** under GDPR guidelines 
3. You need to confirm via email that you want the download, then you'll receive a download link via email (usually a ZIP with `.tcx` files)

Note: The download link typically expires in 7 days, so save your data locally.

(HT @ https://www.reddit.com/r/Strava/comments/1c9xkly/transferring_nike_run_club_history_to_strava/)