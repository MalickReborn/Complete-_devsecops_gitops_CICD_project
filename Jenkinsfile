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
    }
}
