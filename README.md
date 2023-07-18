# Nostr Serverless API

The Nostr Serverless API (NSA) project allows anyone with an AWS account to quickly and cheaply deploy and run their own Nostr API. We aim to give data scientists working with Nostr data, a superior user experience than what is enjoyed by data scientists working with social data from platforms such as Reddit, Twitter, Instagram, and Facebook.


NSA's system architecture is outlined Figure 1. Specifically, this project consists of an AWS API Gateway to that handles inbound traffic and sends it to an AWS Lambda function which runs a Dockerized Flask application to process the request and send back a response.

<p align="center">
  <img src="https://github.com/garyokeeffe/NSA/blob/main/resources/NostrServerlessAPI.png?raw=true"><br>
  Figure 1: Nostr Serverless API System Architecture Diagram
</p>

## Prerequisites

<details>
<summary>Details:</summary>

- An AWS account
- Docker installed
- AWS CLI installed and configured with your AWS credentials.

</details>

## Deployment
<details>
<summary>Details:</summary>

1. **Build and push the Docker image**:

    Make sure Docker is running on your machine. Then, navigate to the directory containing the Dockerfile and run the following commands, replacing ACCOUNT_ID with your AWS account ID and REGION with your AWS region:

   ```bash
    aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com
    docker build -t nostr-app .
    docker tag nostr-app:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/nostr-app:latest
    # The following command is only necessary if the ECR repository does not already exist.
    aws ecr create-repository --repository-name nostr-app --region REGION
    docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/nostr-app:latest
   ```

2. **Deploy the CloudFormation stack**:

   Navigate to the directory containing the CloudFormation template (`cloudformationtemplate.yaml`) and run the following command, replacing `STACK_NAME` with your desired CloudFormation stack name, `DOCKER_IMAGE_URI` with the URI of the Docker image you just pushed, and `NSEC_FORMATTED_PRIVATE_KEY` with a throwaway nostr account's private key:

   ```bash
   aws cloudformation deploy --template-file ./cloudformationtemplate.yaml --stack-name STACK_NAME --parameter-overrides DockerImageUri=DOCKER_IMAGE_URI NostrPrivateKey=NSEC_FORMATTED_PRIVATE_KEY --capabilities CAPABILITY_IAM --capabilities CAPABILITY_IAM
   ```

   After successful deployment, you can access the Flask application via the URL of the API Gateway that was created. You can find your API's base URL by running the following command after successful deployment:
```bash
aws cloudformation describe-stacks --stack-name STACK_NAME --query 'Stacks[].Outputs'
```
(remember to replace `STACK_NAME` with the name of your stack (which is defined when you ran `aws cloudformation deploy` in the last step).
</details>

## Usage

<details>
<summary>Details:</summary>

To do.

</details>