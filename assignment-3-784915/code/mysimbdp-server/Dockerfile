# Get Docker image
FROM python:3.6-stretch

# Here we define '/server' as base directory (where all commands will be executed).
WORKDIR /server

# Install requirements and update dependencies
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update

# Here we put files at the image '/server' folder.
ADD server/ /server

# Run server 
CMD python batchingestmanager.py