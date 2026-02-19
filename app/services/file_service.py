
import os
from fastapi import UploadFile
from datetime import datetime

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(file: UploadFile) -> str:
	"""
	업로드 파일을 static/uploads/에 저장하고, 파일 URL을 반환한다.
	파일이 없거나 파일명이 없거나 파일 크기가 0이면 저장하지 않고 None 반환

	파일 크기 체크 로직:
	- file.file.seek(0, 2): 파일 끝으로 이동
	- file.file.tell(): 파일 크기(바이트) 반환
	- file.file.seek(0): 다시 파일 처음으로 이동
	이 로직은 사용자가 파일을 첨부하지 않았거나, 빈 파일을 첨부한 경우
	uploads 폴더에 불필요한 빈 파일이 생성되는 것을 방지하기 위한 안전장치입니다.
	실제 내용이 있는 파일만 저장되도록 합니다.
	"""
	if not file or not file.filename:
		return None
	file.file.seek(0, 2)  # 파일 끝으로 이동
	size = file.file.tell()  # 파일 크기 확인
	file.file.seek(0)     # 다시 처음으로 이동
	if size == 0:
		return None
	filename = datetime.now().strftime('%Y%m%d%H%M%S_') + file.filename
	file_path = os.path.join(UPLOAD_DIR, filename)
	with open(file_path, 'wb') as f:
		f.write(file.file.read())
	return f"/static/uploads/{filename}"
