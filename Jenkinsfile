pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/sunkaraboinaaravind/network-devops-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t network-devops-dashboard .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f network-devops-dashboard-container || true'
		sh 'docker run -d --name network-devops-dashboard-container --network devops-net -p 5000:5000 network-devops-dashboard'
            }
        }

        stage('Run New Container') {
            steps {
                sh 'docker run -d --name network-devops-dashboard-container -p 5000:5000 network-devops-dashboard'
            }
        }
    }
}
