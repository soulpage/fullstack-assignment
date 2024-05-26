pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "saikrishna38721/backend"
        FRONTEND_IMAGE = "saikrishna38721/frontend"
        DOCKER_CREDENTIALS_ID = "dockerhub"  // Jenkins credential ID for Docker Hub
        SONAR_SCANNER_HOME = tool 'sonarqube'  // Name of SonarQube Scanner tool as configured in Jenkins
        SONAR_PROJECT_KEY = "demo"
        SONAR_HOST_URL = "http://34.174.208.0:9000"
        SONAR_AUTH_TOKEN = credentials('sonarqube')  // Jenkins credential ID for SonarQube token
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    // Checkout the repository
                    checkout scm
                }
            }
        }

        stage('Build Backend') {
            steps {
                script {
                    dir('backend') {
                        sh 'pip install -r dependencies.txt'
                        sh 'python manage.py collectstatic --noinput'
                    }
                }
            }
        }

        stage('Build Frontend') {
            steps {
                script {
                    dir('frontend') {
                        sh 'npm install'
                        sh 'npm run build'
                    }
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Run SonarQube analysis on backend
                    withSonarQubeEnv('SonarQube') {  // 'SonarQube' is the name of the SonarQube server configuration in Jenkins
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
                    // Build backend Docker image
                    docker.build("${BACKEND_IMAGE}", "./backend")
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    // Build frontend Docker image
                    docker.build("${FRONTEND_IMAGE}", "./frontend")
                }
            }
        }

        stage('Push Backend I
