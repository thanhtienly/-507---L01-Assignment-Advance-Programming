FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

COPY startup.sh startup.sh

ENTRYPOINT [ "./startup.sh" ]
# Lệnh khởi chạy ứng dụng FastAPI bằng Uvicorn
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]