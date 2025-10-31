from flask import Flask, request, send_file, jsonify
import requests
import io
import re
import base64
import sys
import os

app = Flask(__name__)

# ---- CONFIG ----
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "YOUR_SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "YOUR_SPOTIFY_CLIENT_SECRET")

# ---- HELPER FUNCTIONS ----
def get_access_token():
    """Fetch an OAuth token from Spotify API."""
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth}"}
    data = {"grant_type": "client_credentials"}

    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def extract_track_id(url):
    """Extract track ID from Spotify URL."""
    match = re.search(r"track/([a-zA-Z0-9]+)", url)
    if not match:
        raise ValueError("Invalid Spotify track URL")
    return match.group(1)

def get_poster_from_spotify(url):
    """Given a Spotify URL, return (track_name, image_bytes)."""
    track_id = extract_track_id(url)
    token = get_access_token()

    headers = {"Authorization": f"Bearer {token}"}
    track_res = requests.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers)
    track_res.raise_for_status()
    track_data = track_res.json()

    # Get the highest resolution album image
    image_url = track_data["album"]["images"][0]["url"]
    image_data = requests.get(image_url)
    image_data.raise_for_status()

    return track_data["name"], image_data.content


# ---- FLASK ROUTE ----
@app.route("/poster", methods=["GET"])
def get_spotify_poster():
    """Web API endpoint: returns the album poster for a given Spotify track URL."""
    track_url = request.args.get("url")
    if not track_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        track_name, image_bytes = get_poster_from_spotify(track_url)
        return send_file(
            io.BytesIO(image_bytes),
            mimetype="image/jpeg",
            as_attachment=True,
            download_name=f"{track_name}_poster.jpg"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---- CLI SUPPORT ----
def run_cli(url):
    """Run from command line: download and save poster locally."""
    try:
        track_name, image_bytes = get_poster_from_spotify(url)
        filename = f"{track_name}_poster.jpg".replace("/", "_")
        with open(filename, "wb") as f:
            f.write(image_bytes)
        print(f"✅ Saved album poster as: {filename}")
    except Exception as e:
        print(f"❌ Error: {e}")


# ---- MAIN ----
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI mode: python app.py <spotify_url>
        run_cli(sys.argv[1])
    else:
        # Web server mode
        app.run(debug=True)
