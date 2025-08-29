pipeline {
    agent any
    environment {
        PYTHON_VERSION = '3.11'
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/kingb0611/snow-connect.git', branch: 'master'
            }
        }
        stage('Setup Python Env') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install boto3
                pip install pytest
                '''
            }
        }
        stage('Test') {
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                sh '''
                . venv/bin/activate
                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                PYTHONPATH=./aws_connect pytest tests/py_test.py --maxfail=1 --disable-warnings -q
                '''
                }
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
                expression { fileExists('aws_connect/create_user.py') }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                sh '''
                . venv/bin/activate
                export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                python aws_connect/create_user.py
                '''
                }
            }
        }
    }
}
