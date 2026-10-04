import os
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API_KEY = os.environ["AIzaSyBu595gPXxjllyRCQoagowpNpg2BsejsL4"]
SEARCH = "Ragnarok WoE"

url = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode({
    "part": "snippet",
    "q": SEARCH,
    "type": "video",
    "order": "date",
    "maxResults": 10,
    "key": API_KEY
})

data = json.load(
    urllib.request.urlopen(url)
)

rss = ET.Element("rss", {"version": "2.0"})
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "Ragnarok WoE Videos"
ET.SubElement(channel, "description").text = "Latest Ragnarok WoE YouTube videos"
ET.SubElement(channel, "link").text = "https://youtube.com"

for video in data["items"]:

    video_id = video["id"]["videoId"]
    snippet = video["snippet"]

    item = ET.SubElement(channel, "item")

    ET.SubElement(item, "title").text = snippet["title"]

    ET.SubElement(item, "link").text = (
        f"https://www.youtube.com/watch?v={video_id}"
    )

    ET.SubElement(item, "guid").text = video_id

    ET.SubElement(item, "description").text = (
        snippet["description"]
    )

os.makedirs("docs", exist_ok=True)

ET.ElementTree(rss).write(
    "docs/feed.xml",
    encoding="utf-8",
    xml_declaration=True
)

print("RSS feed created!")
