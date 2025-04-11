pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('SonarToken')
        IMAGE_NAME = 'flaskfordevsecops'
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub_credentials')
        DOCKER_HUB_USERNAME = 'malickguess'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-login',
                    url: 'https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project'
            }
        }

        stage('Setup & Install') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                export PIP_CACHE_DIR=$HOME/.cache/pip 
                pip install --upgrade pip
                pip install --cache-dir=$PIP_CACHE_DIR -r requirements.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python -m unittest discover
                '''
            }
        }

        stage('Dependencies Check') {
            steps {
                sh '''
                . venv/bin/activate
                export PIP_CACHE_DIR=$HOME/.cache/pip
                pip-audit -r requirements.txt || true
                pip-audit --fix || true
                '''
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

        stage('Docker Build') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Scan Docker Image') {
            steps {
                script {
                    def trivyOutput = sh(script: "trivy image ${IMAGE_NAME}:latest", returnStdout: true).trim()
                    println trivyOutput

                    if (trivyOutput.contains("Total: 0")) {
                        echo "No vulnerabilities found in the Docker image."
                    } else {
                        echo "Vulnerabilities found in the Docker image."
                    }
                }
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh """
                        echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin
                        docker tag ${IMAGE_NAME}:latest \$DOCKER_USERNAME/${IMAGE_NAME}:latest
                        docker push \$DOCKER_USERNAME/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }

        stage('Clean Up') {
            steps {
                sh '''
                docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest || true
                rm -rf venv
                rm -rf $HOME/.cache/pip
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
