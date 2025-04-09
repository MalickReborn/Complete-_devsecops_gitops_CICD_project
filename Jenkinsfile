pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'Sonarqube' // The name of the SonarQube server as configured in Jenkins
    }

    tools {
        // Assuming you have SonarQube scanner installed in Jenkins
        sonarQubeScanner 'Sonarqube' // Name of the SonarQube Scanner as configured in Jenkins
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
                script {
                    // Ensure the sonar.properties file is in place (usually in the root directory)
                    if (fileExists('sonar.properties')) {
                        echo "Using sonar.properties file from SCM"
                    } else {
                        error "sonar.properties file not found in the repository!"
                    }

                    // Start the SonarQube analysis
                    withSonarQubeEnv('SonarQube') {
                        // Run the SonarQube scanner
                        sh 'sonar-scanner'
                    }
                }
            }
        }
}
