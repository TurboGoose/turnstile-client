FROM python:3.9
WORKDIR /app
RUN apt-get update && apt-get install -y cmake
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN bash ./download_crt.sh
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]