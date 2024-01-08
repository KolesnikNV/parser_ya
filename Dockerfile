FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y wget gnupg python3 python3-pip \

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN dpkg -i google-chrome-stable_current_amd64.deb

RUN apt-get -f install -y

RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]
