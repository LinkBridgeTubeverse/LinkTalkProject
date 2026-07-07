import os
import json
import random
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 서비스 계정 인증 불러오기
credentials = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["YOUTUBE_SERVICE_ACCOUNT"]),
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)
youtube = build("youtube", "v3", credentials=credentials)

# 제휴 링크 생성 함수
def get_affiliate_link(product_url: str) -> str:
    affiliate_id = os.environ["AFFILIATE_ID"]  # GitHub Secrets에 등록한 값
    return f"https://s.click.aliexpress.com/e/{affiliate_id}?target={product_url}"

# 상품 리스트 (랜덤 선택 대상)
products = [
    "https://ko.aliexpress.com/item/1005010661950273.html",
    "https://ko.aliexpress.com/item/987654321.html",
    "https://ko.aliexpress.com/item/123456789.html",
    "https://ko.aliexpress.com/item/555555555.html",
    "https://ko.aliexpress.com/item/666666666.html"
]

# 업로드할 에피소드 데이터
episodes = [
    {
        "file": "episode14.mp4",
        "title": "明 14화 — 내부 균열 본격화",
        "description": "권력자들의 불신과 과학자들의 갈등이 본격화된다...",
        "tags": ["明", "느와르", "정치스릴러", "ProjectMyung"],
        "publish_time": "2026-07-07T12:00:00"
    },
    {
        "file": "episode15.mp4",
        "title": "明 15화 — 최강한의 절에서의 깨달음",
        "description": "최강한이 절에서 깨달음을 얻고 일본행을 결심한다...",
        "tags": ["최강한", "박대한", "NeoNoir"],
        "publish_time": "2026-07-08T12:00:00"
    }
]

# 영상 업로드 함수 (랜덤 상품 링크 삽입)
def upload_video(ep):
    product_url = random.choice(products)  # 랜덤 상품 선택
    affiliate_link = get_affiliate_link(product_url)

    description = ep["description"]
    description += f"\n\n관련 상품 링크: {affiliate_link}"

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": ep["title"],
                "description": description,
                "tags": ep["tags"],
                "categoryId": "24"
            },
            "status": {
                "privacyStatus": "public",
                "publishAt": ep["publish_time"]
            }
        },
        media_body=MediaFileUpload(ep["file"], chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"Uploaded: {ep['title']} (Video ID: {response['id']})")
    return response['id']

if __name__ == "__main__":
    video_ids = []
    for ep in episodes:
        vid = upload_video(ep)
        video_ids.append(vid)

    print("모든 영상 업로드 완료. 랜덤 상품 링크가 각 영상 설명에 추가되었습니다.")
