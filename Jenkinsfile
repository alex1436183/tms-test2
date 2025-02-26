pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_gr3.git'  // Обновленный URL репозитория
        BRANCH_NAME = 'main'
        IMAGE_NAME = 'myapp-image'
        CONTAINER_NAME = 'myapp-container'
        PORT = '5050'
    }

    stages {
        stage('Clone repository') {
            agent {
                label 'minion'
            }
            steps {
                cleanWs()
                echo "Cloning repository from ${REPO_URL}"
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            agent {
                label 'minion'
            }
            steps {
                script {
                    echo "Building Docker image on Docker agent..."
                    sh """
                    docker build --no-cache -f Dockerfile -t ${IMAGE_NAME} .
                    echo "Docker image built successfully!"
                    """
                }
            }
        }

        stage('Start Docker Container') {
            agent {
                docker {
                    image "${IMAGE_NAME}"  // Используем локальный образ
                    args "-d -p ${PORT}:${PORT} --name ${CONTAINER_NAME}"  // Настройка портов и имени контейнера
                    reuseNode true  // Переиспользуем ноду
                    label 'minion'  // Запускать Docker агент на ноде 'minion'
                }
            }
            steps {
                script {
                    echo "Docker container started successfully!"
                }
            }
        }
    }
}
