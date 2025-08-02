# 🏃‍♀️ Nike Run Club TCX Converter for Strava

This script batch-processes `.tcx` files exported from the **Nike Run Club (NRC)** app and prepares them for clean import into **Strava**. It corrects known formatting issues in Nike’s TCX files that often cause inaccurate distances, durations, or broken GPS data when imported into Strava.

---

## ❗ Problem

Nike's `.tcx` exports can contain structural and data issues such as:

- 🚫 `<Trackpoint>` entries with missing GPS (`<Position>`) or timestamp (`<Time>`) information
- 🧨 Corrupted or malformed `<DistanceMeters>` fields that confuse Strava’s distance calculation
- ⏱ Inconsistent sampling intervals (e.g., multiple samples per second)
- 🧹 Extraneous whitespace or formatting errors

These can result in:

- ❌ Incorrect total distance (e.g., thousands of miles)
- ❌ Incorrect activity duration
- ❌ Missing route data in Strava
- ❌ Invalid pace or elevation plots

---

## ✅ What This Script Does

This tool batch-cleans an entire folder of `.tcx` files and generates Strava-compatible outputs.

### Fixes applied:

- ✅ Removes all `<DistanceMeters>` tags to prevent inflated distance values
- ✅ Keeps only `<Trackpoint>` entries with both `<Time>` and `<Position>`
- ✅ Preserves and reconstructs the GPS path accurately
- ✅ Formats files cleanly for upload to Strava
- ✅ Outputs a plain-text summary of all activities

---

## 📁 Output

- Clean `.tcx` files are saved in a `strava_ready/` subfolder
- A `tcx_summary.txt` file lists summary info for each run: start time, duration, distance, and pace

---

## 🚀 How to Use

1. Download the script
2. Run from the command line:
   ```bash
   python strava_batch_fix_tcx_with_summary.py


## 📥 Getting Your Nike Run Club Data

To use this tool, you’ll need your `.tcx` run files. The best way to get complete and high-quality data is by submitting a **GDPR request** via the [Nike Privacy Portal](https://privacy.nike.com).

- Log in and request access to your data under **"Access Your Data"**
- Choose the **Nike Run Club** product if prompted
- Nike will email you a download link (usually a ZIP archive)
- ⚠️ You typically have **7 days** to download before the link expires

Once downloaded, extract the `.tcx` files and point this script to that folder.
