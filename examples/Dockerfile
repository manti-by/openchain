# Use an official Python runtime as a parent image
FROM ubuntu:16.04

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y software-properties-common apt-utils
RUN apt-get install -y build-essential git python3 python3-dev python3-pip python3-venv

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV ROLE pool

# Run app handler when the container launches
CMD ["python3", "run.py"]