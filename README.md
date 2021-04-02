# Introduction
This is a Django template meant to run on K8s

# Setup
## Prerequisites
1. a PSQL Managed DB
2. an S3 compatible space
3. a Digital Ocean K8s

## Config
### Reference
https://www.digitalocean.com/community/tutorials/how-to-deploy-a-scalable-and-secure-django-application-with-kubernetes

### Steps
Update the files in ./k8s to use the right app name (replace `estimer` by your own name, everywhere).

Then follow the steps in the ref doc. I only did it once and it wasn't an easy adventure. 
I'll certainely put more details here next time I go through this process.

