# pull official base image
FROM python

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt /usr/src/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy project

COPY . /usr/src

#EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]

#CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--workers", "4"]