# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
    
# Set up a working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY  requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . /app

# Expose the port that the FastAPI app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
