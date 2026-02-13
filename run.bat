@echo off
REM 가상환경 활성화 (필요시 경로 수정)
call .venv\Scripts\activate

REM FastAPI 앱 실행 (포트, 리로드 옵션 등 필요에 따라 수정)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause