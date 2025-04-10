pipeline {
    agent any

    environment {
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
                    withSonarQubeEnv('Sonarqube') {
                        sh """
                            /opt/sonar-scanner/bin/sonar-scanner \
                            -Dsonar.login=$SONAR_TOKEN
                        """
                        echo 'SonarQube Analysis Completed'
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

        stage('Unit Tests') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                python -m unittest discover
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        failure {
            echo 'Something went wrong. Check above logs for details.'
        }
    }
}
