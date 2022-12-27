# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11

EXPOSE 8000

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
#COPY ./app /code/app
 
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
#"gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"