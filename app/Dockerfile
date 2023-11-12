FROM tensorflow/tensorflow:devel-gpu
RUN pip install --upgrade pip
RUN mkdir /app
ADD . /app
RUN cd /app
RUN ls -la
RUN pip install -r /app/req.txt
WORKDIR /app
CMD [ "python", "manager.py" ]