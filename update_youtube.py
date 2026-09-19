import json
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCgyaTqiC7D4MaOfw8T1n9jA"

FEED_URL = (
    "https://www.youtube.com/feeds/videos.xml"
    f"?channel_id={CHANNEL_ID}"
)

OUTPUT_FILE = "youtube-videos.json"

request = urllib.request.Request(
    FEED_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    feed_data = response.read()

root = ET.fromstring(feed_data)

namespaces = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015"
}

videos = []

for entry in root.findall("atom:entry", namespaces)[:10]:

    video_id = entry.findtext(
        "yt:videoId",
        default="",
        namespaces=namespaces
    )

    title = entry.findtext(
        "atom:title",
        default="",
        namespaces=namespaces
    )

    published = entry.findtext(
        "atom:published",
        default="",
        namespaces=namespaces
    )

    if not video_id:
        continue

    videos.append({
        "title": title,
        "videoId": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "embed": f"https://www.youtube.com/embed/{video_id}",
        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "published": published
    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        videos,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"{len(videos)}개의 유튜브 영상을 저장했습니다.")