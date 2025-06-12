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
                    // Build the Docker image with a unique tag
                    dockerImage = docker.build("${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Start the container detached, mapping host 1993 → container 605
                    sh """
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p ${HOST_PORT}:${CONTAINER_PORT} \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                    // Give the service a moment to boot
                    sh 'sleep 5'
                    // Smoke-test the GET /movie endpoint
                    sh """
                        if ! curl -f http://localhost:${HOST_PORT}/movie; then
                            echo "API did not respond correctly on port ${HOST_PORT}"
                            exit 1
                        fi
                    """
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
            echo "Build & run succeeded: ${IMAGE_NAME}:${IMAGE_TAG} on host port ${HOST_PORT}"
        }
        failure {
            echo "Build or run failed; see above for details."
        }
    }
}
