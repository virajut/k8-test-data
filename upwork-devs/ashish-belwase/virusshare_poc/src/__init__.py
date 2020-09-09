import os
from flask import Flask, request, jsonify, send_file

from src.file_processor import FileProcessor
from src.scrapers import VSScraper


def validation_error(msg):
    return jsonify({"error": msg}), 400


def create_app():

    app = Flask(__name__, static_url_path="/src/static")

    @app.route("/health")
    def health():
        return jsonify({"message": "ok"})

    @app.route("/scrape-vs-file", methods=["POST"])
    def scrape_vs_file():
        data = request.json
        if "api_key" not in data or "hash" not in data:
            return validation_error("api_key and hash required")

        vs = VSScraper(os.environ.get("vs_api_key", ""))
        f = vs.scrape_file(data["hash"])
        return jsonify({"file_name": f})

    @app.route("/scrape-vs", methods=["POST"])
    def scrape_vs():
        vs = VSScraper(os.environ.get("vs_api_key", ""))
        vs.scrape_hashes()
        return jsonify({})

    @app.route("/check-malicious", methods=["POST"])
    def check_malicious():
        file = request.files.get("file")
        if not file:
            return validation_error("file required")
        file_info = FileProcessor.process(file)
        return jsonify(file_info)

    @app.route("/fetch-vs-files", methods=["POST"])
    def fetch_vs_files():
        vs = VSScraper(os.environ.get("vs_api_key", ""))
        hashes = vs.get_demo_hashes()
        output = FileProcessor.process_vs_hash(hashes)
        return jsonify(output)

    @app.route("/files", methods=["POST"])
    def get_files():
        data = request.json
        file_type = data.get("file_type", None)
        if not file_type:
            return jsonify({"message": "file_type not supplied"})
        num_files = data.get("num_files", 1)
        output_file = FileProcessor.get_files(file_type, num_files)
        if not output_file:
            return jsonify({"message": "no files present"})
        else:
            return send_file(
                output_file, attachment_filename=output_file, as_attachment=True
            )

    return app
