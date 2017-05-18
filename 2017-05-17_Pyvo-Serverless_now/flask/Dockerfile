FROM python:3.5

RUN python3 -m venv venv 
RUN venv/bin/pip install flask gunicorn

COPY hello.py .

EXPOSE 8000

CMD ["venv/bin/gunicorn", "--bind", "0.0.0.0:8000", "hello:app"]
