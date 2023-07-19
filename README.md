# Nostr Serverless API

The Nostr Serverless API (NSA) project allows anyone with an AWS account to quickly and cheaply deploy and maintain their own Nostr API. Our goal is to make a Data Scientist's user experience working with Nostr data amazing.

## System Architecture
<details>

NSA's system architecture is outlined in **Figure 1** below. Specifically, this project consists of an AWS API Gateway that routes inbound API calls into an AWS Lambda function, which, in turn, spins up a Dockerized Flask application to process the API request. This architecture was chosen to optimize for operating costs at low traffic volumes. We use an AWS Cloudformation Template to abstract the cloud service configuration process from the user so that delpoying (and maintaining) the API is trivial.

<p align="center">
  <img src="https://github.com/garyokeeffe/NSA/blob/main/resources/NostrServerlessAPI.png?raw=true"><br>
  <b>Figure 1</b>: Nostr Serverless API System Architecture Diagram
</p>

</details>

## Deploying the API
<details>
<summary>Details:</summary>

### Prerequisites

- An AWS account
- Docker installed, running, and configured to build `arm64` images
- AWS CLI installed and configured with your AWS credentials.

### Steps:

<details>
<summary><b>Step 1: Build and push the Docker image</b> </summary>

Navigate to the directory containing the Dockerfile (`Dockerfile`) and run the following commands (replacing `ACCOUNT_ID` with your AWS account ID and `REGION` with your desired AWS region):

```bash
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com # Log into your AWS account (remember to replace REGION and ACCOUNT_ID)
aws ecr create-repository --repository-name nostr-app --region REGION # Create your ECR (if the ECR doesn't already exist)
docker build -t nostr-app . # Build the docker image giving it the name "nostr-app" 
docker tag nostr-app:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/nostr-app:latest # Tag your docker image with the ECR name
docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/nostr-app:latest # Push your docker image onto the ECR
```
</details>
<details>
<summary><b>Step 2: Deploy the CloudFormation stack</b></summary>

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
</details>

## Using the API

<details>
<summary>Details:</summary>

To do.

</details>