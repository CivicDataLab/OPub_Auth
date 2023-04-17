FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV KEYCLOAK_URL=https://kc.ndp.civicdatalab.in/auth/

RUN echo 'deb http://deb.debian.org/debian stretch main' >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get autoremove -y && \
    apt-get install -y libssl1.0-dev curl git nano wget screen vim && \
    rm -rf /var/lib/apt/lists/* && rm -rf /var/lib/apt/lists/partial/*

WORKDIR /code
COPY OPub_Auth/requirements.txt /code/
COPY OPub_Auth/ /code/
COPY opub_back_env/lib/python3.10/site-packages/ /usr/local/lib/python3.10/
ENV PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.10/"

RUN pip uninstall psycopg2-binary
RUN pip install psycopg2-binary
RUN python manage.py migrate
RUN python manage.py createcachetable

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]