FROM python:3.12.2

RUN apt-get update && apt-get install -y wget

# Download wait-for-it.sh
RUN wget -qO /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

ENV DB_HOST='db'
ENV DB_PORT=5432
ENV DB_NAME='db_name'
ENV DB_USER='db_user'
ENV DB_PASSWORD='db_pass'
ENV MONGODB_USERNAME='mongo_user'
ENV MONGODB_PASSWORD='mongo_pass'
ENV MONGODB_SERVER='mongo_server'
ENV MONGODB_PORT=27017

WORKDIR /opt/app

COPY . .

COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /data_store

CMD ["python3", "start.sh"]