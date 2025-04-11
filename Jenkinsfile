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

        stage('Dependencies check'){
            steps {
                sh """
                pip-audit -r requirements.txt
                pip audit --fix
                """   
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
                    // Build the Docker image
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Scan Docker Image'){
            //Run trivy to scan the Docker image
            def trivyOutput = sh(script: "trivy image ${IMAGE_NAME}:latest", returnStdout: true).trim()

            //Display Trivy scan results
            println trivyOutput

            //Check if vulnerabilities were found
            if (trivyOutput.contains("Total: 0")) {
                echo "No vulnerabilities found in the Docker image."
            } else {
                echo "Vulnerabilities found in the Docker image."
                // further action can tbe taken based on our requirements
            }
        }

        stage('Docker Push') {
            steps {
                script {
                    // Log in to Docker Hub using credentials
                    withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        docker tag ${IMAGE_NAME}:latest ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
                        docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Clean up') {
            steps {
                sh 'docker rmi ${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest'  // Optionally clean up the image after pushing
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
