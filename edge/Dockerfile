FROM python:3.9
WORKDIR /app
RUN apt-get update && apt-get install cmake ffmpeg libsm6 libxext6  -y
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN bash ./download_crt.sh
CMD ["python3", "main.py"]