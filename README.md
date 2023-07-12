# Nostr Serverless API

This repository contains a Dockerized Flask application and an AWS CloudFormation template to deploy the application to AWS Lambda and expose it via Amazon API Gateway.

## Prerequisites

- An AWS account
- Docker installed
- AWS CLI installed and configured with your AWS credentials. The IAM user that is used to run the AWS CLI commands (let's call this the "CLI IAM user") needs permissions to create and manage AWS Lambda functions, API Gateway APIs, and IAM roles and policies. These permissions can be granted by attaching the `AdministratorAccess` policy to the user, which provides full access to AWS services and resources. However, for production systems, you should follow the principle of least privilege and only grant the necessary permissions.

## Setting up the IAM Role for the Lambda Function

This IAM role is separate from the CLI IAM user mentioned in the prerequisites. The Lambda function needs to assume this role when it's invoked to have the necessary permissions.

1. **Log in to the AWS Management Console and open the IAM service**.
2. **Create a new role**:
   - Click on "Roles" in the left-hand menu and then click on "Create role".
   - Select "AWS service" for the type of trusted entity and "Lambda" for the service that will use this role, then click "Next: Permissions".
3. **Attach the necessary policies**:
   - In the "Attach permissions policies" page, search for and select the `AWSLambdaExecute` policy. This managed policy provides the permissions necessary for a Lambda function to execute (including sending logs to CloudWatch Logs).
   - If your Lambda function needs to access other AWS resources (like an S3 bucket), you should also attach policies that grant permissions to those resources (however this is not included in the scope of this repo yet and so should not be necessary).
   - Click "Next: Tags".
4. **(Optional) Add tags**:
   - Best practice recommends you add tags to any AWS resource you have configured. You can add tags to your role (key-value pairs) for easier management, then click "Next: Review".
5. **Review and create the role**:
   - Give your role a name and (optional but recommended) description, review the permissions and tags, and then click "Create role".

Your IAM role for the Lambda function is now set up and ready to be used. You can find the ARN of the role in the role's summary page, and it's what you should use for `IAM_ROLE_ARN` when deploying the CloudFormation stack.

## Deployment

1. **Build and push the Docker image**:

   Navigate to the directory containing the Dockerfile and run the following commands, replacing `ACCOUNT_ID` with your AWS account ID and `REGION` with your AWS region:

   ```bash
   $(aws ecr get-login --no-include-email --region REGION)
   docker build -t nostr-app .
   docker tag nostr-app:latest ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/nostr-app:latest
   docker push ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/nostr-app:latest
   ```

2. **Deploy the CloudFormation stack**:

   Navigate to the directory containing the CloudFormation template (`cloudformationtemplate.yaml`) and run the following command, replacing `STACK_NAME` with your desired CloudFormation stack name, `DOCKER_IMAGE_URI` with the URI of the Docker image you just pushed, and `IAM_ROLE_ARN` with the ARN of the IAM role that you created:

   ```bash
   aws cloudformation deploy --template-file ./cloudformationtemplate.yaml --stack-name STACK_NAME --parameter-overrides DockerImageUri=DOCKER_IMAGE_URI LambdaExecutionRole=IAM_ROLE_ARN
   ```

## Usage

After successful deployment, you can access the Flask application via the URL of the API Gateway that was created. You can find this URL in the Outputs section of the CloudFormation stack in the AWS Management Console. Hit the `/verify` endpoint to verify that the Nostr Serverless API has been successfully configured. If you need to confirm your API gateway URL, run the following command:
```bash
aws cloudformation describe-stacks --stack-name STACK_NAME --query 'Stacks[].Outputs'
```
(remember to replace `STACK_NAME` with the name of your stack (which is defined in the parameter section of your `cloudformationtemplate.yaml` file).