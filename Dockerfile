FROM python:3.10

WORKDIR /service

COPY ./service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service .

CMD [ "flask", "run", "--host=0.0.0.0" ]
