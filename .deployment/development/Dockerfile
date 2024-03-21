FROM python:3.12

LABEL maintainer="Fairplay"

# Install requirements
RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -U poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN cd /tmp \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

WORKDIR /app

COPY ./src /app

EXPOSE 9000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
