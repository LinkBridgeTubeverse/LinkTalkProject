import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    # 🔑 GitHub Secrets에서 불러온 환경 변수
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("YOUTUBE_API_KEY 환경 변수가 설정되지 않았습니다.")

    # 📺 YouTube API 클라이언트 초기화
    youtube = build("youtube", "v3", developerKey=api_key)

    # 업로드할 영상 파일 경로
    video_file = "sample_video.mp4"

    # 업로드할 영상 메타데이터
    request_body = {
        "snippet": {
            "title": "자동 업로드 테스트 영상",
            "description": "이 영상은 LinkTalkProject 자동 업로드 테스트입니다.",
            "tags": ["LinkTalkProject", "YouTube API", "Automation"],
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
