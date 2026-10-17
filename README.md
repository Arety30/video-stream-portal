# Video Stream Portal

Video Stream Portal is a small FastAPI application by Syed Abrar Ali that serves a single-page video player meant to be published behind a reverse proxy or tunnel. It solves a simple sharing problem: instead of passing around raw Google Drive or YouTube links, one URL on the owner's own host shows a themed player where a Drive file ID, a Drive share URL or a YouTube URL can be pasted and embedded, and the page displays its own public address so it can be copied and shared.

## Where it is used

Abrar runs it as a private "stream gateway" page on a local machine and exposes the `/video` route through a tunnel so friends or other devices can open one link and watch a shared video. It is a presentation layer only; the media itself is still hosted by Google Drive or YouTube and plays inside their embedded players.

## How it works

- `main.py` creates a FastAPI app with two routes, `GET /video` and `GET /video/`, both of which read `templates/index.html` from disk on each request and return it as HTML (404 with a short error page if the template is missing). `uvicorn` is started on `127.0.0.1:8080` with auto-reload when the file is run directly.
- `templates/index.html` is self-contained: CSS in a `<style>` block, three colour themes (`default`, `cyberpunk`, `matrix`) switched by adding a class to `<body>`, icons from the Lucide CDN, and vanilla JavaScript:
  - `updatePlayer(source, title)` turns the input into an embeddable URL: a bare Drive file ID becomes `https://drive.google.com/FILE<id>/preview`; a Drive URL containing `/view` is rewritten to `/preview`; `youtube.com/watch?v=` and `youtu.be/` links become `https://www.youtube.com/embed/<id>`; anything else is used as-is. The result is assigned to the `<iframe id="videoPlayer">`.
  - `loadCustomVideo()` classifies the text box (Drive URL, YouTube URL, long ID without slashes, other) and calls `updatePlayer`.
  - `loadPreset(id, name, el)` fills the box from one of the preset buttons.
  - On load the page writes `window.location.origin + pathname` into the "share this URL" box; `copyTunnelUrl()` copies it to the clipboard.

| File | Role |
|------|------|
| `main.py` | FastAPI app, serves the template at `/video` |
| `templates/index.html` | Player UI, theme switcher, URL normalisation, share box |

There is no database, no upload handling and no server-side state.

## Setup

Requirements: Python 3.9+, `fastapi`, `uvicorn`. Internet access is needed in the browser for the Lucide icon script, Google Fonts and the embedded players.

```bash
git clone <repo-url> ~/video_app
cd ~/video_app
python3 -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn
```

Configuration is done by editing `templates/index.html`:

- the default `<iframe src>` and the first preset button carry a Drive file identifier; replace them with your own file ID (for example `1AbCdEfGhIjKlMnOpQrStUvWxYz`);
- the second preset points at a public sample video and can be removed or changed;
- host/port are set at the bottom of `main.py` (`127.0.0.1:8080`).

## Usage

```bash
python3 main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8080
```

Open `http://localhost:8080/video`. Paste one of:

- a Drive file ID such as `1AbCdEfGhIjKlMnOpQrStUvWxYz`
- a Drive link such as `https://drive.google.com/FILE
- a YouTube link such as `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

and press Load. To publish it, put the app behind any HTTPS reverse proxy or tunnel pointing at port 8080 (the page shows whatever origin it is served from as the share URL).

## Project structure

```
video_app/
├── main.py
└── templates/
    └── index.html
```

## Limitations and notes

- No authentication: anyone with the URL can open the page. Access control has to come from the proxy/tunnel in front of it.
- Only embeds third-party players; Drive files must be shared with "anyone with the link" for the preview iframe to work.
- The theme buttons rely on the global `event` object inside `setTheme()`, which works in current browsers but is deprecated.
- The root path `/` returns 404; only `/video` and `/video/` are routed.
- `reload=True` in `main.py` is a development setting; use the `uvicorn` command without it for a long-running deployment.
