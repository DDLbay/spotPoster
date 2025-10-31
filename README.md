# 🎵 Spotify Song Poster Fetcher

A lightweight **Flask + CLI tool** that fetches the **album poster (cover art)** of any Spotify song — either through a **web API** or directly from your **command line**.

---

## 🚀 Features

- 🎧 Accepts **Spotify track URLs**
- 🖼️ Returns **high-quality album poster**
- 🌐 Works as a **Flask API**
- 💻 Works as a **CLI tool**
- 🔐 Uses **Spotify Web API** for data
- ⚡ No database, just plug and play

---

## 🧰 Requirements

- Python 3.8+
- Spotify Developer Account (for API access)
- Spotify **Client ID** and **Client Secret**

Get credentials from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

---

## 📦 Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/yourusername/spotify-poster-fetcher.git
cd spotify-poster-fetcher
pip install flask requests
````

---

## ⚙️ Environment Setup

You can either edit the file directly to include your Spotify credentials,
or use environment variables for security:

### macOS / Linux:

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

### Windows (PowerShell):

```bash
setx SPOTIFY_CLIENT_ID "your_client_id"
setx SPOTIFY_CLIENT_SECRET "your_client_secret"
```

---

## 🧪 Usage

### ▶️ 1. Run as a Flask Web API

Start the Flask server:

```bash
python app.py
```

Then open your browser or use `curl`:

```
http://127.0.0.1:5000/poster?url=https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp
```

It will return the **poster image file** as a downloadable response.

---

### 💻 2. Run as a CLI Tool

You can directly fetch and save a poster without running the web server:

```bash
python app.py https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp
```

Output:

```
✅ Saved album poster as: Mr. Brightside_poster.jpg
```

---

## 🧠 Example Response (API)

**Request:**

```
GET /poster?url=https://open.spotify.com/track/4VqPOruhp5EdPBeR92t6lQ
```

**Response:**
→ File download: `Viva La Vida_poster.jpg`

---

## 🧩 Project Structure

```
spotify-poster-fetcher/
├── app.py             # Main Flask + CLI script
├── README.md          # Documentation
└── requirements.txt   # Dependencies (optional)
```

---

## 🧱 API Reference

### `GET /poster`

| Parameter | Type   | Required | Description            |
| --------- | ------ | -------- | ---------------------- |
| `url`     | string | ✅ Yes    | Full Spotify track URL |

**Response:**

* Returns the album poster as a downloadable JPEG file
* `Content-Type: image/jpeg`

**Error responses:**

```json
{
  "error": "Invalid Spotify track URL"
}
```

---

## 🧤 Example Integration

You can use this API from your own app, e.g., in Python:

```python
import requests

url = "http://127.0.0.1:5000/poster"
params = {"url": "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"}
r = requests.get(url, params=params)

with open("poster.jpg", "wb") as f:
    f.write(r.content)
```

---

## ⚡ Future Enhancements

* [ ] Add caching for access tokens
* [ ] Add inline (preview) mode
* [ ] Add playlist / album poster support
* [ ] Dockerfile for containerized deployment

---

## 📝 License

This project is open-source and available under the **MIT License**.

---

## 💡 Author

**Abhishek** — Software Developer
GitHub: [@yourusername](https://github.com/yourusername)

---

> *“One line of code closer to the beat.”*

Would you like me to include a **`requirements.txt`** file snippet in the README too (for pip installation section)?
```
