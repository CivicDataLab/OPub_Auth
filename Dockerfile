FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV KEYCLOAK_URL=https://kc.ndp.civicdatalab.in/auth/
WORKDIR /code
COPY OPub_Auth/requirements.txt /code/
COPY OPub_Auth/ /code/
COPY opub_back_env/lib/python3.10/site-packages/ /usr/local/lib/python3.10/
ENV PYTHONPATH="$PYTHONPATH:/usr/local/lib/python3.10/"
RUN pip install psycopg2-binary
RUN python OPub_Auth/manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]