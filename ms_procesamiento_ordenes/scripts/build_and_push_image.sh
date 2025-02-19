#!/bin/bash

# Set the image name and tag
AWS_ACCOUNT_ID="538430999815.dkr.ecr.us-east-1.amazonaws.com"
IMAGE_NAME="/curso-arquitectura-software/procesamiento-ordenes"  # 
IMAGE_TAG="latest" 

# Build the Docker image
echo "Building the Docker image..."
docker build -t ${AWS_ACCOUNT_ID}${IMAGE_NAME}:${IMAGE_TAG} .

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "Error: Docker image build failed."
  exit 1
fi

# Authenticate Docker to AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}

# Push the Docker to aws ECR
echo "Pushing the Docker image to AWS..."
docker push ${AWS_ACCOUNT_ID}${IMAGE_NAME}:${IMAGE_TAG}
