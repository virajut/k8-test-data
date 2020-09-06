from flask import Flask, request, jsonify
from file_processor import FileProcessor
from scrapers import VSScraper

app = Flask(__name__, static_url_path="/src/static")

# https://cloud.corvusforensics.com/s/HDcCHLnQTGBnYBN


@app.route("/health")
def health():
    return jsonify({"message": "ok"})


@app.route("/scrape-vs-file", methods=["POST"])
def scrape_vs_file():
    data = request.json
    vs = VSScraper(data["api_key"])
    f = vs.scrape_file(data["hash"])
    return jsonify({"file_name": f})


@app.route("/check-malicious", methods=["POST"])
def check_malicious():
    file = request.files["file"]
    file_info = FileProcessor.process(file)
    return jsonify(file_info)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
