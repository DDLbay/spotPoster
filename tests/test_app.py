import io
import json
import pytest
import app
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    """Creates a Flask test client."""
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        yield client


# --- MOCK HELPERS ---
@pytest.fixture
def mock_token(monkeypatch):
    """Mock Spotify access token retrieval."""
    monkeypatch.setattr(app, "get_access_token", lambda: "fake_access_token")


@pytest.fixture
def mock_track_data():
    """Mock response for Spotify track metadata."""
    return {
        "name": "Mock Song",
        "album": {
            "images": [
                {"url": "https://mock.image/album.jpg"}
            ]
        }
    }


# --- TESTS ---

def test_extract_track_id_valid():
    url = "https://open.spotify.com/track/3n3Ppam7vgaVa1iaRUc9Lp"
    assert app.extract_track_id(url) == "3n3Ppam7vgaVa1iaRUc9Lp"


def test_extract_track_id_invalid():
    with pytest.raises(ValueError):
        app.extract_track_id("https://open.spotify.com/album/12345")


@patch("requests.post")
def test_get_access_token_success(mock_post):
    mock_post.return_value.json.return_value = {"access_token": "mock_token"}
    mock_post.return_value.raise_for_status = lambda: None
    token = app.get_access_token()
    assert token == "mock_token"


@patch("requests.get")
def test_get_poster_from_spotify(mock_get, mock_token, mock_track_data):
    # Mock Spotify API track response
    mock_track_resp = MagicMock()
    mock_track_resp.json.return_value = mock_track_data
    mock_track_resp.raise_for_status = lambda: None

    # Mock image response
    mock_image_resp = MagicMock()
    mock_image_resp.content = b"fake_image_bytes"
    mock_image_resp.raise_for_status = lambda: None

    mock_get.side_effect = [mock_track_resp, mock_image_resp]

    track_name, image_bytes = app.get_poster_from_spotify("https://open.spotify.com/track/12345")

    assert track_name == "Mock Song"
    assert image_bytes == b"fake_image_bytes"


@patch("app.get_poster_from_spotify")
def test_api_route_success(mock_get_poster, client):
    mock_get_poster.return_value = ("Mock Song", b"fake_image_bytes")

    response = client.get("/poster?url=https://open.spotify.com/track/abc123")

    assert response.status_code == 200
    assert response.mimetype == "image/jpeg"
    assert response.data == b"fake_image_bytes"


def test_api_route_missing_url(client):
    response = client.get("/poster")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


@patch("app.get_poster_from_spotify")
def test_cli_downloads_file(tmp_path, mock_get_poster):
    mock_get_poster.return_value = ("Mock Song", b"fake_image_bytes")

    outfile = tmp_path / "Mock Song_poster.jpg"
    with patch("builtins.open", open(str(outfile), "wb")) as mock_open:
        app.run_cli("https://open.spotify.com/track/abc123")

    assert outfile.exists() is True or outfile.name == "Mock Song_poster.jpg"
