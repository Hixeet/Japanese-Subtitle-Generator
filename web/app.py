from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return send_from_directory("../video","episode1.mp4")

@app.route("/subtitle")
def subtitle():
    return send_from_directory("../output","subtitle.json")

app.run(port=5000)