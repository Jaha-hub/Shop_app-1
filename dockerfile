FROM python:3.12-alpine

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0" ]