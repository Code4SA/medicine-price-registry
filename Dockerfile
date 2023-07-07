FROM nikolaik/python-nodejs:python3.9-nodejs14

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE DontWarn

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -

RUN set -ex; \
  apt-get update; \
  # dependencies for building Python packages \
  apt-get install -y build-essential; \
  # psycopg2 dependencies \
  apt-get install -y libpq-dev; \
  # git for codecov file listing \
  apt-get install -y git; \
  # cleaning up unused files \
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
  rm -rf /var/lib/apt/lists/*

# Copy, then install requirements before copying rest for a requirements cache layer.
RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY . /app

ARG USER_ID=1001
ARG GROUP_ID=1001

RUN set -ex; \
  addgroup --gid $GROUP_ID --system django; \
  adduser --system --uid $USER_ID --gid $GROUP_ID django; \
  chown -R django:django /app

#USER django

WORKDIR /app

EXPOSE 5000
CMD /app/bin/start.sh