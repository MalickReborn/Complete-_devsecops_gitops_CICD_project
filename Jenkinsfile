pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SonarToken')
        IMAGE_NAME = 'myFlaskForDevsecopsApp'
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

        stage('Docker Build') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
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
