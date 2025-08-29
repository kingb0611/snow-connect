pipeline {
    agent any
    environment {
        PYTHON_VERSION = '3.11'
    }
    stages {
        stage('Checkout') {
            steps {
                // Checkout source code from GitHub
                git url: 'https://github.com/kingb0611/snow-connect.git', branch: 'main'
            }
        }
        stage('Setup Python Env') {
            steps {
                // Install Python and dependencies including boto3
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install boto3
                '''
            }
        }
        stage('Lint') {
            steps {
                // Perform linting using flake8
                sh '''
                . venv/bin/activate
                pip install flake8
                flake8 .
                '''
            }
        }
        stage('Test') {
            steps {
                // Run tests (adapt if project includes tests)
                sh '''
                . venv/bin/activate
                if [ -f tests/test.py ]; then python tests/test.py; fi
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
