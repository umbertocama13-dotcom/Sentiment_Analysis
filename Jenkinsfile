
pipeline {
    agent any
 
    environment {
        IMAGE_NAME = "sentiment-api"
        CONTAINER_NAME = "sentiment-api-container"
        PORT = "8000"
    }
 
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/umbertocama13-dotcom/Sentiment_Analysis.git'
            }
        }
 
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    export CXXFLAGS="-include cstdint"
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }
 
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }
 
        stage('Smoke Test') {
            steps {
                script {
                    try {
                        sh "docker rm -f ${CONTAINER_NAME} || true"
                        sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:8000 ${IMAGE_NAME}:latest"

                        sh "curl --fail --retry 50 --retry-delay 10 --retry-connrefused http://localhost:${PORT}/docs"
                        sh "curl --fail http://localhost:${PORT}/metrics"
                        sh """
                            curl --fail -X POST http://localhost:${PORT}/predict \
                            -H "Content-Type: application/json" \
                            -d '{"review": "This product is amazing and works perfectly"}'
                        """
                    } finally {
                        sh "docker logs ${CONTAINER_NAME} || true"
                        sh "docker stop ${CONTAINER_NAME} || true"
                    }
                }
            }
        }
 
        stage('Deploy') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d --name ${CONTAINER_NAME} -p ${PORT}:8000 ${IMAGE_NAME}:latest"
            }
        }
    }
 
    post {
        success {
            echo 'Pipeline completata con successo'
        }
        failure {
            echo 'Pipeline fallita'
        }
        always {
            sh "docker ps -a"
        }
    }
}