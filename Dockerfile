FROM python:3.10.8-slim 

COPY . /tubepy/

WORKDIR /tubepy

RUN pip install -r requirements.txt

CMD ["python", "tubepy/setup.py"]
