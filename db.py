import json
import os
import re
from collections import defaultdict

DB_FILE = "chords_db.json"

def generate_db_html():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            chords_db = json.load(f)
    else:
        chords_db = []

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>MUSIC DATABASE</title>
        <script src="./engine/scripts/chart.js"></script>
        <script src="./engine/scripts/jquery.min.js"></script>
        <script src="./engine/scripts/jquery.dataTables.min.js"></script>
        <link rel="stylesheet" href="./engine/scripts/jquery.dataTables.min.css">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { text-align: center; margin-bottom: 40px; }
            #buttons { text-align: center; margin-bottom: 20px; }
            button { padding: 10px 20px; margin: 5px; cursor: pointer; }
            canvas { display: block; margin: 20px auto; }
            table { width: 100%; margin-top: 20px; border-collapse: collapse; }
            table, th, td { border: 1px solid #ddd; }
            th, td { padding: 8px; text-align: center; }
            th { background-color: #f4f4f4; cursor: pointer; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
    <h1>Chords Database</h1>
    <div id="buttons">
        <button onclick="showTable()">Table Database</button>
        <button onclick="showBarChart()">Bar graphs</button>
        <button onclick="showLineChart()">Line graphs</button>
        <button onclick="showPieChart()">Graphic 2</button>
    </div>
    <div id="table-container">
        <table id="chords-table" class="display">
            <thead>
                <tr>
                    <th>Artist</th>
                    <th>Title</th>
                    <th>Chord</th>
                    <th>Times used</th>
                    <th>BPM</th>
                    <th>Keynote</th>
                </tr>
            </thead>
            <tbody>
    """

    chord_counts = defaultdict(int)

    for entry in chords_db:
        artist = entry.get("artist", "Unknown")
        title = entry.get("title", "Unknown")
        bpm = entry.get("bpm", "N/A")
        keynote = entry.get("keynote", "Unknown")

        for chord_change in entry.get("chords", []):
            if isinstance(chord_change, str):
                match = re.search(r"chord='(.+?)', timestamp=(\d+\.\d+)", chord_change)
                if match:
                    chord = match.group(1)
                else:
                    chord = "N/A"
            elif isinstance(chord_change, dict):
                chord = chord_change.get("chord", "N/A")
            else:
                chord = "N/A"

            if chord == "N":
                continue

            chord_counts[(artist, title, chord, bpm, keynote)] += 1

    for (artist, title, chord, bpm, keynote), count in chord_counts.items():
        html_content += f"<tr><td>{artist}</td><td>{title}</td><td>{chord}</td><td>{count}</td><td>{bpm}</td><td>{keynote}</td></tr>"

    html_content += """
            </tbody>
        </table>
    </div>

    <canvas id="chart-canvas" width="400" height="200" style="display:none;"></canvas>

    <script>
        var chart;

        function showTable() {
            document.getElementById("table-container").style.display = "block";
            document.getElementById("chart-canvas").style.display = "none";
        }

        function showBarChart() {
            document.getElementById("table-container").style.display = "none";
            document.getElementById("chart-canvas").style.display = "block";
        }

        function showLineChart() {
            document.getElementById("table-container").style.display = "none";
            document.getElementById("chart-canvas").style.display = "block";
        }

        function showPieChart() {
            document.getElementById("table-container").style.display = "none";
            document.getElementById("chart-canvas").style.display = "block";
        }

        $(document).ready(function() {
            $('#chords-table').DataTable({
                "paging": true,
                "lengthChange": true,
                "searching": true,
                "ordering": true,
                "info": true,
                "autoWidth": false,
                "language": {
                    "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json"
                }
            });
        });
    </script>
    </body>
    </html>
    """

    db_html_file = "chords_database.html"
    with open(db_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\033[92m{db_html_file} has been generated\033[0m")
    return db_html_file
