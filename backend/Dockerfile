FROM python:3.11-slim



RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY ./pyproject.toml .
COPY ./poetry.lock* .

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi 


COPY . $APP_HOME

RUN chmod +x /home/app/web/entrypoint.sh

CMD [ "/home/app/web/entrypoint.sh" ]