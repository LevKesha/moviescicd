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
                    // 1) Start the container with workspace mounted
                    sh '''
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -v ${WORKSPACE}:/app \
                          -p ${HOST_PORT}:${CONTAINER_PORT} \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                    sh 'sleep 5'

                    // 2) Install test dependencies inside the container
                    sh '''
                        docker exec ${CONTAINER_NAME} \
                          python -m pip install --no-cache-dir requests python-dotenv
                    '''

                    // 3) Run the unified test suite inside the container
                    sh '''
                        docker exec -e URL="http://localhost:${CONTAINER_PORT}/movie" ${CONTAINER_NAME} \
                          python /app/test.py
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                // Tear down container and image
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
