# DevSecOps/GitOps Pipeline

## Project Overview and Goals

  This project implements a DevSecOps pipeline based on GitOps principles to automate, secure, and optimize the software development lifecycle, from continuous integration (CI) to continuous deployment (CD). It is designed for a Python Flask application, forked from https://github.com/ubc/flask-sample-app.git. The main objectives are:  
Automation : Speed up delivery through automated testing, building, and deployments.  
Code quality : Ensure robust and maintainable code through static code quality analysis (bug detection, adherence to conventions, technical debt reduction).  
Security : Embed DevSecOps practices (vulnerability scans, compliance) at every step.  
GitOps : Manage configurations and deployments declaratively with Git as the single source of truth.  
Reliability : Guarantee stable and reproducible deployments in production for the Flask application.
Diagramme du pipeline


## Part 1 : Continuous Integration (CI)

###Prérequisite

  To set up the CI pipeline for the Python Flask application, the following tools and infrastructure are required:  
Infrastructure:  
CI VM: A virtual machine dedicated to installing CI tools (Jenkins, SonarQube, etc.).  
OS: Ubuntu 22.04 LTS.  
CPU: 4 vCPUs.  
RAM: 8 GB.  
Storage: 50 GB SSD.  
Network: Internet access to clone the repository, push to DockerHub, and interact with SonarQube.
Kubernetes Cluster: Required for the continuous deployment (CD) part. For this project, we chose to create two additional VMs on VMware: one for the master node and one for the worker node. Details will be provided in the CD part.
Tools:  
Git: Source code management via a forked GitHub repository.  
Jenkins: CI pipeline orchestration.  
Python 3.8+: Runtime environment for the Flask application.  
Python unittest: Framework for automated unit tests.  
pip-audit: Vulnerability analysis for Python dependencies.  
SonarQube: Static analysis to assess Python code quality (bugs, code smells, technical debt, test coverage).  
Docker: For building and testing Flask application images.  
Trivy: Security scanner for Docker images.  
DockerHub: Registry for storing Docker images after building.


### CI pipeline architecture

  The CI pipeline for the Flask application, orchestrated by Jenkins, follows these key steps:  
Code retrieval : Clone the Git repository forked from https://github.com/ubc/flask-sample-app.git.  
Static code quality analysis : Run SonarQube to detect bugs, code smells, and technical debt in Python code.  
Dependency analysis : Use pip-audit to identify vulnerabilities in Python dependencies (via requirements.txt).  
Unit tests : Execute automated tests with Python unittest to validate the application logic.  
Build : Create a Docker image for the Flask application.  
Security scan : Analyze the Docker image with Trivy to identify vulnerabilities.  
Publication : Push the validated image to DockerHub.
Quality thresholds (e.g., 80% test coverage, no critical bugs) and security thresholds (no critical vulnerabilities) are enforced to block progression if needed.

### Installation

  Configure the CI VM (Ubuntu 22.04 LTS, 4 vCPUs, 8 Go RAM, 50 Go SSD). / Set up the CI VM (Ubuntu 22.04 LTS, 4 vCPUs, 8 GB RAM, 50 GB SSD).
YOu can set a EC2 or any VM on any Cloud provider , but for this project i have set a local Vmware VM.

Install Git, Python 3.8+ / Install Git, Python 3.8+:
```
sudo apt update
sudo apt install -y git 
```

Docker:
https://docs.docker.com/engine/install/ubuntu/


Jenkins:
https://www.jenkins.io/doc/book/installing/linux/

Trivy:
```
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install -y trivy
```
Sonarqube:
You can use a docker container or installation from binaries ():
```
docker run -d --name sonar -p 9000:9000 sonarqube:lts-community
```
https://docs.sonarsource.com/sonarqube-server/10.4/setup-and-upgrade/install-the-server/introduction/

Pip-audit and Unittest:
Just add in the requirements.txt in addition to the flask minimum dependences the following ones : flask-testing and pip-audit


  In order to have jenkins working well with all these tools, you'll need to configure some plugins , server set up, and credentials.
The following plugins have to be install into jenkins: 
Plugin Name | Description
Pipeline (a.k.a. Workflow) Plugin | Core plugin for defining pipelines as code (Jenkinsfile)
GitHub + GitHub Branch Source + Git | Connects Jenkins with GitHub repositories
JUnit Plugin | Parses and displays results from unittest or pytest
SonarQube Scanner for Jenkins | Runs SonarQube analysis from Jenkins
Warnings Next Generation (optional for Trivy) | Use with trivy output to visualize security issues
Docker Pipeline + Docker Commons | Enables Docker build, tag, and push operations
Credentials | Stores secrets (GitHub token, DockerHub creds, etc.)


### Setup Pipeline

1. Creating the Pipeline in Jenkins with SCM
  This step configures a Jenkins pipeline to fetch the Jenkinsfile from the GitHub repository using Source Code Management (SCM), ensuring the pipeline is versioned with the code.
Steps
- Configure the pipeline in Jenkins.  
- Access Jenkins at http://<CI_VM_IP>:8080.  
- Click New Item, name it Flask-Pipeline, select Pipeline, and click OK.  
In the Pipeline section:  
- Select Pipeline script from SCM.  
- Choose Git as SCM.  
- Enter Repository URL: https://github.com/ubc/<your repo.git>.  
_ Specify Branch: <branch_name>.
-Set Script Path: Jenkinsfile.  
- If private, select Credential: github-token.
- Save and click Build Now to test.

2.Create a sonar project

  Since we have a code analysis section we then have to configure a SonarQube Project and Create sonar-project.properties file
A SonarQube project is set up to analyze Python code quality, with a sonar-project.properties file defining analysis parameters.
Steps
  
- Log in to SonarQube at http://<CI_VM_IP>:9000.  
- Click Create Project > Manually.  
- Set Project Key: flask-sample-app, Project Name: Flask Sample App.  
- Click Set Up.  
- Create sonar.properties in the project root in your SCM repo:
    This file will contains some information like project key mainly, but possibly other variables
- Add and push:  
  

3. Configuring the SonarQube Server in Jenkins with an Access Token

  The SonarQube server is integrated into Jenkins using a Secret Text credential (access token) for authentication.

Steps

  Configure SonarQube in Jenkins  
- In SonarQube, go to My Account > Security > Generate Tokens, create flask-sonar-token, and copy it.  

In Jenkins:  
- Go to Manage Jenkins > Manage Credentials > (global) > Add Credentials.  
- Set Kind: Secret Text, ID: sonar-token, Secret: paste token, Description: SonarQube Token.  
- Save.
- Go to Manage Jenkins > Configure System > SonarQube servers.  
- Click Add SonarQube:  
- Name: SonarQube.  
- Server URL: http://<CI_VM_IP>:9000.  
- Server authentication token: Select sonar-token.
- Save.

  
4. Creating the GitHub Credential with a Personal Access Token

  A Username with Password credential is created for GitHub, using a Personal Access Token (PAT) to securely clone the repository.
  
In GitHub, go to Settings > Developer settings > Personal access tokens > Generate new token:  
    Name: <githubtokenname>.  
    Scope: repo.  
- Copy the token.

In Jenkins:  
- Go to Manage Jenkins > Manage Credentials > (global) > Add Credentials.  
- Set Kind: Username with Password, ID: github-token.  
- Username: Your GitHub username.  
- Password: Paste the PAT.  
- Description: GitHub PAT.  
- Save.

5. Create the Dockerfile
  A Dockerfile is created to build the Docker image for the Flask application, specifying the environment, dependencies, and startup command.


### Usage

  Once configured, the pipeline is executed via Jenkins to validate, test, and build the Flask application.

Steps:
- Run and monitor the pipeline.  
-Access Jenkins at http://<CI_VM_IP>:8080.  
- Verify Flask-Pipeline uses the Jenkinsfile.  
- Click Build Now.  
- Check SonarQube reports at http://<CI_VM_IP>:9000.  
- Review pip-audit results.  
- Confirm the Docker image on DockerHub.  
- Fix and rerun if thresholds fail.
  
Security (DevSecOps)
  The pipeline embeds security checks at each step to block critical vulnerabilities:
Static Analysis: SonarQube detects bugs and potential vulnerabilities in Python code.
Dependency Scan: pip-audit identifies issues in requirements.txt.
Image Scan: Trivy checks Docker images for high/critical vulnerabilities.
Commands
Run security analyses.







