# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any needed dependencies
RUN pip install --no-cache-dir requests pandas

# Run pvr.py when the container launches
CMD ["python", "./pvr2.py"]
