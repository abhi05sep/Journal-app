# Start with an official Python base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first (better for caching)
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Tell Docker the listen on port 5000
# Expose the port Flask will run on

EXPOSE 5000

# Run the Flask app
#Command to run when container starts
CMD ["python", "app.py"]
