# 🚀 SolarScan 빠른 시작 가이드

이 문서는 SolarScan 프로젝트를 **5분 안에** 로컬에서 실행하는 방법을 안내합니다.

## 📋 사전 준비

다음 소프트웨어가 설치되어 있어야 합니다:

- ✅ **Node.js** 18+ ([다운로드](https://nodejs.org/))
- ✅ **Python** 3.11+ ([다운로드](https://www.python.org/downloads/))
- ✅ **Git** ([다운로드](https://git-scm.com/downloads))

## 🎯 Step 1: 프로젝트 클론

```bash
cd ~/Dev  # 또는 원하는 디렉토리
git clone https://github.com/your-username/solar-ai-platform.git
cd solar-ai-platform
```

## 🔧 Step 2: Backend 설정 및 실행

### 2-1. Python 가상환경 생성

```bash
cd backend
python3 -m venv venv
```

### 2-2. 가상환경 활성화

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 2-3. 의존성 설치

```bash
pip install -r requirements.txt
```

이 과정은 1-2분 정도 소요됩니다.

### 2-4. 환경 변수 설정

```bash
cp env.example .env
```

`.env` 파일을 열고 다음 항목만 수정하세요 (나머지는 기본값 사용):

```env
# 개발 모드에서는 이 정도만 설정하면 됩니다
ENVIRONMENT=development
DEBUG=True

# 나중에 실제 API 키 발급받으면 추가
# KAKAO_REST_API_KEY=your_key_here
# GYEONGGI_CLIMATE_API_KEY=your_key_here
```

### 2-5. Backend 서버 실행

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **성공!** Backend가 http://localhost:8000 에서 실행됩니다.

브라우저에서 http://localhost:8000/docs 를 열어 API 문서를 확인하세요.

**이 터미널 창은 열어두고, 새 터미널을 열어 다음 단계를 진행하세요.**

## 🎨 Step 3: Frontend 설정 및 실행

### 3-1. 새 터미널 열기

프로젝트 루트 디렉토리로 이동:

```bash
cd ~/Dev/solar-ai-platform/frontend
```

### 3-2. 의존성 설치

```bash
npm install
```

이 과정은 1-2분 정도 소요됩니다.

### 3-3. 환경 변수 설정

```bash
cp .env.example .env.local
```

`.env.local` 파일을 열고 다음과 같이 설정:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3-4. Frontend 서버 실행

```bash
npm run dev
```

✅ **성공!** Frontend가 http://localhost:3000 에서 실행됩니다.

## 🎉 Step 4: 웹사이트 접속

브라우저에서 http://localhost:3000 을 열면 SolarScan 홈페이지가 나타납니다!

### 테스트 해보기

1. 주소 입력창에 다음을 입력:
   ```
   경기도 수원시 영통구 광교로 156
   ```

2. **"분석 시작"** 버튼 클릭

3. 약 30초 후 분석 결과 페이지로 이동합니다.

## 🔍 주요 페이지

- **홈페이지**: http://localhost:3000
- **API 문서**: http://localhost:8000/docs
- **API 헬스체크**: http://localhost:8000/health

## 🛠 문제 해결

### Backend 실행 시 오류

**오류: `ModuleNotFoundError: No module named 'fastapi'`**

```bash
# 가상환경이 활성화되어 있는지 확인
which python  # venv 경로가 나와야 함

# 의존성 재설치
pip install -r requirements.txt
```

**오류: `Address already in use`**

```bash
# 8000 포트를 사용 중인 프로세스 종료
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID번호> /F
```

### Frontend 실행 시 오류

**오류: `EADDRINUSE: address already in use :::3000`**

```bash
# 3000 포트를 사용 중인 프로세스 종료
# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID번호> /F
```

**오류: `npm ERR! code ENOENT`**

```bash
# Node.js 버전 확인 (18+ 필요)
node --version

# npm 캐시 정리
npm cache clean --force

# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

## 📚 다음 단계

### 1. 실제 API 연동

현재는 더미 데이터를 사용하고 있습니다. 실제 데이터를 사용하려면:

#### Kakao Maps API 키 발급
1. https://developers.kakao.com/ 접속
2. 내 애플리케이션 → 애플리케이션 추가
3. REST API 키 복사
4. `backend/.env`에 추가:
   ```env
   KAKAO_REST_API_KEY=your_key_here
   ```

#### 경기도 기후플랫폼 API 키 발급
1. https://climate.gg.go.kr/ 접속
2. API 신청 (담당자 문의 필요)
3. `backend/.env`에 추가:
   ```env
   GYEONGGI_CLIMATE_API_KEY=your_key_here
   ```

### 2. 데이터베이스 설정 (선택)

개발 초기에는 메모리 DB로 충분하지만, 실제 데이터를 저장하려면:

#### PostgreSQL 설치 및 설정

**macOS (Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
createdb solarscan
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgis
sudo -u postgres createdb solarscan
```

**Windows:**
1. https://www.postgresql.org/download/windows/ 에서 설치
2. pgAdmin으로 `solarscan` 데이터베이스 생성

#### 환경 변수 업데이트
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/solarscan
```

#### 마이그레이션 실행
```bash
cd backend
alembic upgrade head
```

### 3. Redis 설정 (선택)

캐싱 및 성능 향상을 위해:

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu:**
```bash
sudo apt install redis-server
sudo systemctl start redis
```

**Windows:**
https://github.com/microsoftarchive/redis/releases 에서 다운로드

### 4. AI 모델 학습

실제 데이터로 AI 모델을 학습하려면:

```bash
cd models/training

# 샘플 데이터로 학습 (테스트용)
python train.py --mode test

# 실제 데이터로 학습 (데이터 수집 후)
python train.py --mode production --epochs 500
```

## 🎓 학습 자료

- **사업 계획서**: `docs/business_plan/사업계획서.md`
- **기술 문서**: `docs/technical/기술_아키텍처.md`
- **API 문서**: http://localhost:8000/docs
- **전체 README**: `README.md`

## 💡 개발 팁

### Hot Reload 활용

- **Backend**: 코드 수정 시 자동 재시작 (`--reload` 옵션)
- **Frontend**: 코드 수정 시 자동 새로고침 (Next.js Fast Refresh)

### 디버깅

**Backend 디버깅:**
```python
# api/main.py에 추가
import pdb; pdb.set_trace()
```

**Frontend 디버깅:**
```typescript
// 브라우저 콘솔에서
console.log('Debug:', data);
```

### 코드 포맷팅

**Backend:**
```bash
cd backend
black .  # 자동 포맷팅
```

**Frontend:**
```bash
cd frontend
npm run lint  # 린트 체크
```

## 🚀 프로덕션 배포

프로덕션 배포 가이드는 `README.md`의 "배포" 섹션을 참고하세요.

## 📞 도움이 필요하신가요?

- **GitHub Issues**: https://github.com/your-username/solar-ai-platform/issues
- **이메일**: contact@solarscan.kr
- **Discord**: https://discord.gg/solarscan (예정)

## ✅ 체크리스트

프로젝트가 제대로 실행되고 있는지 확인하세요:

- [ ] Backend 서버가 http://localhost:8000 에서 실행 중
- [ ] API 문서가 http://localhost:8000/docs 에서 보임
- [ ] Frontend 서버가 http://localhost:3000 에서 실행 중
- [ ] 홈페이지에서 주소 입력 가능
- [ ] "분석 시작" 버튼 클릭 시 결과 페이지로 이동

모두 체크되었다면 성공입니다! 🎉

---

**Happy Coding! ☀️**

