FROM python:3.7-alpine

WORKDIR /app

RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --system 

COPY . .

CMD ["python","code/app.py"]

# For Cloud Run
# RUN pip install gunicorn
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
