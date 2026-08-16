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

        stage('SonarQube Analysis'){
            steps{
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=cloudnative-shop \
                            -Dsonar.projectName=CloudNativeShop \
                            -Dsonar.sources=product-service,order-service \
                            -Dsonar.python.version=3.12
                        """ 
                    }
                }
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
                      cloudnative-shop-product:${BUILD_NUMBER}
                '''
            }
        }

        stage('Push Product Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

                        docker tag cloudnative-shop-product:${BUILD_NUMBER} \
                            $DOCKERHUB_USERNAME/cloudnative-shop-product:${BUILD_NUMBER}

                        docker tag cloudnative-shop-product:${BUILD_NUMBER} \
                            $DOCKERHUB_USERNAME/cloudnative-shop-product:latest

                        docker push \
                            $DOCKERHUB_USERNAME/cloudnative-shop-product:${BUILD_NUMBER}

                        docker push \
                            $DOCKERHUB_USERNAME/cloudnative-shop-product:latest

                        docker logout
                    '''
                }
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
                      cloudnative-shop-order:${BUILD_NUMBER}
                '''
            }
        }
        
        stage('Push Order Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'                    
                    )
                ])  {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin

                        docker tag cloudnative-shop-order:${BUILD_NUMBER} \
                            $DOCKERHUB_USERNAME/cloudnative-shop-order:${BUILD_NUMBER}

                        docker tag cloudnative-shop-order:${BUILD_NUMBER} \
                            $DOCKERHUB_USERNAME/cloudnative-shop-order:latest

                        docker push \
                            $DOCKERHUB_USERNAME/cloudnative-shop-order:${BUILD_NUMBER}

                        docker pushh \
                            $DOCKERHUB_USERNAME/cloudnative-shop-order:latest

                        docker logout
                    '''
                }
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