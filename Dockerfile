# Use the official Ubuntu 20.04 image
FROM ubuntu:20.04

# Update package list and install necessary packages
RUN apt-get update && \
    apt-get install -y wget gnupg python3 python3-pip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable
# Set the working directory
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Specify the default command to run on container startup
CMD ["python3", "bot.py"]
