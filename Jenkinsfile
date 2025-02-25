pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_gr3.git'
        BRANCH_NAME = 'main'
        IMAGE_NAME = 'myapp-image'
        CONTAINER_NAME = 'myapp-container'
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
                sh """
                echo "Building Docker image..."
                docker build -f Dockerfile -t ${IMAGE_NAME} .
                echo "Docker image built successfully!"
                """
            }
        }

        stage('Start or Reuse Container') {
            steps {
                script {
                    def containerExists = sh(script: "docker ps -a --format '{{.Names}}' | grep -w ${CONTAINER_NAME} || true", returnStdout: true).trim()
                    if (containerExists) {
                        echo "Container ${CONTAINER_NAME} already exists. Restarting..."
                        sh "docker start ${CONTAINER_NAME}"
                    } else {
                        echo "Creating and starting new container ${CONTAINER_NAME}..."
                        sh "docker run -d -p 5050:5050 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                    }
                }
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image 'myapp-image'
                    reuseNode true
                }
            }
            steps {
                parallel (
                    'Run test_app.py': {
                        sh """
                        echo "Running test_app.py inside Docker container..."
                        pytest tests/test_app.py --maxfail=1 --disable-warnings
                        """
                    },
                    'Run test_app2.py': {
                        sh """
                        echo "Running test_app2.py inside Docker container..."
                        pytest tests/test_app2.py --maxfail=1 --disable-warnings
                        """
                    }
                )
            }
        }
    }

    post {
        always {
            echo 'Build finished'
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
