pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Product Service') {
            steps {
                sh '''
                    cd product-service
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python -m pytest
                '''
            }
        }

        stage('Test Order Service') {
            steps {
                sh '''
                    cd order-service
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    python -m pytest
                '''
            }
        }

        stage('Build Product Image') {
            steps {
                sh '''
                    docker build \
                        -t cloudnative-shop-product:${BUILD_NUMBER} \
                        ./product-service
                '''
            }
        }

        stage('Trivy Product Scan') {
            steps{
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --exit-code 0 \
                      --format table \
                      cloudnative-shop-product:4
                '''
            }
        }

        stage('Build Order Image') {
            steps {
                sh '''
                    docker build \
                        -t cloudnative-shop-order:${BUILD_NUMBER} \
                        ./order-service
                '''
            }
        }

        stage('Trivy Order Scan'){
            steps{
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --exit-code 0 \
                      --format table \
                      cloudnative-shop-order:4
                '''
            }
        }
    }

    post {
        success {
            echo '🚀 CloudNativeShop CI PASSED!'
        }

        failure {
            echo '❌ CloudNativeShop CI FAILED!'
        }
    }
}