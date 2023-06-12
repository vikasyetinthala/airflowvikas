FROM 
RUN apt-get update && apt-get install -y git
RUN mkdir pipeline
WORKDIR /pipeline
COPY ./ ./
RUN pip install -r requirements.txt
