FROM ubuntu:20.04

# Update package list and install necessary packages
RUN apt-get update && \
    apt-get install -y wget gnupg python3 python3-pip

# Download Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome
RUN dpkg -i google-chrome-stable_current_amd64.deb

# Install dependencies (if any)
RUN apt-get -f install -y

# Download ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip

# Set working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Specify the default command to run on container start
CMD ["python3", "bot.py"]
