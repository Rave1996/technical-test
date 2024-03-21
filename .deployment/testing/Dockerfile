FROM python:3.12

LABEL maintainer="The Five Hundred Band"

# Install requirements
RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -U poetry \
    && poetry self add poetry-plugin-export


COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN cd /tmp \
    && poetry export -f requirements.txt --output /tmp/requirements.txt --without-hashes --with dev \
    && pip install --no-warn-script-location --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt

# Copying environment variables
COPY ./envs.sh /tmp/envs.sh
RUN chmod +x /tmp/envs.sh


# Copy code app
WORKDIR /app
COPY . /app

# Testing process
RUN rm -rf reports && mkdir reports
CMD . /tmp/envs.sh && coverage run -m pytest -s -v --lf --junitxml=reports/unittest_report.xml && coverage xml -o reports/coverage.xml && coverage report
