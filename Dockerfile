# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /final_articleProj

# Set the working directory to /app
COPY . /final_articleProj

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# # Run app.py on port 5000 first = host machine, second = flask of docker container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "server.py"]

# Not running doc2vec, need to change that