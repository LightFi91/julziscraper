# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Create a volume named 'bata' and set it as the mount point for /app/data
VOLUME /app/batadb

# Set an environment variable to determine which script to run
ENV SCRIPT_NAME bata.py

# Run app.py when the container launches
CMD python $SCRIPT_NAME