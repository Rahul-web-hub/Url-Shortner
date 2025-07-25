import threading
from flask import Flask, request, jsonify, redirect
from app.models import URLMapping
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

# In-memory store for URL mappings
url_store = {}

# Thread lock to prevent race conditions
db_lock = threading.Lock()

@app.route('/')
def health_check():
    """Basic health check to confirm the service is up."""
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    """Detailed API health check."""
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """
    Shortens a given URL and returns the short code + full short URL.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 415

    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL format"}), 400

    with db_lock:
        # Reuse existing short code if URL already exists
        for code, mapping in url_store.items():
            if mapping.original_url == long_url:
                short_code = code
                break
        else:
            short_code = generate_short_code(set(url_store.keys()))
            url_store[short_code] = URLMapping(original_url=long_url)

    short_url = request.host_url + short_code
    return jsonify({"short_code": short_code, "short_url": short_url}), 201

@app.route("/<string:short_code>")
def redirect_to_url(short_code: str):
    """
    Redirects a short code to its original URL.
    """
    with db_lock:
        mapping = url_store.get(short_code)
        if not mapping:
            return jsonify({"error": "Short code not found"}), 404

        mapping.increment_clicks()
        return redirect(mapping.original_url, code=302)

@app.route("/api/stats/<string:short_code>")
def get_stats(short_code: str):
    """
    Returns stats for a short code: click count, original URL, created time.
    """
    with db_lock:
        mapping = url_store.get(short_code)
        if not mapping:
            return jsonify({"error": "Short code not found"}), 404

        return jsonify(mapping.to_dict())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
