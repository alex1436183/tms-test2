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
                echo "Building Docker image!"
                docker build -f Dockerfile -t ${IMAGE_NAME} .
                echo "Starting is docker container!"
                docker run -d -p 5050:5050 --name myapp-container myapp-image
                """
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
     stage('Cleanup') {
            steps {
                sh """
                echo "Cleaning up Docker containers myapp-container"
                docker rm -f myapp-container || true
                """
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
