# Use an official lightweight Python image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Use the updated package names for system dependencies 
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libgomp1

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Tell Docker that the container listens on port 8000
EXPOSE 8000

# The command to run your application when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
