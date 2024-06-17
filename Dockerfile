FROM python:3.12-slim

WORKDIR /app/src

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
