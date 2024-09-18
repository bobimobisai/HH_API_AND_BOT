FROM python:3.12.3-slim-bullseye


WORKDIR .
COPY . .


RUN pip install --upgrade setuptools
RUN pip install -r  requirements.txt

CMD ["sh", "-c", "alembic revision --autogenerate -m 'Initial migration' && alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8020"]
