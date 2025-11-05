# 🌞 SolarScan - AI 기반 태양광 설치 최적화 플랫폼

경기도 기후플랫폼(climate.gg.go.kr) 데이터를 활용하여 태양광 설치 적합성과 예상 비용 절감액을 AI로 분석하는 웹 플랫폼입니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [시작하기](#시작하기)
- [프로젝트 구조](#프로젝트-구조)
- [API 문서](#api-문서)
- [배포](#배포)
- [기여하기](#기여하기)

## 🎯 프로젝트 개요

### 문제 정의
- 태양광 설치를 고려하는 사람들이 **사전에 정확한 정보를 얻기 어려움**
- 부동산 방문 전 태양광 설치 가능성을 확인할 방법 부족
- 설치 비용 대비 실제 절감액을 계산하기 복잡함

### 솔루션
- **AI 기반 발전량 예측**: 경기도 기후 데이터를 학습한 AI 모델로 정확한 발전량 예측
- **자동 지붕 분석**: 위성 이미지 분석으로 지붕 면적, 방향, 경사각 자동 계산
- **경제성 분석**: 설치 비용, 보조금, 절감액, ROI 자동 계산
- **30초 분석**: 주소 입력 후 30초 이내 결과 제공

### 타겟 사용자
1. **주택 구매 예정자**: 부동산 보기 전 태양광 설치 가능성 확인
2. **기존 주택 소유자**: 태양광 설치 고려 중인 사람
3. **B2B 파트너**: 부동산 중개업소, 태양광 설치 업체

## ✨ 주요 기능

### 1. 주소 기반 분석
```
입력: 경기도 수원시 영통구 광교로 156
↓
AI 분석 (30초)
↓
출력:
  - 지붕 분석 (면적, 방향, 경사각)
  - 발전량 예측 (월별, 연간)
  - 경제성 분석 (비용, 절감액, ROI)
  - 환경 기여도 (CO2 감축, 나무 심기 효과)
```

### 2. 비교 분석
- 최대 5개 주소 동시 비교
- 일사량, 발전량, 절감액 비교 차트
- 최적 위치 추천

### 3. 히트맵
- 경기도 전역 일사량 히트맵
- 지역별 태양광 효율 순위
- 클릭으로 해당 지역 분석

### 4. 프리미엄 리포트
- 상세 PDF 리포트 다운로드
- 20년 시뮬레이션
- 최적 설치 용량 추천
- 업체별 견적 비교

## 🛠 기술 스택

### Frontend
```json
{
  "framework": "Next.js 14 (App Router)",
  "language": "TypeScript",
  "styling": "Tailwind CSS",
  "state": "Zustand",
  "charts": "Recharts",
  "maps": "Kakao Maps API"
}
```

### Backend
```python
{
    "framework": "FastAPI",
    "language": "Python 3.11+",
    "database": "PostgreSQL + PostGIS",
    "cache": "Redis",
    "queue": "Celery + RabbitMQ",
    "ml": "XGBoost, TensorFlow",
    "cv": "OpenCV"
}
```

### Infrastructure
- **Cloud**: AWS (EC2, RDS, S3)
- **Frontend Hosting**: Vercel
- **Container**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, CloudWatch

## 🚀 시작하기

### 사전 요구사항

- **Node.js** 18+ (Frontend)
- **Python** 3.11+ (Backend)
- **PostgreSQL** 15+ (PostGIS 확장)
- **Redis** 7+
- **Docker** & **Docker Compose** (선택)

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/solar-ai-platform.git
cd solar-ai-platform
```

### 2. Backend 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp env.example .env
# .env 파일을 열어 필요한 값 입력

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Backend가 http://localhost:8000 에서 실행됩니다.

### 3. Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
# .env.local 파일을 열어 API URL 설정

# 개발 서버 실행
npm run dev
```

Frontend가 http://localhost:3000 에서 실행됩니다.

### 4. Docker로 실행 (선택)

```bash
# 전체 스택 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

## 📁 프로젝트 구조

```
solar-ai-platform/
├── backend/                    # FastAPI 백엔드
│   ├── api/                    # API 엔드포인트
│   │   ├── main.py            # 메인 애플리케이션
│   │   └── routes/            # API 라우트
│   ├── services/              # 비즈니스 로직
│   │   ├── analysis.py        # 분석 서비스
│   │   ├── prediction.py      # AI 예측
│   │   └── economics.py       # 경제성 분석
│   ├── models/                # 데이터 모델
│   │   ├── database.py        # DB 모델
│   │   └── schemas.py         # Pydantic 스키마
│   ├── data_collectors/       # 데이터 수집
│   │   ├── climate_collector.py
│   │   └── satellite_collector.py
│   ├── utils/                 # 유틸리티
│   │   ├── cache.py
│   │   ├── security.py
│   │   └── validators.py
│   └── requirements.txt       # Python 의존성
│
├── frontend/                  # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/              # App Router 페이지
│   │   │   ├── page.tsx      # 홈페이지
│   │   │   ├── analysis/     # 분석 결과 페이지
│   │   │   ├── compare/      # 비교 페이지
│   │   │   └── heatmap/      # 히트맵 페이지
│   │   ├── components/       # React 컴포넌트
│   │   │   ├── ui/           # 기본 UI 컴포넌트
│   │   │   ├── analysis/     # 분석 관련 컴포넌트
│   │   │   └── map/          # 지도 컴포넌트
│   │   ├── services/         # API 클라이언트
│   │   ├── hooks/            # Custom Hooks
│   │   ├── stores/           # Zustand 스토어
│   │   └── types/            # TypeScript 타입
│   └── package.json
│
├── models/                    # AI 모델
│   ├── training/             # 모델 학습 스크립트
│   │   ├── solar_prediction_model.py
│   │   ├── roof_analysis_model.py
│   │   └── train.py
│   └── inference/            # 추론 스크립트
│
├── data/                     # 데이터
│   ├── raw/                  # 원본 데이터
│   ├── processed/            # 전처리된 데이터
│   └── models/               # 학습된 모델 파일
│
├── docs/                     # 문서
│   ├── business_plan/        # 사업 계획서
│   ├── technical/            # 기술 문서
│   └── api/                  # API 문서
│
├── docker-compose.yml        # Docker Compose 설정
└── README.md                 # 이 파일
```

## 📚 API 문서

### 주요 엔드포인트

#### 1. 분석 요청
```http
POST /api/v1/analysis
Content-Type: application/json

{
  "address": "경기도 수원시 영통구 광교로 156",
  "building_type": "house",
  "email": "user@example.com"
}
```

**응답:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "분석이 시작되었습니다.",
  "estimated_time": 30
}
```

#### 2. 결과 조회
```http
GET /api/v1/analysis/{request_id}
```

**응답:**
```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "location": {
    "address": "경기도 수원시 영통구 광교로 156",
    "latitude": 37.2858,
    "longitude": 127.0444
  },
  "roof_analysis": {
    "roof_area": 150.0,
    "roof_direction": "S",
    "roof_angle": 25.0,
    "usable_area": 135.0
  },
  "solar_prediction": {
    "recommended_capacity": 18.0,
    "annual_generation": 3650.0,
    "monthly_generation": {...}
  },
  "economic_analysis": {
    "installation_cost": 9000000,
    "subsidy_amount": 1800000,
    "net_cost": 7200000,
    "annual_savings": 547500,
    "payback_period": 13.2
  },
  "environmental_impact": {
    "co2_reduction": 1.55,
    "tree_equivalent": 235
  }
}
```

#### 3. 비교 분석
```http
POST /api/v1/compare
Content-Type: application/json

{
  "addresses": [
    "경기도 수원시 영통구 광교로 156",
    "경기도 성남시 분당구 판교역로 235"
  ]
}
```

#### 4. 히트맵 데이터
```http
GET /api/v1/heatmap?region=gyeonggi&metric=solar_radiation
```

전체 API 문서: http://localhost:8000/docs

## 🔧 개발 가이드

### Backend 개발

```bash
cd backend

# 테스트 실행
pytest tests/ -v

# 코드 포맷팅
black .

# 타입 체크
mypy .

# 새 마이그레이션 생성
alembic revision --autogenerate -m "description"
```

### Frontend 개발

```bash
cd frontend

# 타입 체크
npm run type-check

# 린트
npm run lint

# 빌드
npm run build

# 프로덕션 실행
npm run start
```

### AI 모델 학습

```bash
cd models/training

# 데이터 전처리
python preprocess_data.py

# 모델 학습
python train.py --model xgboost --epochs 100

# 모델 평가
python evaluate.py --model-path ../data/models/solar_xgboost_v1.pkl
```

## 🚢 배포

### Backend 배포 (AWS EC2)

```bash
# Docker 이미지 빌드
docker build -t solarscan-backend:latest ./backend

# ECR에 푸시
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin {account-id}.dkr.ecr.ap-northeast-2.amazonaws.com
docker tag solarscan-backend:latest {account-id}.dkr.ecr.ap-northeast-2.amazonaws.com/solarscan-backend:latest
docker push {account-id}.dkr.ecr.ap-northeast-2.amazonaws.com/solarscan-backend:latest

# ECS 서비스 업데이트
aws ecs update-service --cluster solarscan-cluster --service solarscan-backend --force-new-deployment
```

### Frontend 배포 (Vercel)

```bash
cd frontend

# Vercel CLI 설치
npm install -g vercel

# 배포
vercel --prod
```

## 📊 모니터링

### 로그 확인

```bash
# Backend 로그
docker-compose logs -f backend

# Celery Worker 로그
docker-compose logs -f celery

# 전체 로그
docker-compose logs -f
```

### 메트릭

- **Sentry**: 에러 모니터링
- **CloudWatch**: 인프라 모니터링
- **Grafana**: 커스텀 대시보드

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 코딩 컨벤션

- **Python**: PEP 8, Black formatter
- **TypeScript**: ESLint, Prettier
- **Commit**: Conventional Commits

## 📝 라이선스

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 문의

- **이메일**: contact@solarscan.kr
- **웹사이트**: https://solarscan.kr
- **GitHub Issues**: https://github.com/your-username/solar-ai-platform/issues

## 🙏 감사의 말

- **경기도 기후플랫폼**: 기후 데이터 제공
- **Kakao Maps**: 지도 및 위성 이미지 API
- **한국에너지공단**: 태양광 관련 정보

---

**Made with ☀️ by SolarScan Team**

