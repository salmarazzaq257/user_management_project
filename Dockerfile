# # Use the official Python image
# # Use an official Python runtime as a parent image
# FROM python:3.11.2

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set the working directory
# WORKDIR /app

# # Copy the requirements file
# COPY requirements.txt /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code
# COPY . /app/

# # Expose the default Django port
# EXPOSE 8000

# # Command to run the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /project

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]