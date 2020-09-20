import os
from flask import Flask, request, jsonify, send_file

from src.file_service import FileService
from src.scrapers import VSScraper, GlasswallScraper
from src.config import Config


def validation_error(msg):
    return jsonify({"error": msg}), 400


def create_app():

    app = Flask(__name__, static_url_path="/src/static")
    app.config.from_object(Config)

    @app.route("/health")
    def health():
        return jsonify({"message": "ok"})

    @app.route("/process-zip", methods=["POST"])
    def process_zip():
        output = {}
        file = request.files.get("file", None)
        if not file:
            return jsonify({"message": "no file supplied"})
        FileService.process_zip(file)
        return jsonify(output)

    @app.route("/fetch-files", methods=["POST"])
    def fetch_files():
        output = {}
        data = request.json
        if data["site"] == "glasswall":
            GlasswallScraper.scrape()

        elif data["site"] == "virusshare":
            vs_api_key = os.environ.get("vs_api_key", None)
            if vs_api_key:
                vs = VSScraper(vs_api_key)
                vs.scrape()
            else:
                output["message"] = "vs_api_key not supplied"
        return jsonify(output)

    return app
