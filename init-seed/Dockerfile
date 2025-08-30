FROM python:3.11-alpine
RUN pip install --no-cache-dir requests python-dotenv
WORKDIR /app
COPY seed.py /app/seed.py
CMD ["python", "seed.py"]
