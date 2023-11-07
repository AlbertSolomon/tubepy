FROM python:3.10.8-slim

COPY . /tubepy/

WORKDIR /tubepy

RUN pip install --upgrade pip

RUN pip install Tk

RUN pip install -r requirements.txt

CMD ["python", "tubepy/setup.py"]
