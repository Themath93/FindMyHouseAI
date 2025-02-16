# 🏡 FindMyHouseAI

## 📌 프로젝트 개요
서울주택공사(SH) 및 한국토지주택공사(LH)에서 제공하는 청년 및 신혼부부 대상 임대주택 공고 PDF를 자동으로 수집하여, LangGraph와 Streamlit을 활용해 사용자의 조건에 맞는 최적의 임대 정보를 추천하는 AI Agent 앱을 개발합니다.

## 🚀 주요 기능
- **임대주택 공고 수집**: SH 및 LH의 임대주택 공고 PDF 자동 크롤링 및 업데이트
- **텍스트 임베딩**: 공고 내용을 벡터화하여 효율적인 검색 및 추천 가능
- **AI 기반 검색 및 추천**: 사용자 입력 조건(연령, 소득, 거주지역 등)에 맞춰 최적의 공고 추천
- **Streamlit UI 제공**: 직관적인 웹 인터페이스를 통해 누구나 쉽게 사용 가능
- **LangGraph 기반 AI Workflow**: 사용자 입력 → 조건 필터링 → 최적 공고 추천

## 🛠️ 기술 스택
- **프로그래밍 언어**: Python
- **AI 프레임워크**: LangGraph, OpenAI API (또는 LlamaIndex)
- **웹 프레임워크**: Streamlit
- **데이터 저장소**: FAISS 또는 ChromaDB (벡터DB 활용)
- **PDF 처리**: PyMuPDF, pdfplumber
- **크롤링**: Selenium, BeautifulSoup

## 🏗️ 설치 및 실행 방법
### 1️⃣ 프로젝트 클론
```bash
git clone https://github.com/Themath93/FindMyHouseAI.git
cd FindMyHouseAI
```

### 2️⃣ 가상 환경 설정 (선택 사항)
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ 필수 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 4️⃣ Streamlit 앱 실행
```bash
streamlit run main.py
```

## 📊 데이터 처리 파이프라인
1. **SH/LH 홈페이지에서 PDF 크롤링** (Selenium, BeautifulSoup 활용)
2. **텍스트 추출 및 전처리** (PyMuPDF, pdfplumber 활용)
3. **텍스트 임베딩 생성** (OpenAI Embedding API 또는 Sentence Transformers 활용)
4. **벡터DB 저장 및 검색** (FAISS 또는 ChromaDB 활용)
5. **사용자 입력 기반 공고 추천** (LangGraph 기반 AI Workflow 실행)

## 🤝 기여 방법
1. 이슈를 확인하고 원하는 작업을 선택합니다.
2. 새로운 브랜치를 생성하고 기능을 추가합니다.
3. 변경사항을 커밋한 후, PR(Pull Request)을 생성합니다.

## 📜 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.

---

💡 **문의 및 피드백**
- 프로젝트에 대한 아이디어 또는 질문이 있다면 Issue 또는 Discussions를 활용해주세요!
- 더 나은 프로젝트를 위해 PR은 언제나 환영입니다! 🙌
