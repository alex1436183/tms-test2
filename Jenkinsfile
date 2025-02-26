pipeline {
    agent { label 'minion' }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms_gr3.git'
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
                    sh "docker build --no-cache -f Dockerfile -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Start Docker Container and Run Tests') {
            agent {
                docker {
                    image "${IMAGE_NAME}"
                    label 'minion'
                    args "-d -p ${PORT}:${PORT} --name ${CONTAINER_NAME}"  // Запускаем контейнер
                    reuseNode true
                }
            }
            steps {
                parallel (
                    test_app_py: {
                        sh "docker exec ${CONTAINER_NAME} pytest tests/test_app.py --maxfail=1 --disable-warnings"
                    },
                    test_app2_py: {
                        sh "docker exec ${CONTAINER_NAME} pytest tests/test_app2.py --maxfail=1 --disable-warnings"
                    }
                )
            }
        }
    }

    post {
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
