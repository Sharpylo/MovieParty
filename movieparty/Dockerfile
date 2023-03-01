FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash mp && chmod 777 /opt /run

WORKDIR /mp

RUN mkdir /mp/static && mkdir /mp/media && chown -R mp:mp /mp && chmod 755 /mp

COPY --chown=mp:mp . .

RUN pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get update &&  \
    apt-get install -y gunicorn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

USER mp

CMD ["gunicorn", "-b", '0.0.0.0:8000', 'movieparty.wsgi:application']
