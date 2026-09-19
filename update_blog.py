import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from urllib.parse import urlparse

BLOG_ID = "nettclean"
RSS_URL = f"https://rss.blog.naver.com/{BLOG_ID}.xml"

OUTPUT_FILE = "blog-posts.json"
IMAGE_DIR = "blog-images"

os.makedirs(IMAGE_DIR, exist_ok=True)

request = urllib.request.Request(
    RSS_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

with urllib.request.urlopen(request, timeout=30) as response:
    rss_data = response.read()

root = ET.fromstring(rss_data)

posts = []

for index, item in enumerate(root.findall(".//item")[:20]):

    title = unescape(item.findtext("title", "").strip())
    link = item.findtext("link", "").strip()
    pub_date = item.findtext("pubDate", "").strip()
    description = item.findtext("description", "")

    image_url = ""

    image_match = re.search(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        description,
        re.IGNORECASE
    )

    if image_match:
        image_url = unescape(image_match.group(1))

        if image_url.startswith("//"):
            image_url = "https:" + image_url

    local_image = ""

    if image_url:
        try:
            # 블로그 글 번호를 파일명으로 사용
            post_match = re.search(r"/(\d+)", link)

            if post_match:
                image_name = f"{post_match.group(1)}.jpg"
            else:
                image_name = f"post-{index}.jpg"

            image_path = os.path.join(IMAGE_DIR, image_name)

            image_request = urllib.request.Request(
                image_url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Referer": "https://blog.naver.com/"
                }
            )

            with urllib.request.urlopen(
                image_request,
                timeout=30
            ) as image_response:

                with open(image_path, "wb") as image_file:
                    image_file.write(image_response.read())

            local_image = image_path

        except Exception as e:
            print(f"이미지 다운로드 실패: {title}")
            print(e)

    posts.append({
        "title": title,
        "link": link,
        "date": pub_date,
        "image": local_image
    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        posts,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"{len(posts)}개의 블로그 글을 저장했습니다.")