from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pandas as pd
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os
import requests

# YouTube API 초기화
def get_youtube_service():
    return build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])

youtube = get_youtube_service()

# 어필리에이트 API 호출 (예시)
def get_affiliate_link(product_id):
    api_url = f"https://affiliate-platform.com/api/link?product={product_id}&ref={os.environ['AFFILIATE_ID']}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get("affiliate_link")
    return None

# 업로드할 에피소드 데이터 (상품 매칭 포함)
episodes = [
    {
        "file": "episode14.mp4",
        "title": "明 14화 — 내부 균열 본격화",
        "description": "권력자들의 불신과 과학자들의 갈등이 본격화된다...",
        "tags": ["明", "느와르", "정치스릴러", "ProjectMyung"],
        "publish_time": "2026-07-07T12:00:00",
        "product_id": "12345"
    },
    {
        "file": "episode15.mp4",
        "title": "明 15화 — 최강한의 절에서의 깨달음",
        "description": "최강한이 절에서 깨달음을 얻고 일본행을 결심한다...",
        "tags": ["최강한", "박대한", "NeoNoir"],
        "publish_time": "2026-07-08T12:00:00",
        "product_id": "67890"
    }
]

# 영상 업로드 함수 (상품 링크 삽입)
def upload_video(ep):
    affiliate_link = get_affiliate_link(ep["product_id"])
    description = ep["description"]
    if affiliate_link:
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

# 성과 분석
def get_video_stats(video_id):
    request = youtube.videos().list(part="statistics", id=video_id)
    response = request.execute()
    stats = response["items"][0]["statistics"]
    return {
        "video_id": video_id,
        "views": stats.get("viewCount", 0),
        "likes": stats.get("likeCount", 0),
        "comments": stats.get("commentCount", 0)
    }

# 보고서 생성
def generate_report(data, filename="youtube_report"):
    df = pd.DataFrame(data)
    df.to_csv(f"{filename}.csv", index=False)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="YouTube Performance Report", ln=True, align="C")

    for row in data:
        pdf.cell(200, 10, txt=f"Video {row['video_id']} - Views: {row['views']}, Likes: {row['likes']}, Comments: {row['comments']}", ln=True)

    pdf.output(f"{filename}.pdf")
    print(f"Reports generated: {filename}.csv and {filename}.pdf")

# 이메일 발송
def send_email_report(to_email, subject, body, attachments):
    msg = MIMEMultipart()
    msg['From'] = os.environ["EMAIL_USER"]
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for file in attachments:
        with open(file, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={file}')
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
    server.send_message(msg)
    server.quit()
    print(f"Email sent to {to_email}")

# 실행
video_ids = []
for ep in episodes:
    vid = upload_video(ep)
    video_ids.append(vid)

stats_data = []
for vid in video_ids:
    stats_data.append(get_video_stats(vid))

generate_report(stats_data)

send_email_report(
    to_email="yybbcc031@fmail.com",
    subject="YouTube Performance Report",
    body="자동 생성된 보고서를 첨부합니다.",
    attachments=["youtube_report.csv", "youtube_report.pdf"]
)
