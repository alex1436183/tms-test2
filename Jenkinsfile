stage('Start Docker Container') {
            agent {
                docker {
                    image "${IMAGE_NAME}"
                    label 'minion'
                    args "-d -p ${PORT}:${PORT} --name ${CONTAINER_NAME}"
                    reuseNode true
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
