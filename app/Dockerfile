FROM python:3.11.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

COPY db.sqlite3 .

EXPOSE 8000

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]