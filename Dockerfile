FROM python:3.9.18-alpine
WORKDIR /web
COPY . /web/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /web/codejavu

RUN ["chmod", "+x", "/web/codejavu/entrypoint.sh"]

EXPOSE 8000

ENTRYPOINT ["sh", "/web/codejavu/entrypoint.sh"]