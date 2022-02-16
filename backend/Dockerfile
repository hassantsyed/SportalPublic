FROM python:3.7

EXPOSE 8000

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "SportBook.wsgi:application"]
