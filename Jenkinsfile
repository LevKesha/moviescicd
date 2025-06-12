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
                    // 1) Start the container detached, mapping host → container ports
                    sh '''
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p ${HOST_PORT}:${CONTAINER_PORT} \
                          ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                    sh 'sleep 5'

                    // 2) Install test dependencies on the Jenkins agent
                    sh 'python3 -m pip install --no-cache-dir requests python-dotenv'

                    // 3) Run Python test suite against the mapped host port
                    sh '''
                        export URL="http://localhost:${HOST_PORT}/movie" && \
                        python3 test.py
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                // Tear down the container and image
                sh "docker rm -f ${CONTAINER_NAME} || true"
                sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true"
            }
        }
        success {
            echo "Agent-side tests passed for ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Tests failed; see logs for details."
        }
    }
}
