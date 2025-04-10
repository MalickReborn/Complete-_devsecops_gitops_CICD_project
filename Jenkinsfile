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

        echo "Copie du projet dans /home pour le scan..."
        sudo cp -r /var/lib/jenkins/workspace/test /home/project-scan

        echo "Analyse des vulnérabilités avec Trivy dans /tmp/project-scan..."
        trivy fs --scanners vuln /home/project-scan --exit-code 0 --severity CRITICAL,HIGH --ignore-unfixed

        echo "Scan terminé."
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
