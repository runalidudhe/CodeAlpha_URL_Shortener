
from flask import Flask, render_template, request, redirect, jsonify
from database import (
    initialize_database,
    save_url,
    get_url,
    update_clicks,
    get_all_urls
)
import string
import secrets
from urllib.parse import urlparse

app = Flask(__name__)


# Generate unique short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = ''.join(
            secrets.choice(characters) for _ in range(length)
        )

        if get_url(short_code) is None:
            return short_code


# Validate URL
def validate_url(url):
    try:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ("http", "https"):
            return False

        if not parsed_url.hostname:
            return False

        if "." not in parsed_url.hostname:
            return False

        return True

    except (ValueError, AttributeError):
        return False


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Create short URL
@app.route("/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json(silent=True) or request.form

    original_url = data.get("url", "").strip()

    if not original_url:
        return jsonify({
            "success": False,
            "message": "Please enter a URL."
        }), 400

    if not validate_url(original_url):
        return jsonify({
            "success": False,
            "message": "Please enter a valid HTTP or HTTPS URL."
        }), 400

    try:
        short_code = generate_short_code()

        save_url(short_code, original_url)

        short_url = request.host_url + short_code

        return jsonify({
            "success": True,
            "original_url": original_url,
            "short_url": short_url,
            "short_code": short_code,
            "message": "Short URL created successfully!"
        }), 201

    except Exception:
        app.logger.exception("URL creation failed")

        return jsonify({
            "success": False,
            "message": "Unable to create short URL. Please try again."
        }), 500


# Redirect short URL
@app.route("/<short_code>")
def redirect_url(short_code):

    url_data = get_url(short_code)

    if url_data is None:
        return jsonify({
            "success": False,
            "message": "Short URL not found."
        }), 404

    update_clicks(short_code)

    return redirect(url_data["original_url"], code=302)


# Get URL history
@app.route("/api/urls", methods=["GET"])
def url_history():

    try:
        urls = get_all_urls()

        result = []

        for url in urls:
            result.append({
                "short_code": url["short_code"],
                "original_url": url["original_url"],
                "short_url": request.host_url + url["short_code"],
                "created_at": url["created_at"],
                "clicks": url["clicks"]
            })

        return jsonify({
            "success": True,
            "total": len(result),
            "urls": result
        })

    except Exception:
        app.logger.exception("Unable to retrieve URL history")

        return jsonify({
            "success": False,
            "message": "Unable to retrieve URL history."
        }), 500


# Health check API
@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy",
        "application": "CodeAlpha URL Shortener API"
    })


# Run application
if __name__ == "__main__":

    initialize_database()

    print("===================================")
    print("   CODEALPHA URL SHORTENER")
    print("===================================")
    print("Server: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
