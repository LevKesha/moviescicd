pipeline {
    agent any

    environment {
        IMAGE_NAME      = "movies-api"
        IMAGE_TAG       = "${env.BUILD_ID}"
        CONTAINER_NAME  = "movies-api-${env.BUILD_ID}"
        HOST_PORT       = "1993"
        CONTAINER_PORT  = "605"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Run Docker Container & Execute Python Tests') {
            steps {
                script {
                    // 1) Start the container
                    sh '''
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p ${HOST_PORT}:${CONTAINER_PORT} \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                    sh 'sleep 5'

                    // 2) Install test dependencies on the Jenkins agent via python -m pip
                    sh 'python3 -m pip install --no-cache-dir -r requirements.txt requests python-dotenv'

                    // 3) Run the unified Python test suite locally against the container API
                    sh 'python3 test.py'
                }
            }
        }
        }
    }

    post {
        always {
            script {
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
            }
        }
        success {
            echo "Tests inside container passed for ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Tests failed; see logs for details."
        }
    }
}
