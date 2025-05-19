#!/bin/bash

# Configuration
AWS_REGION="us-east-1"
ECR_REPOSITORY_NAME="exercise-app"
CLUSTER_NAME="exercise-app-cluster"
SERVICE_NAME="exercise-app-service"

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Create ECR repository if it doesn't exist
aws ecr describe-repositories --repository-names $ECR_REPOSITORY_NAME --region $AWS_REGION || \
    aws ecr create-repository --repository-name $ECR_REPOSITORY_NAME --region $AWS_REGION

# Build and push Docker images
docker build -t $ECR_REPOSITORY_NAME-backend -f app/backend/Dockerfile .
docker build -t $ECR_REPOSITORY_NAME-frontend -f app/frontend/Dockerfile .

docker tag $ECR_REPOSITORY_NAME-backend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME-backend:latest
docker tag $ECR_REPOSITORY_NAME-frontend:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME-frontend:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME-backend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY_NAME-frontend:latest

# Update task definition
envsubst < aws/task-definition.json > aws/task-definition-updated.json
aws ecs register-task-definition --cli-input-json file://aws/task-definition-updated.json

# Update service
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --task-definition exercise-app --force-new-deployment 