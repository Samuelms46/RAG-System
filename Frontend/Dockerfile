FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "streamlit", "run", "page.py", "--server.port", "8800","--server.address", "0.0.0.0" ]