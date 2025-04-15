# DevSecOps/GitOps Pipeline

## Project Overview and Goals

  This project implements a DevSecOps pipeline based on GitOps principles to automate, secure, and optimize the software development lifecycle, from continuous integration (CI) to continuous deployment (CD). It is designed for a Python Flask application, forked from https://github.com/ubc/flask-sample-app.git. The main objectives are:  
Automation : Speed up delivery through automated testing, building, and deployments.  
Code quality : Ensure robust and maintainable code through static code quality analysis (bug detection, adherence to conventions, technical debt reduction).  
Security : Embed DevSecOps practices (vulnerability scans, compliance) at every step.  
GitOps : Manage configurations and deployments declaratively with Git as the single source of truth.  
Reliability : Guarantee stable and reproducible deployments in production for the Flask application.

Here you can see the global project pipeline diagram
[![pipeline-diagram.png](https://i.postimg.cc/9MvpYrTk/pipeline-diagram.png)](https://postimg.cc/BLBHqZm5)


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
[![jenkins-installed.png](https://i.postimg.cc/SRF6zHbF/jenkins-installed.png)](https://postimg.cc/wy2yCfB0)

Trivy:
```
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install -y trivy
```
[![trivy-installed.png](https://i.postimg.cc/L4LBM4jH/trivy-installed.png)](https://postimg.cc/G93sFCMN)

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

#### 1. Creating the Pipeline in Jenkins with SCM
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

#### 2.Create a sonar project

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
  [![sonarcreatepage.png](https://i.postimg.cc/zf4W94Bb/sonarcreatepage.png)](https://postimg.cc/f3jJd2YD)

  [![projet-sonarcreation.png](https://i.postimg.cc/KjDM3z5B/projet-sonarcreation.png)](https://postimg.cc/XBXJTnmY)

#### 3. Configuring the SonarQube Server in Jenkins with an Access Token

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
  [![sonarserverjenkins.png](https://i.postimg.cc/QCH2H9Dn/sonarserverjenkins.png)](https://postimg.cc/SYbTPKJW)

  
#### 4. Creating the GitHub Credential with a Personal Access Token

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

#### 5. Create the Dockerfile
  A Dockerfile is created to build the Docker image for the Flask application, specifying the environment, dependencies, and startup command.
the exemple
[Our simple Dockerfile example](https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project/blob/main/Dockerfile)

#### 6. Write your Jenkinsfile that will integrate all the steps within as we did in this project
[Our simple Jenkinsfile example](https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project/blob/main/Jenkinsfile)


### 6. Usage

  Once configured, the pipeline is executed via Jenkins to validate, test, and build the Flask application.

Steps:
- Run and monitor the pipeline.  
- Access Jenkins at http://<CI_VM_IP>:8080.  
- Verify your Flask Pipeline uses the Jenkinsfile.  
- Click Build Now.
- check the unit tests success
  [![Screenshot-from-2025-04-15-23-07-30.png](https://i.postimg.cc/kGPn3vKv/Screenshot-from-2025-04-15-23-07-30.png)](https://postimg.cc/47wCpt8Y)
- Review pip-audit results.
  [![PIP-AUDIT-ANALYSED.png](https://i.postimg.cc/Y9f6Ybrv/PIP-AUDIT-ANALYSED.png)](https://postimg.cc/S2RYpLz4)  
- Check SonarQube reports at http://<CI_VM_IP>:9000.
  [![soanr-analysis-done.png](https://i.postimg.cc/KY7kHjdV/soanr-analysis-done.png)](https://postimg.cc/94MQ4mXt)  
- Ensure that the container image has been build and scanned from vulnerabilities
  [![trivy-image-scanned.png](https://i.postimg.cc/jjTCPKLh/trivy-image-scanned.png)](https://postimg.cc/3kLKQsjy)
  [![TRIVY-IMAGE-SCANNED2.png](https://i.postimg.cc/CK454t8p/TRIVY-IMAGE-SCANNED2.png)](https://postimg.cc/hJfKD2M2)
- Confirm the Docker image on DockerHub.
  [![docker-image-pushed.png](https://i.postimg.cc/fLxK5MKT/docker-image-pushed.png)](https://postimg.cc/zbGKGZ69)  
- Fix and rerun if thresholds fail.
  [![pipeline-success.png](https://i.postimg.cc/Kv5WxDtv/pipeline-success.png)](https://postimg.cc/D886csCt)
  
#### 7. about Security (DevSecOps)
  The pipeline embeds security checks at each step to block critical vulnerabilities:
Static Analysis: SonarQube detects bugs and potential vulnerabilities in Python code.
Dependency Scan: pip-audit identifies issues in requirements.txt.
Image Scan: Trivy checks Docker images for high/critical vulnerabilities.
Commands
Run security analyses.


#### 8. Create the webhook to autonate the run of pipeline
   To create a webhook for Jenkins in GitHub, first ensure your Jenkins server is publicly accessible (or at least reachable from GitHub) and that you have the GitHub plugin installed in Jenkins. Then, in Jenkins, go to your job configuration, check **"GitHub Project"**, and enter your GitHub repository URL. Under **"Source Code Management"**, choose **Git** and input your repository URL and credentials if necessary. Next, go to your GitHub repository, click on **Settings** > **Webhooks** > **Add webhook**. In the **Payload URL**, enter your Jenkins webhook endpoint, usually `http://<your-jenkins-domain>/github-webhook/`. Set the **Content type** to `application/json`, and choose to send **Just the push event** (or more, depending on your needs). Finally, click **Add webhook**. Now, every time you push code to the repository, GitHub will trigger a build in Jenkins.

We conclude the first part of the project here. The second part related to the Gitops and Continuous Deployment will be available on the second config repository since we want to respect usages a goot habit avoinding to have the code and configuration materials within a sole repository.
the config phase is available [here](https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project_gitops_config.git).







