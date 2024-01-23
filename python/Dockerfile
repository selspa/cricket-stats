FROM python:3-alpine

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app

# install psycopg dependencies
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

# install pandas dependancies
RUN apk add build-base python3-dev

# upgrade pip and setuptools
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /app

# start the server
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

