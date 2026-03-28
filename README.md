## 실행 방법

### 1. Back-End 서버 실행
```bash
# 가상환경 활성화
conda activate be

# 백엔드 디렉토리로 이동
cd gayeon/human-evaluation/backend

# 서버 실행
uvicorn main:app --reload
```

### 2. Front-End 서버 실행
``` bash
# 가상환경 활성화
conda activate fe

# 프론트엔드 디렉토리로 이동
cd gayeon/human-evaluation/frontend

# 서버 실행
npm run dev
```
