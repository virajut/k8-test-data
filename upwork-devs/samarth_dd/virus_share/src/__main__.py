
from flask import Flask, request, jsonify
from scrapers import Scraper

app = Flask(__name__,static_url_path="/src/static")

@app.route("/")
def home():
    return "Glasswall API"

@app.route("/scrape-vs-file")
def scrape_vs_file():
    data = request.json
    vs = Scraper()
    f = vs.scrape_file()
    return jsonify({"file_name": f})

if __name__=="__main__":
    app.run()