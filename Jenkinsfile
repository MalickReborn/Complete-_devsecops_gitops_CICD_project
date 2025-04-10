pipeline {
    agent any
    environment{
        SONAR_TOKEN = credentials('SonarToken')
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-login',
                    url: 'https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project'
            }
        }

    stage('SonarQube Analysis') {
            steps {
                script {
                    // Start the SonarQube analysis
                    withSonarQubeEnv('Sonarqube') {
                        // Run the SonarQube scanner which will automatically use the sonar.properties file
                        sh '/opt/sonar-scanner/bin/sonar-scanner -Dsonar.login=${SONAR_TOKEN}'
                        echo 'SonarQube Analysis Completed'
                    }
                }
            }
        }
    }


    stage('Trivy - Vulnerability Scan') {
            steps {
                sh '''
                echo "Running Trivy Vulnerability Scan..."
                trivy fs --scanners vuln . --exit-code 0 --severity CRITICAL,HIGH --ignore-unfixed
                '''
            }
        }

        stage('Trivy - Secrets Scan') {
            steps {
                sh '''
                echo "Running Trivy Secrets Scan..."
                trivy fs --scanners secret . --exit-code 0
                '''
            }
        }

        stage('Trivy - Config Scan') {
            steps {
                sh '''
                echo "Running Trivy Config Scan..."
                trivy config . --exit-code 0 || echo "Check misconfigurations in the logs."
                '''
            }
        }




    
}
