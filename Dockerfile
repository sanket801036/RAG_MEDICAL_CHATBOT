## Parent image
FROM python:3.10-slim

## Essential environment variables # These are must for your production grade project.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies #Uh these are some basic commands to update our all the packages inside it and building essential libraries dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying all contents from local to container
COPY . .
# Now we are copying all the contents from local to container..We have created one app directory inside the docker container.Okay, now it will be copying all the things.From here you can see on the left it will be copying all the things and pasting it inside this app directory.

## Install Python dependencies # to install all the packages, install all the dependencies, install all our libraries. # So basically it will remove the previous catch files. # Uh just go here inside components you can see a catch file have been created So it will ignore these catch files and build the dependencies from scratch. # It will not include those catch files.
RUN pip install --no-cache-dir -e . # 

## Expose only flask port # Uh, on which port your flask app is running.
EXPOSE 5000

## Run the Flask app # How we run the app you just write command python app slash application.py on the terminal and your app will get opened. So same thing we have written here also.
CMD ["python", "app/application.py"]

