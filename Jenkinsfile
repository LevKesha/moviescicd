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

        stage('Run Docker Container & Execute Python Tests') {
            steps {
                script {
                    // 1) Start the container detached, mapping host 1993 → container 605
                    sh '''
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p ${HOST_PORT}:${CONTAINER_PORT} \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                    // Give the service a moment to boot
                    sh 'sleep 5'

                    // 2) Install test dependencies on the Jenkins agent
                    sh 'pip install -m --no-cache-dir -r requirements.txt requests python-dotenv'

                    // 3) Run the unified Python test suite
                    sh 'python test.py'
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
            echo "All tests passed and image cleaned up: ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Build, deploy or tests failed; see logs for details."
        }
    }
}
