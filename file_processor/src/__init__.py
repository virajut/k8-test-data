import os
from flask import Flask, request, jsonify, send_file

from src.config import Config


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/process", methods=["POST"])
    def get_files():
        data = request.json
        """
        To do process file 
        """
        msg = data.get("msg", None)
        if not msg:
            return jsonify({"message": "No msg"})

    return app
