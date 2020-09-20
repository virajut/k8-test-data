import os
from flask import Flask, request, jsonify, send_file

from src.file_service import FileService
from src.config import Config


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/files", methods=["POST"])
    def get_files():
        if request.headers.get("Authorization") != Config.auth_token:
            return jsonify({"message": "Invalid auth_token"})

        data = request.json
        file_type = data.get("file_type", None)
        if not file_type:
            return jsonify({"message": "file_type not supplied"})
        num_files = data.get("num_files", 1)
        output_file = FileService.get_files(file_type, num_files)
        if not output_file:
            return jsonify({"message": "no files present"})
        else:
            return send_file(
                output_file, attachment_filename=output_file, as_attachment=True
            )

    return app
