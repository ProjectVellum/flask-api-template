# Use an official Python runtime as a parent image
FROM ubuntu:18.04

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN export LANG=C.UTF-8
RUN apt update -y; apt install -y python3-pip git

# Install any needed packages specified in requirements.txt
RUN pip3 install -e .
RUN pip3 install -r requirements.txt

RUN /bin/bash ./flask_fat/tests/test_all.sh

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME GXP

# Run app.py when the container launches
CMD ["bash", "./gxp/tests/everything.sh"]