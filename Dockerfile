FROM python:3.10.8-slim 

COPY . /tubepy/

WORKDIR /tubepy

RUN pip install -r requirements.txt

RUN pip install tkinter

CMD ["python", "tubepy/setup.py"]
