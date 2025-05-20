FROM python:3.12-slim

WORKDIR /backup

COPY ./requirements.txt /backup/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /backup/requirements.txt

COPY . /backup

RUN chmod +x app_start.sh

CMD ["bash", "app_start.sh"]
