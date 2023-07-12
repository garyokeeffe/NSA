# Nostr Serverless API
A Nostr Serverless API


## Setting up the Project
We have included several placeholder variables in this git repo for you to replace with your own variables. Configuration of these variables is done in three phases: ** Step 1. Configure and Build the Docker Image**, **Step 2. Configure AWS resources via GUI**, **Step 3. Configure and Run the Cloudformation Template**.

### Step 1. Configure and Build the Docker Image
The placeholder `NOSTR_PRIVATE_KEY` variable on line 25 of the `Dockerfile` should be replaced with your user's private key (in nsec format).
