import math
from flask import Flask, render_template, request, jsonify
import gpxpy

app = Flask(__name__)

def estrai_track_points(file_stream):
    gpx = gpxpy.parse(file_stream)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(point)
    return points

def genera_link_google_maps(points):
    base_url = "https://www.google.com/maps/dir/"
    MAX_TAPPE = 10
    n_points = len(points)

    if n_points == 0:
        return None

    if n_points <= MAX_TAPPE:
        selected_points = points
    else:
        step = math.ceil(n_points / MAX_TAPPE)
        selected_points = points[::step]

    coords_str = [f"{pt.latitude},{pt.longitude}" for pt in selected_points]
    link = base_url + "/".join(coords_str)
    return link

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Nessun file caricato"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "File senza nome"}), 400

    try:
        points = estrai_track_points(file.stream)
        link = genera_link_google_maps(points)
        if link:
            return jsonify({"link": link})
        else:
            return jsonify({"error": "Nessun track point trovato nel file GPX"}), 400
    except Exception as e:
        return jsonify({"error": f"Errore nel parsing del file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
