# a base debian image with google cloud sdk tools
FROM google/cloud-sdk:latest

# copy only the needed files
WORKDIR /app
COPY main.py requirements.txt .env create-database-and-tables.sh /app/

# build-arg mode -> environment variable MODE
ARG mode
ENV MODE=$mode

# install postgresql-13
RUN apt-get update && \
    apt-get -y install wget && \
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && \
    apt-get -y install postgresql-13

# install requirements.txt
RUN pip install -r requirements.txt

# make the bash script executable
RUN chmod +x create-database-and-tables.sh

EXPOSE 8000

# sleep forever
CMD ["sleep", "infinity"]
