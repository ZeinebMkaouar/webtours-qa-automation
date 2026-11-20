pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Recuperation du code source depuis Git...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installation des dependances Python et Playwright...'
                bat '''
                    python -m pip install -r requirements.txt
                    python -m playwright install chromium
                '''
            }
        }

        stage('Execute Playwright Tests') {
            steps {
                echo 'Lancement de la suite de tests automatises...'
                bat '''
                    python -m pytest test_webtours.py -v --html=reports/report.html --self-contained-html --junitxml=reports/results.xml
                '''
            }
        }
    }

    post {
        always {
            echo 'Publication des rapports de tests...'
            junit allowEmptyResults: true, testResults: 'reports/results.xml'
            
            publishHTML target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Rapport HTML Playwright'
            ]
        }
        success {
            echo 'Tous les tests Web Tours ont reussi avec succes !'
        }
        failure {
            echo 'Des tests ont echoue. Consulter le rapport pour analyse.'
        }
    }
}
