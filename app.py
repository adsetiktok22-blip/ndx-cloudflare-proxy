import os
from flask import Flask, request, jsonify
import cloudscraper

app = Flask(__name__)
scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)

@app.route("/")
def health():
    return jsonify({"status": "ok", "msg": "cloudscraper-proxy ready"})

@app.route("/fetch")
def fetch():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "missing url param"}), 400
    try:
        resp = scraper.get(url, timeout=30)
        return jsonify({"status_code": resp.status_code, "html": resp.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
