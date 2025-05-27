# Use an official Python runtime as a parent image
FROM python:3.12.9-alpine3.21

# Set the working directory in the container to /app
WORKDIR /app

# Copy the pyproject.toml and uv.lock files to the working directory
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install uv

# Install any dependencies specified in pyproject.toml and uv.lock
RUN uv sync 

# Copy the application code into the container
COPY src ./src
COPY README.md ./
# Make port 80 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]