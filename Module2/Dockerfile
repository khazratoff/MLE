# Use Ubuntu as the base image
FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
    
# Set up a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY  requirements.txt utils.py /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY src /app/src


CMD ["python3","src/data_loader.py"]
