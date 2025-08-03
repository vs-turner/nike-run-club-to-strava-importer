
import os
from pathlib import Path
from lxml import etree
import xml.etree.ElementTree as ET
from datetime import timedelta

def fix_tcx_file(input_path, output_path):
    parser = etree.XMLParser(remove_blank_text=True, recover=True)
    tree = etree.parse(str(input_path), parser)
    root = tree.getroot()
    ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}

    # Remove all DistanceMeters tags
    for dist_elem in root.findall('.//tcx:DistanceMeters', ns):
        parent = dist_elem.getparent()
        if parent is not None:
            parent.remove(dist_elem)

    # Filter only <Trackpoint>s with both <Time> and <Position>
    activities = root.findall('.//tcx:Activity', ns)
    if not activities:
        return False
    laps = activities[0].findall('tcx:Lap', ns)
    if not laps:
        return False
    tracks = laps[0].findall('tcx:Track', ns)
    if not tracks:
        return False
    track = tracks[0]

    valid_tps = []
    for tp in track.findall('tcx:Trackpoint', ns):
        if tp.find('tcx:Time', ns) is not None and tp.find('tcx:Position', ns) is not None:
            valid_tps.append(tp)

    for tp in track.findall('tcx:Trackpoint', ns):
        track.remove(tp)
    for vtp in valid_tps:
        track.append(vtp)

    tree.write(str(output_path), pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return True

def parse_tcx_summary(file_path):
    ns = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    tree = ET.parse(file_path)
    root = tree.getroot()
    activities = root.findall('.//tcx:Activity', ns)
    summaries = []

    for activity in activities:
        sport = activity.attrib.get('Sport', 'Unknown')
        id_elem = activity.find('tcx:Id', ns)
        start_time = id_elem.text if id_elem is not None else 'Unknown'
        total_time_sec = 0
        total_distance_m = 0
        for lap in activity.findall('tcx:Lap', ns):
            time_elem = lap.find('tcx:TotalTimeSeconds', ns)
            dist_elem = lap.find('tcx:DistanceMeters', ns)
            if time_elem is not None:
                total_time_sec += float(time_elem.text)
            if dist_elem is not None:
                total_distance_m += float(dist_elem.text)
        duration = timedelta(seconds=total_time_sec)
        distance_km = total_distance_m / 1000
        distance_miles = total_distance_m / 1609.34
        if distance_miles > 0:
            pace_min_per_mile = (total_time_sec / 60) / distance_miles
            pace_str = f"{int(pace_min_per_mile)}:{int((pace_min_per_mile % 1) * 60):02d} min/mi"
        else:
            pace_str = "N/A"
        summaries.append({
            'sport': sport,
            'start_time': start_time,
            'duration': duration,
            'distance_km': distance_km,
            'distance_miles': distance_miles,
            'pace': pace_str
        })
    return summaries

def batch_fix_folder(input_folder, output_folder):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    tcx_files = list(input_folder.glob("*.tcx"))
    print(f"Found {len(tcx_files)} TCX files to process.")
    summary_lines = []

    for file in tcx_files:
        out_path = output_folder / file.name
        try:
            success = fix_tcx_file(file, out_path)
            if success:
                summary = parse_tcx_summary(out_path)
                for i, act in enumerate(summary, 1):
                    block = (
                        f"File: {file.name}\\n"
                        f"  Sport         : {act['sport']}\\n"
                        f"  Start Time    : {act['start_time']}\\n"
                        f"  Duration      : {act['duration']}\\n"
                        f"  Distance (km) : {act['distance_km']:.2f}\\n"
                        f"  Distance (mi) : {act['distance_miles']:.2f}\\n"
                        f"  Pace          : {act['pace']}\\n"
                    )
                    summary_lines.append(block)
                print(f"✔ Fixed: {file.name}")
            else:
                print(f"✖ Skipped (no valid data): {file.name}")
        except Exception as e:
            print(f"✖ Failed: {file.name} | Error: {e}")

    # Save summary
    summary_file = output_folder / "tcx_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("\\n".join(summary_lines))
    print(f"Summary written to: {summary_file}")

if __name__ == "__main__":
    input_path = input("Enter the path to your original .tcx files: ").strip()
    output_path = os.path.join(input_path, "strava_ready")
    batch_fix_folder(input_path, output_path)



