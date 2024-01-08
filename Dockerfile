# Use the official Ubuntu 20.04 image
FROM ubuntu:20.04

# Update package list and install necessary packages
RUN apt-get update && \
    apt-get install -y wget gnupg python3 python3-pip

# Download Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install dependencies for Google Chrome
RUN apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libcurl3-gnutls \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libu2f-udev \
    libvulkan1 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils

# Install Google Chrome
RUN dpkg -i google-chrome-stable_current_amd64.deb

# Download ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip

# Unzip ChromeDriver
RUN apt-get install -y unzip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Specify the default command to run on container startup
CMD ["python3", "bot.py"]
