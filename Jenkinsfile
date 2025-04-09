pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'Sonarqube' // name from Jenkins > Configure System
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credrentials',
                    url: 'https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project'
            }
        }
    }

    stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh 'sonar-scanner' // this needs to be available on the Jenkins agent
                }
            }
    }
}
