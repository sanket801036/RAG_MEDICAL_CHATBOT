pipeline {
    agent any

    environment {
        AWS_REGION = 'eu-north-1'
        ECR_REPO = 'my-repo'
        IMAGE_TAG = 'latest'
        SERVICE_NAME = 'llmops-medical-service'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/sanket801036/RAG_MEDICAL_CHATBOT.git']])
                    
                }
            }
        }

        stage('Build, Scan, and Push Docker Image to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
                    script {
                        def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
                        def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
                        def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

                        sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ecrUrl}
                        docker build -t ${env.ECR_REPO}:${IMAGE_TAG} .

                        # Trivy Scan with increased timeout
                        echo "Running Trivy scan with 30-minute timeout..."
                        trivy image --timeout 30m --severity HIGH,CRITICAL --format json -o trivy-report.json ${env.ECR_REPO}:${IMAGE_TAG} || true

                        docker tag ${env.ECR_REPO}:${IMAGE_TAG} ${imageFullTag}
                        
                        # Push with retry logic
                        set +e
                        MAX_RETRIES=3
                        RETRY_COUNT=0
                        
                        while [ \$RETRY_COUNT -lt \$MAX_RETRIES ]; do
                          docker push ${imageFullTag}
                          if [ \$? -eq 0 ]; then
                            echo "✅ Push successful"
                            break
                          else
                            RETRY_COUNT=\$((RETRY_COUNT+1))
                            echo "⚠️ Push failed, retrying... (\$RETRY_COUNT/\$MAX_RETRIES)"
                            sleep 30
                          fi
                        done
                        
                        if [ \$RETRY_COUNT -eq \$MAX_RETRIES ]; then
                          echo "❌ Push failed after \$MAX_RETRIES attempts"
                          exit 1
                        fi
                        """

                        archiveArtifacts artifacts: 'trivy-report.json', allowEmptyArchive: true
                    }
                }
            }
        }

        //  stage('Deploy to AWS App Runner') {
        //     steps {
        //         withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-token']]) {
        //             script {
        //                 def accountId = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
        //                 def ecrUrl = "${accountId}.dkr.ecr.${env.AWS_REGION}.amazonaws.com/${env.ECR_REPO}"
        //                 def imageFullTag = "${ecrUrl}:${IMAGE_TAG}"

        //                 echo "Triggering deployment to AWS App Runner..."

        //                 sh """
        //                 SERVICE_ARN=\$(aws apprunner list-services --query "ServiceSummaryList[?ServiceName=='${SERVICE_NAME}'].ServiceArn" --output text --region ${AWS_REGION})
        //                 echo "Found App Runner Service ARN: \$SERVICE_ARN"

        //                 aws apprunner start-deployment --service-arn \$SERVICE_ARN --region ${AWS_REGION}
        //                 """
        //             }

        //         }
        //     }
        // }
        
    }
}