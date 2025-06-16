pipeline {
    agent any

    environment {
        IMAGE_NAME      = "movies-api"
        IMAGE_TAG       = "${BUILD_ID}"          //   "${env.BUILD_ID}" also works
        CONTAINER_NAME  = "movies-api-${BUILD_ID}"
        HOST_PORT       = "1993"
        CONTAINER_PORT  = "605"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
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
                    /* 1) start container (workspace mounted read-write) */
                    sh """
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -v ${WORKSPACE}:/app \
                          -p ${HOST_PORT}:${CONTAINER_PORT} \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                    sh 'sleep 5'

                    /* 2) install test-only deps  (space after install!) */
                    sh """
                        docker exec ${CONTAINER_NAME} \
                          python -m pip install --no-cache-dir requests python-dotenv
                    """

                    /* 3) run the unified test suite */
                    sh """
                        docker exec -e URL="http://localhost:${CONTAINER_PORT}/movie" \
                          ${CONTAINER_NAME} python /app/test.py
                    """
                }
            }
        }
    }

    post {
        always {
            sh "docker rm -f ${CONTAINER_NAME} || true"
            sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
        }
        success { echo "Tests inside container passed for ${IMAGE_NAME}:${IMAGE_TAG}" }
        failure { echo "Tests failed; see logs for details." }
    }
}
