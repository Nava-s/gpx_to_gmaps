import streamlit as st
import gpxpy
import math

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
        selected_points = [points[0]]
        n_intermedi = MAX_TAPPE - 2
        step = (n_points - 2) / (n_intermedi + 1)
        for i in range(1, n_intermedi + 1):
            idx = round(i * step)
            selected_points.append(points[idx])

        selected_points.append(points[-1])

    coords_str = [f"{pt.latitude},{pt.longitude}" for pt in selected_points]
    link = base_url + "/".join(coords_str)
    return link

# Streamlit UI
st.set_page_config(page_title="GPX to Google Maps", layout="centered")

st.markdown("<h1 style='text-align: center;'>Carica qui il tuo file GPX</h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Scegli un file GPX", type="gpx")

if uploaded_file is not None:
    with st.spinner("Elaborazione del file..."):
        try:
            points = estrai_track_points(uploaded_file)
            link = genera_link_google_maps(points)
            if link:
                st.success("Link generato con successo!")
                st.markdown(f"<a href='{link}' target='_blank'>{link}</a>", unsafe_allow_html=True)
            else:
                st.error("Nessun punto trovato nel file GPX.")
        except Exception as e:
            st.error(f"Errore nel parsing del file GPX: {e}")
