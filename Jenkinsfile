pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/MalickReborn/Complete-_devsecops_gitops_CICD_project'
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
                        // Run the SonarQube scanner which will automatically use the sonar.properties file
                        sh 'sonar-scanner'
                        echo 'SonarQube Analysis Completed'
                    }
                }
            }
        }
    }
}
