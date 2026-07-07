# LinkTalkProject

YouTube 자동화 및 OpenWiki 문서 업데이트를 위한 프로젝트입니다.  
이 저장소는 **main.py 실행 환경**과 **GitHub Actions 워크플로우**를 통해 자동화된 작업을 수행합니다.

---

## 🚀 프로젝트 개요
- **main.py**: YouTube API를 활용한 자동 업로드 및 관리 코드
- **.github/workflows**:
  - `python.yml`: main.py 실행 자동화
  - `openwiki.yml`: OpenWiki 문서 자동 업데이트
  - `main.yml`: 기타 관리용 워크플로우

---

## ⚙️ 실행 방법
### 1. 로컬 실행
```bash
python main.py
