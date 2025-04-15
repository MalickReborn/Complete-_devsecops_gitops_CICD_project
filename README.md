Pipeline DevSecOps/GitOps
Présentation et objectifs globaux du projet
Français
Ce projet met en œuvre un pipeline DevSecOps basé sur les principes GitOps pour automatiser, sécuriser et optimiser le cycle de vie du développement logiciel, de l’intégration continue (CI) au déploiement continu (CD). Il est conçu pour une application Python Flask, basée sur un dépôt forké depuis https://github.com/ubc/flask-sample-app.git. Les objectifs principaux sont :  
Automatisation : Accélérer les livraisons grâce à des tests, builds et déploiements automatisés.  
Qualité du code : Garantir un code robuste et maintenable grâce à des analyses statiques de qualité de code (détection de bugs, respect des conventions, réduction de la dette technique).  
Sécurité : Intégrer des pratiques DevSecOps (scans de vulnérabilités, conformité) à chaque étape.  
GitOps : Gérer les configurations et déploiements de manière déclarative avec Git comme source unique de vérité.  
Fiabilité : Assurer des déploiements stables et reproductibles en production pour l’application Flask>
English
This project implements a DevSecOps pipeline based on GitOps principles to automate, secure, and optimize the software development lifecycle, from continuous integration (CI) to continuous deployment (CD). It is designed for a Python Flask application, forked from https://github.com/ubc/flask-sample-app.git. The main objectives are:  
Automation : Speed up delivery through automated testing, building, and deployments.  
Code quality : Ensure robust and maintainable code through static code quality analysis (bug detection, adherence to conventions, technical debt reduction).  
Security : Embed DevSecOps practices (vulnerability scans, compliance) at every step.  
GitOps : Manage configurations and deployments declaratively with Git as the single source of truth.  
Reliability : Guarantee stable and reproducible deployments in production for the Flask application.
Diagramme du pipeline
Français
Diagramme à venir : Une représentation visuelle du pipeline DevSecOps/GitOps, couvrant les étapes de l’intégration continue (CI) et du déploiement continu (CD) pour l’application Python Flask, sera ajoutée ici une fois fournie.
English
Diagram to come: A visual representation of the DevSecOps/GitOps pipeline, covering the stages of continuous integration (CI) and continuous deployment (CD) for the Python Flask application, will be added here once provided.
Partie 1 : Continuous Integration (CI)
Prérequis
Français
Pour configurer le pipeline CI pour l’application Python Flask, les outils suivants et l’infrastructure suivante sont nécessaires :  
Infrastructure :  
VM CI : Une machine virtuelle dédiée pour installer les outils CI (Jenkins, SonarQube, etc.).  
OS : Ubuntu 22.04 LTS.  
CPU : 4 vCPUs.  
RAM : 8 Go.  
Stockage : 50 Go SSD.  
Réseau : Accès Internet pour cloner le dépôt, pousser vers DockerHub, et interagir avec SonarQube.
Cluster Kubernetes : Requis pour la partie déploiement continu (CD). Pour ce projet, nous avons choisi de créer deux VMs supplémentaires sur VMware : une pour le nœud maître et une pour le nœud worker. Les détails seront fournis dans la partie CD.
Outils :  
Git : Gestion du code source via un dépôt forké sur GitHub.  
Jenkins : Orchestration du pipeline CI.  
Python 3.8+ : Environnement d’exécution pour l’application Flask.  
Python unittest : Framework pour les tests unitaires automatisés.  
pip-audit : Analyse des vulnérabilités des dépendances Python.  
SonarQube : Analyse statique pour évaluer la qualité du code Python (bugs, code smells, dette technique, couverture de tests).  
Docker : Pour construire et tester les images de l’application Flask.  
Trivy : Scanner de sécurité pour les images Docker.  
DockerHub : Registre pour stocker les images Docker après le build.
English
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
Architecture du pipeline CI
Français
Le pipeline CI pour l’application Flask, orchestré par Jenkins, suit ces étapes clés :  
Récupération du code : Clone du dépôt Git forké depuis https://github.com/ubc/flask-sample-app.git.  
Analyse statique de qualité de code : Exécution de SonarQube pour détecter bugs, code smells et dette technique dans le code Python.  
Analyse des dépendances : Utilisation de pip-audit pour identifier les vulnérabilités dans les dépendances Python (via requirements.txt).  
Tests unitaires : Exécution des tests automatisés avec Python unittest pour valider la logique de l’application.  
Build : Création d’une image Docker pour l’application Flask.  
Scan de sécurité : Analyse de l’image Docker avec Trivy pour identifier les vulnérabilités.  
Publication : Push de l’image validée vers DockerHub.
Les seuils de qualité (ex. : 80 % de couverture de tests, aucun bug critique) et de sécurité (aucune vulnérabilité critique) sont appliqués pour bloquer la progression si nécessaire.
English
The CI pipeline for the Flask application, orchestrated by Jenkins, follows these key steps:  
Code retrieval : Clone the Git repository forked from https://github.com/ubc/flask-sample-app.git.  
Static code quality analysis : Run SonarQube to detect bugs, code smells, and technical debt in Python code.  
Dependency analysis : Use pip-audit to identify vulnerabilities in Python dependencies (via requirements.txt).  
Unit tests : Execute automated tests with Python unittest to validate the application logic.  
Build : Create a Docker image for the Flask application.  
Security scan : Analyze the Docker image with Trivy to identify vulnerabilities.  
Publication : Push the validated image to DockerHub.
Quality thresholds (e.g., 80% test coverage, no critical bugs) and security thresholds (no critical vulnerabilities) are enforced to block progression if needed.

Installation

Configurez la VM CI (Ubuntu 22.04 LTS, 4 vCPUs, 8 Go RAM, 50 Go SSD). / Set up the CI VM (Ubuntu 22.04 LTS, 4 vCPUs, 8 GB RAM, 50 GB SSD).
Installez Git, Python 3.8+ / Install Git, Python 3.8+:
``
sudo apt update
sudo apt install -y git 
``

Docker:
https://docs.docker.com/engine/install/ubuntu/


Jenkins:
https://www.jenkins.io/doc/book/installing/linux/

Trivy:
``
sudo apt-get install -y wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install -y trivy
``
Sonarqube:
You can use a docker container or installation from binaries ():
``
docker run -d --name sonar -p 9000:9000 sonarqube:lts-community
``
https://docs.sonarsource.com/sonarqube-server/10.4/setup-and-upgrade/install-the-server/introduction/

Pip-audit and Unittest:
Just add in the requirements.txt in addition to the flask minimum dependences the following ones : flask-testing and pip-audit


In order to have jenkins work well with all these tools, you'll need to configure some plugins , server set up, and credentials.

the following plugins have to be added to jenkins: 
Plugin Name | Description
Pipeline (a.k.a. Workflow) Plugin | Core plugin for defining pipelines as code (Jenkinsfile)
GitHub + GitHub Branch Source + Git | Connects Jenkins with GitHub repositories
JUnit Plugin | Parses and displays results from unittest or pytest
SonarQube Scanner for Jenkins | Runs SonarQube analysis from Jenkins
Warnings Next Generation (optional for Trivy) | Use with trivy output to visualize security issues
Docker Pipeline + Docker Commons | Enables Docker build, tag, and push operations
Credentials | Stores secrets (GitHub token, DockerHub creds, etc.)


Setup Pipeline
1. Creating the Pipeline in Jenkins with SCM
This step configures a Jenkins pipeline to fetch the Jenkinsfile from the GitHub repository using Source Code Management (SCM), ensuring the pipeline is versioned with the code.
Commands
Configure the pipeline in Jenkins.  
Access Jenkins at http://<CI_VM_IP>:8080.  
Click New Item, name it Flask-Pipeline, select Pipeline, and click OK.  
In the Pipeline section:  
Select Pipeline script from SCM.  
Choose Git as SCM.  
Enter Repository URL: https://github.com/ubc/flask-sample-app.git.  
Specify Branch: main.  
Set Script Path: Jenkinsfile.  
If private, select Credential: github-token (see step 4).
Save and click Build Now.
2. Configuring a SonarQube Project and Creating sonar.properties
A SonarQube project is set up to analyze Python code quality, with a sonar.properties file defining analysis parameters.
Commands
Create the SonarQube project and sonar.properties file.  
Log in to SonarQube at http://<CI_VM_IP>:9000.  
Click Create Project > Manually.  
Set Project Key: flask-sample-app, Project Name: Flask Sample App.  
Click Set Up.  
Create sonar.properties in the project root:  
properties

sonar.projectKey=flask-sample-app
sonar.projectName=Flask Sample App
sonar.projectVersion=1.0
sonar.sources=.
sonar.language=py
sonar.sourceEncoding=UTF-8
sonar.host.url=http://<CI_VM_IP>:9000
Add and push:  
bash

git add sonar.properties
git commit -m "Add sonar.properties"
git push origin main
3. Configuring the SonarQube Server in Jenkins with an Access Token
The SonarQube server is integrated into Jenkins using a Secret Text credential (access token) for authentication.
Commands
Configure SonarQube in Jenkins.  
In SonarQube, go to My Account > Security > Generate Tokens, create flask-sonar-token, and copy it.  
In Jenkins:  
Go to Manage Jenkins > Manage Credentials > (global) > Add Credentials.  
Set Kind: Secret Text, ID: sonar-token, Secret: paste token, Description: SonarQube Token.  
Save.
Go to Manage Jenkins > Configure System > SonarQube servers.  
Click Add SonarQube:  
Name: SonarQube.  
Server URL: http://<CI_VM_IP>:9000.  
Server authentication token: Select sonar-token.
Save.
4. Creating the GitHub Credential with a Personal Access Token
A Username with Password credential is created for GitHub, using a Personal Access Token (PAT) to securely clone the repository.
Commands
Create the GitHub credential.  
In GitHub, go to Settings > Developer settings > Personal access tokens > Generate new token:  
Name: jenkins-flask-access.  
Scope: repo.  
Copy the token.
In Jenkins:  
Go to Manage Jenkins > Manage Credentials > (global) > Add Credentials.  
Set Kind: Username with Password, ID: github-token.  
Username: Your GitHub username.  
Password: Paste the PAT.  
Description: GitHub PAT.  
Save.
5. Creating the Dockerfile
A Dockerfile is created to build the Docker image for the Flask application, specifying the environment, dependencies, and startup command.
Commands
Create the Dockerfile.  
Create Dockerfile in the project root:  
dockerfile

FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
Add and push:  
bash

git add Dockerfile
git commit -m "Add Dockerfile"
git push origin main
Usage
Once configured, the pipeline is executed via Jenkins to validate, test, and build the Flask application.
Commands
Run and monitor the pipeline.  
Access Jenkins at http://<CI_VM_IP>:8080.  
Verify Flask-Pipeline uses the Jenkinsfile.  
Click Build Now.  
Check SonarQube reports at http://<CI_VM_IP>:9000.  
Review pip-audit results.  
Confirm the Docker image on DockerHub.  
Fix and rerun if thresholds fail.
Security (DevSecOps)
The pipeline embeds security checks at each step to block critical vulnerabilities:
Static Analysis: SonarQube detects bugs and potential vulnerabilities in Python code.
Dependency Scan: pip-audit identifies issues in requirements.txt.
Image Scan: Trivy checks Docker images for high/critical vulnerabilities.
Commands
Run security analyses.







