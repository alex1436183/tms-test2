pipeline {
    agent { label 'minion' }  // Устанавливаем агент для всего пайплайна

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_gr3.git'  // URL репозитория
        BRANCH_NAME = 'main'
        IMAGE_NAME = 'myapp-image'
        CONTAINER_NAME = 'myapp-container'
        PORT = '5050'
    }

    stages {
        stage('Clone repository') {
            steps {
                cleanWs()
                echo "Cloning repository from ${REPO_URL}"
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
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
                    image "${IMAGE_NAME}"  // Используем созданный образ
                    label 'minion'  // Агент с меткой minion
                    args "-d -p ${PORT}:${PORT} --name ${CONTAINER_NAME}"  // Настроим порты и имя контейнера
                    reuseNode true  // Переиспользуем ноду
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
