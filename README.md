# Nostr Serverless API

The Nostr Serverless API (NSA) project allows anyone with an AWS account to quickly and cheaply deploy and maintain their own Nostr API. Our goal is to make a Data Scientist's user experience working with Nostr data amazing.

## System Architecture
<details>

NSA's system architecture is outlined in **Figure 1** below. Specifically, this project consists of an AWS API Gateway that routes inbound API calls into an AWS Lambda function, which, in turn, spins up a Dockerized Flask application to process the API request. This architecture was chosen to minimize operating costs at low traffic volumes. We use an AWS Cloudformation Template to automate cloud service orchestration so that delpoying (and maintaining) the API is trivial.

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

Navigate to the directory containing the CloudFormation template (`cloudformationtemplate.yaml`) and run the following command, replacing `STACK_NAME` with your desired CloudFormation stack name and `DOCKER_IMAGE_URI` with the URI of the Docker image you just pushed:

   ```bash
   aws cloudformation deploy --template-file ./cloudformationtemplate.yaml --stack-name STACK_NAME --parameter-overrides DockerImageUri=DOCKER_IMAGE_URI --capabilities CAPABILITY_IAM
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
Full API documentation is available to Open API standards in this projects `openapi.yaml` file, and is also hosted on [Swagger Hub here](https://app.swaggerhub.com/apis/GARYJOKEEFFE/nostr-serverless_api/0.0.1). We also describe them here briefly.

Recall, you must first get your API's Base URL via the `describe-stacks` command (which can be found in Step 2 of the **Deploying the API** section). Once you have the base URL, you will be able to reach the following endpoints (with more endpoints to follow soon):

<details>
<summary>Verify the API is running correctly</summary>

**Description**: Publishing a "Running Nostr Serverless API" note from your account to verify everything is set up correctly

**Endpoint**: `/v0/verify`

**HTTP Method**: `POST`

**Objects to be added to the HTTP request**:
- relays = [LIST OF RELAYS OR STRING OF RELAY]
- private_key = [PRIVATE KEY IN NSEC FORMAT]

</details>

<details>
<summary>Send a Public Note</summary>

**Description**: Send a note from your account to a set of relays

**Endpoint**: `/v0/send/note`

**HTTP Method**: `POST`

**Objects to be added to the HTTP request**:
- relays = [LIST OF RELAYS OR STRING OF RELAY]
- private_key = [PRIVATE KEY IN NSEC FORMAT]
- text = [STRING OF YOUR NOTE's CONTENT]

</details>

<details>
<summary>Send a DM</summary>

**Description**: Send a DM from your account to someone elses over a set of relays

**Endpoint**: `/v0/send/dm`

**HTTP Method**: `POST`

**Objects to be added to the HTTP request**:
- relays = [LIST OF RELAYS OR STRING OF RELAY]
- sender_private_key = [PRIVATE KEY IN NSEC FORMAT]
- recipient_public_key = [PRIVATE KEY IN NPUB OR HEX FORMAT]
- text = [STRING OF YOUR NOTE's CONTENT]

</details>


<details>
<summary>Fetch Public Notes</summary>

**Description**: Fetch all notes that meet the filter criteria (filters to be added to request)

**Endpoint**: `/v0/fetch/notes`

**HTTP Method**: `POST`

**Objects that can be added to the HTTP request**:
- authors = [LIST OR STRING OF NPUB OR HEX FORMATTED AUTHOR[S]] 
- relays = [LIST OF RELAYS OR STRING OF RELAY]
- event_refs = [LIST OR STRING OF EVENT REFENENCES]
- pubkey_refs = [LIST OR STRING OF PUB KEY REFENENCES]
- since = [INTEGER OF INTERVAL START]
- from = [INTEGER OF INTERVAL TERMINATION]
- limit = [INTEGER OF #NOTES TO FETCH PER RELAY (Defaults to 2000)]

**Objects included in response**:
- Dictionary of noteID's wherein each object has the following properties:
   - time_created = [INTEGER OF WHEN NOTE WAS CREATED]
   - content = [STRING REPRESENTING NOTE's CONTENT]
   - author = [AUTHORS PUBLIC KEY IN HEX FORMAT]
   - signature = [STRING OF NOTE SIGNATURE]
   - tags = [JSON BLOB OF NOSTR NOTE TAG OBJECTS]

</details>

We will be pubilshing comprehensive examples in video and text format. Follow me on Nostr (npub10mgeum509kmlayzuvxhkl337zuh4x2knre8ak2uqhpcra80jdttqqvehf6) or on Twitter @garyjokeeffe to stay up-to-date. 

</details>