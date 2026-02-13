
import os
from fastapi import UploadFile
from datetime import datetime

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload_file(file: UploadFile) -> str:
	"""
	업로드 파일을 static/uploads/에 저장하고, 파일 URL을 반환한다.
	"""
	filename = datetime.now().strftime('%Y%m%d%H%M%S_') + file.filename
	file_path = os.path.join(UPLOAD_DIR, filename)
	with open(file_path, 'wb') as f:
		f.write(file.file.read())
	# URL 경로 반환 (예: /static/uploads/파일명)
	return f"/static/uploads/{filename}"
