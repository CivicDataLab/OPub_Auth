FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV KEYCLOAK_URL=https://kc.ndp.civicdatalab.in/auth/

# RUN echo 'deb http://deb.debian.org/debian stretch main' >> /etc/apt/sources.list && \
#     apt-get update && \
#     apt-get autoremove -y && \
#     apt-get install -y libssl1.0-dev curl git nano wget screen vim && \
#     rm -rf /var/lib/apt/lists/* && rm -rf /var/lib/apt/lists/partial/*

WORKDIR /code
COPY requirements.txt /code/
COPY . /code/
# COPY opub_back_env/lib/python3.10/site-packages/ /usr/local/lib/python3.10/
# ENV PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.10/"

# RUN pip uninstall -y psycopg2-binary
# RUN pip install psycopg2-binary
RUN pip install -r /code/requirements.txt
# RUN python manage.py migrate
# RUN python manage.py createcachetable

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]