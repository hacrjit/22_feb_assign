from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    video_ids = re.findall(r"videoId\":\"([^\"]+)\"", response.text)
    video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids[:5]]
    thumbnail_urls = re.findall(r"\"thumbnail\":{\"thumbnails\":\[{\"url\":\"(.*?)\"", response.text)[:5]
    titles = re.findall(r"\"title\":{\"runs\":\[{\"text\":\"(.*?)\"}", response.text)[:5]
    view_counts = re.findall(r"\"viewCountText\":{\"simpleText\":\"(.*?)\"", response.text)[:5]
    times = re.findall(r"\"publishedTimeText\":{\"simpleText\":\"(.*?)\"", response.text)[:5]

    with open("youtube_videos.csv", "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Video URL", "Thumbnail URL", "Title", "View Count", "Time of Posting"])
        for video_url, thumbnail_url, title, view_count, time in zip(video_urls, thumbnail_urls, titles, view_counts, times):
            csv_writer.writerow([video_url, thumbnail_url, title, view_count, time])

    return "Data saved to youtube_videos.csv"

if __name__ == "__main__":
    app.run(debug=True)
