# Double Number

A small Flask web app with a single page: enter a number, click **Double it**,
and the server doubles it and sends the result back. There's also a button
to join a WhatsApp group.

## How it works

- `app.py` — Flask server. Serves the page at `/` and exposes a
  `POST /api/double` endpoint that takes `{"number": <value>}` and returns
  `{"result": <value * 2>}`.
- `templates/index.html` — the page itself. Client-side JS calls
  `/api/double` via `fetch` and displays the result; no doubling logic runs
  in the browser.
- `index - static example.html` — the original plain HTML/CSS/JS version
  (no server, doubling done entirely client-side), kept for reference.

## Running it

Requires Python 3 with Flask installed (`pip install -r requirements.txt`).

```
python app.py
```

The app starts on `http://127.0.0.1:5000` and is also reachable from other
devices on your local network at `http://<your-machine-ip>:5000`.
