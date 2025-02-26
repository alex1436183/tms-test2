pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms-test2.git'  // URL репозитория
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
                    echo "Building Docker image..."
                    sh """
                    docker build --no-cache -f Dockerfile -t ${IMAGE_NAME} .
                    echo "Docker image built successfully!"
                    """
                }
            }
        }

        stage('Verify Docker Image') {
            agent {
                label 'minion'
            }
            steps {
                script {
                    echo "Checking if the Docker image exists locally..."
                    def imageExists = sh(script: "docker images -q ${IMAGE_NAME}", returnStdout: true).trim()
                    if (!imageExists) {
                        error "Docker image ${IMAGE_NAME} does not exist locally!"
                    } else {
                        echo "Docker image ${IMAGE_NAME} exists locally."
                    }
                }
            }
        }

        stage('Start Docker Container') {
            agent {
                docker {
                    image "${IMAGE_NAME}"  // Используем локальный образ
                    args "-d -p ${PORT}:${PORT} --name ${CONTAINER_NAME}"  // Настройка портов и имени контейнера
                    reuseNode true  // Переиспользуем ноду
                    label 'minion'  // Указываем, что агент должен быть на ноде 'minion'
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
