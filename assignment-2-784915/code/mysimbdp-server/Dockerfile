# Get Docker image
FROM python:3.6-stretch

# Here we put files at the image '/server' folder.
ADD server/ /server

# Here we define '/server' as base directory (where all commands will be executed).
WORKDIR /server

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Update dependencies
RUN apt-get update

# Run server
CMD python batchingestmanager.py