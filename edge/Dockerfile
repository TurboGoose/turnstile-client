FROM python:3.9
WORKDIR /app
RUN apt update
RUN apt install -y cmake
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["python3", "main.py"]