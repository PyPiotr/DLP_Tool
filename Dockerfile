FROM python:3.10

WORKDIR /app
RUN apt-get update -y 
RUN apt-get install build-essential && \
            apt-get install python3-dev -y && \
            apt-get install default-libmysqlclient-dev -y
            
RUN pip3 install pipenv
COPY Pipfile* ./
RUN pipenv install
COPY . . 
RUN chmod +x ./start.sh ./wait-for
EXPOSE 8000



