# Use an official Python image as a base
FROM pytorch/pytorch:2.5.1-cuda11.8-cudnn9-runtime
#docker pull pytorch/pytorch:2.5.1-cuda11.8-cudnn9-runtime

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
