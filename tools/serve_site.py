"""Serve the site locally with the same clean URLs used in production.

Run:
    python tools/serve_site.py
    python tools/serve_site.py --directory dist

Extensionless paths are mapped to their generated .html files, and legacy
.html or trailing-slash URLs redirect to the clean version.
"""

from __future__ import annotations

import argparse
import posixpath
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CleanURLHandler(SimpleHTTPRequestHandler):
    directory_path: Path

    def __init__(self, *args, directory: Path, **kwargs):
        self.directory_path = directory.resolve()
        super().__init__(*args, directory=str(self.directory_path), **kwargs)

    def send_head(self):
        parsed = urllib.parse.urlsplit(self.path)
        path = urllib.parse.unquote(parsed.path)

        if path in ("/index", "/index.html"):
            self._redirect("/", parsed.query)
            return None

        if path.endswith(".html"):
            target = path[:-5] or "/"
            self._redirect(target, parsed.query)
            return None

        if len(path) > 1 and path.endswith("/"):
            target = path.rstrip("/")
            self._redirect("/" if target == "/index" else target, parsed.query)
            return None

        return super().send_head()

    def translate_path(self, path: str) -> str:
        parsed = urllib.parse.urlsplit(path)
        clean = posixpath.normpath(urllib.parse.unquote(parsed.path))
        parts = [part for part in clean.split("/") if part and part not in (".", "..")]
        target = self.directory_path.joinpath(*parts)

        if target.is_dir():
            target = target / "index.html"
        elif not target.exists() and target.suffix == "":
            candidate = target.with_name(target.name + ".html")
            if candidate.is_file():
                target = candidate

        return str(target)

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            not_found = self.directory_path / "404.html"
            if not_found.is_file():
                body = not_found.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message=message, explain=explain)

    def _redirect(self, target: str, query: str) -> None:
        location = target + (f"?{query}" if query else "")
        self.send_response(301)
        self.send_header("Location", location)
        self.end_headers()

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--directory",
        default=str(ROOT),
        help="Directory to serve (default: the repository root).",
    )
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    directory = Path(args.directory).resolve()
    if not directory.is_dir():
        raise SystemExit(f"Directory not found: {directory}")

    server = ThreadingHTTPServer(
        ("127.0.0.1", args.port),
        lambda *handler_args, **handler_kwargs: CleanURLHandler(
            *handler_args, directory=directory, **handler_kwargs
        ),
    )
    print(f"Serving {directory} at http://127.0.0.1:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
