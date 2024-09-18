FROM public.ecr.aws/lambda/python:3.9
COPY . .

RUN python3 -m venv env
RUN source env/bin/activate
RUN ls
RUN pip install -r requirements.txt
RUN pwd
RUN ls
WORKDIR /var/task
# RUN chmod -R 777 /ar/task/
