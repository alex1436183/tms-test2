pipeline {
    agent {
        docker {
            image 'myapp-image'
            reuseNode true
        }
    }

    environment {
        REPO_URL = 'https://github.com/alex1436183/tms-test2.git'
        BRANCH_NAME = 'main'
    }

    stages {
        stage('Clone repository') {
            steps {
                cleanWs()
                echo "Cloning repository from ${REPO_URL}"
                git branch: "${BRANCH_NAME}", url: "${REPO_URL}"
            }
        }

        stage('Run Tests') {
            parallel {
                stage('Run test_app.py') {
                    steps {
                        sh '''
                        echo "Running test_app.py inside Docker container..."
                        pytest tests/test_app.py --maxfail=1 --disable-warnings
                        '''
                    }
                }
                stage('Run test_app2.py') {
                    steps {
                        sh '''
                        echo "Running test_app2.py inside Docker container..."
                        pytest tests/test_app2.py --maxfail=1 --disable-warnings
                        '''
                    }
                }
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
                mimeType: 'text/html',
            )
        }
        failure {
            echo 'Build failed!'
            emailext(
                subject: "Jenkins Job FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "<p>Jenkins job <b>${env.JOB_NAME}</b> (<b>${env.BUILD_NUMBER}</b>) завершился с ошибкой!</p>" +
                      "<p>Логи можно посмотреть тут: <a href='${env.BUILD_URL}'>${env.BUILD_URL}</a></p>",
                to: 'alex1436183@gmail.com',
                mimeType: 'text/html',
            )
        }
    }
}
