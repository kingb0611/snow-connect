pipeline {
    agent any
    environment {
        PYTHON_VERSION = '3.11'
    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout source code from GitHub
                git url: 'https://github.com/kingb0611/snow-connect.git', branch: 'master'
            }
        }
        stage('Setup Python Env') {
            steps {
                // Install Python and dependencies including boto3
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install boto3
                pip install pytest
                '''
            }
        }

        stage('List Workspace') {
            steps {
                sh 'ls -R'
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                . venv/bin/activate
                pytest aws-connect/tests/py_test.py --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Get AWS Credentials') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh 'echo "AWS credentials set as environment variables"'
                }
            }
        }
        stage('Deploy/Run AWS Script') {
            when {
                expression { fileExists('create-user.py') }
            }
            steps {
                sh '''
                . venv/bin/activate
                python create-user.py
                '''
            }
        }
    }
}
