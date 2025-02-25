pipeline { 
    agent {
        docker {
            image 'myapp-image'
            label 'minion'  // Убедитесь, что у вас есть метка для выбора подходящего узла
            reuseNode true  // Переиспользование одного и того же узла, если необходимо
        }
    }
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
                script {
                    echo "Building Docker image on agent!"
                    // Выполнение команды на агенте для сборки Docker-образа
                    sh "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Start Docker Container') {
            steps {
                script {
                    echo "Starting docker container!"
                    docker.run(
                        "-d -p 5050:5050 --name ${CONTAINER_NAME} ${IMAGE_NAME}"
                    ) 
                }
            }
        }

        stage('Run Tests') {
            parallel {
                stage('Run test_app.py') {
                    steps {
                        script {
                            echo "Running test_app.py inside Docker container..."
                            sh "docker exec ${CONTAINER_NAME} pytes
