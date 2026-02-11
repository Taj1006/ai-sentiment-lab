FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD [&quot;streamlit&quot;, &quot;run&quot;, &quot;app.py&quot;, &quot;--server.address=0.0.0.0&quot;]