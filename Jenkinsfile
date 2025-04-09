pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout the SCM repository where the Jenkinsfile is stored
                checkout scm
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
                    withSonarQubeEnv('Sonarqube') {
                        // Run the SonarQube scanner
                        sh 'sonar-scanner'
                    }
                }
            }
        }
}
