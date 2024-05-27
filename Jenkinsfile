pipeline {
    // Define the agent where the pipeline will run. 'any' means it can run on any available agent.
    agent any

    // Define environment variables to be used in the pipeline.
    environment {
        BACKEND_IMAGE = "saikrishna38721/backend"  // Docker image name for the backend
        FRONTEND_IMAGE = "saikrishna38721/frontend"  // Docker image name for the frontend
        DOCKER_CREDENTIALS_ID = "dockerhub"  // Jenkins credential ID for Docker Hub
        SONAR_SCANNER_HOME = tool 'sonarqube'  // Path to SonarQube Scanner tool as configured in Jenkins
        SONAR_PROJECT_KEY = "demo"  // SonarQube project key
        SONAR_HOST_URL = "http://34.174.208.0:9000"  // SonarQube server URL
        SONAR_AUTH_TOKEN = credentials('sonarqube')  // Jenkins credential ID for SonarQube authentication token
    }

    // Define the stages of the pipeline.
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // Checkout the code from the version control system (e.g., Git).
                    checkout scm
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    dir('backend') {
                        // Install the backend dependencies listed in the dependencies.txt file.
                        sh 'pip install -r dependencies.txt'
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    dir('frontend') {
                        // Install the frontend dependencies using npm.
                        sh 'npm install'
                        // Build the frontend project.
                        sh 'npm run build'
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Run SonarQube analysis on the backend code.
                    withSonarQubeEnv('sonarqube') {  // 'sonarqube' is the name of the SonarQube server configuration in Jenkins.
                        sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner " +
                           "-Dsonar.projectKey=${SONAR_PROJECT_KEY} " +
                           "-Dsonar.sources=./backend " +
                           "-Dsonar.host.url=${SONAR_HOST_URL} " +
                           "-Dsonar.login=${SONAR_AUTH_TOKEN}"
                    }
                }
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                script {
                    // Build the backend Docker image from the Dockerfile in the ./backend directory.
                    docker.build("${BACKEND_IMAGE}", "./backend")
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    // Build the frontend Docker image from the Dockerfile in the ./frontend directory.
                    docker.build("${FRONTEND_IMAGE}", "./frontend")
                }
            }
        }

        stage('Push Backend Image to Docker Hub') {
            steps {
                script {
                    // Push the backend Docker image to Docker Hub.
                    docker.withRegistry('https://index.docker.io/v1/', DOCKER_CREDENTIALS_ID) {
                        docker.image(BACKEND_IMAGE).

