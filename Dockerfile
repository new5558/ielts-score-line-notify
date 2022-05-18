FROM python:3.9-slim

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# CMD python main.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 main:app