pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms-test2.git'
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
                    image "${IMAGE_NAME}"
                    label 'minion' 
                    args "-d -p ${PORT}:${PORT} --name ${CONTAINER_NAME}" 
                    reuseNode true
                }
            }
            steps {
                script {
                    echo "Starting Docker container using local image..."
                }
            }
        }

        stage('Run Tests') {
            parallel {
                stage('Run test_app.py') {
                    agent {
                        docker {
                            image "${IMAGE_NAME}" 
                            label 'minion' 
                            reuseNode true 
                        }
                    }
                    steps {
                        script {
                            echo "Running test_app.py inside Docker container..."
                            sh """
                            docker exec ${CONTAINER_NAME} pytest tests/test_app.py --maxfail=1 --disable-warnings
                            """
                        }
                    }
                }
                stage('Run test_app2.py') {
                    agent {
                        docker {
                            image "${IMAGE_NAME}" 
                            label 'minion'
                            reuseNode true
                        }
                    }
                    steps {
                        script {
                            echo "Running test_app2.py inside Docker container..."
                            sh """
                            docker exec ${CONTAINER_NAME} pytest tests/test_app2.py --maxfail=1 --disable-warnings
                            """
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Build finished'
            script {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }
        success {
            echo 'Build was successful!'
            emailext(
                subject: "Jenkins Job SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "<p>Jenkins job <b>${env.JOB_NAME}</b> (<b>${env.BUILD_NUMBER}</b>) успешно выполнен!</p>" +
                      "<p>Проверить можно тут: <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>",
                to: 'alex1436183@gmail.com',
                mimeType: 'text/html'
            )
        }
        failure {
            echo 'Build failed!'
            emailext(
                subject: "Jenkins Job FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "<p>Jenkins job <b>${env.JOB_NAME}</b> (<b>${env.BUILD_NUMBER}</b>) завершился с ошибкой!</p>" +
                      "<p>Логи можно посмотреть тут: <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>",
                to: 'alex1436183@gmail.com',
                mimeType: 'text/html'
            )
        }
    }
}

