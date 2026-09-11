from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import os

UPSTREAM = "https://infoooooo-v6v5.vercel.app/accinfo"

API_KEY = os.environ.get("API_KEY", "Raushan")

SIGNATURE = (
    "╔══════════════════════════════╗"
    "                    Raushan Sahni"
    "    Instagram: @raushan_error_01 "
    "    Telegram: @raushan0107 "
    "╚══════════════════════════════╝"
)

ERROR_MESSAGE = "Api error please contact @Developer_Novaji"


class handler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.send_header(
            "Cache-Control",
            "no-store"
        )
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            uid = params.get("uid", [None])[0]
            key = params.get("key", [None])[0]

            if not uid:
                self.send_json({
                    "error": "UID is required"
                }, 400)
                return

            if key != API_KEY:
                self.send_json({
                    "error": "Invalid key"
                }, 401)
                return

            if not uid.isdigit():
                self.send_json({
                    "error": "Invalid UID"
                }, 400)
                return

            url = f"{UPSTREAM}?uid={uid}&region=ind"

            request = Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urlopen(request, timeout=8) as response:
                raw = response.read().decode("utf-8")

            data = json.loads(raw)

            if isinstance(data, dict):
                social = data.get("socialInfo")

                if isinstance(social, dict):
                    social["signature"] = SIGNATURE

            self.send_json(data, 200)

        except (
            HTTPError,
            URLError,
            TimeoutError,
            json.JSONDecodeError
        ):
            self.send_json({
                "error": ERROR_MESSAGE
            }, 502)

        except Exception:
            self.send_json({
                "error": ERROR_MESSAGE
            }, 500)
          
