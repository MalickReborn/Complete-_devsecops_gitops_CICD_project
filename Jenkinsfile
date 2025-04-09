pipeline {
    agent any

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
                withSonarQubeEnv('Sonarqube') {
                    sh 'sonar-scanner -Dsonar.projectKey=$SONAR_PROJECT_KEY'
                }
            }
        }
}
