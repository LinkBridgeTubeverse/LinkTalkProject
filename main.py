import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# 📌 접근 권한 범위 (YouTube 업로드 권한)
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_credentials():
    creds = None
    # token.json이 이미 있으면 불러오기
    if os.path.exists("token.json"):
        with open("token.json", "r") as token:
            creds_data = json.load(token)
            from google.oauth2.credentials import Credentials
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    # 없거나 만료되었으면 새로 인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # 새 토큰 저장
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def main():
    # 🔑 OAuth 인증 진행
    creds = get_credentials()

    # 📺 YouTube API 클라이언트 초기화
    youtube = build("youtube", "v3", credentials=creds)

    # 📂 업로드할 영상 파일
    video_file = "sample_video.mp4"

    # 📝 업로드할 영상 메타데이터
    request_body = {
        "snippet": {
            "title": "테스트 업로드 영상",
            "description": "이 영상은 GitHub Actions와 YouTube API 업로드 테스트입니다.",
            "tags": ["Test", "YouTube API", "Automation"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "private"  # 공개 설정: public, unlisted, private
        }
    }

    # 📤 영상 업로드 요청
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print("✅ 업로드 완료! 영상 ID:", response["id"])

if __name__ == "__main__":
    main()
