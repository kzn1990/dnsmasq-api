FROM python:3.8

COPY tests.py app.py requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

RUN /usr/local/bin/pytest -v tests.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
