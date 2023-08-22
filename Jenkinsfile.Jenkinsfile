pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }
    environment {{
        my_var = '123'
    }
    stages {
        stage('Pull Code') {
            steps {
                echo 'Pulling Code'
                script {
                    properties([pipelineTriggers([pollSCM('30 * * * *')])])
                }
                git 'https://github.com/mark-wiltshire/DevOps.git'
            }
        }
        stage('Run Backend Server') {
            steps {
                echo 'Running Backend Server'
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python rest_app.py'
                    } else {
                        sh 'nohup python3 rest_app.py &'
                        //sh 'nohup python rest_app.py &'
                    }
                }
            }
        }
        stage('Run Frontend Server') {
            steps {
                echo 'Running Frontend Server'
                script {
                    if (checkOs() == 'Windows') {
                        bat 'start/min python web_app.py'
                    } else {
                        sh 'nohup python3 web_app.py &'
                    }
                }
            }
        }
        stage('Run Backend Testing') {
            steps {
                echo 'Running Backend Testing'
            }
        }
        stage('Run Frontend Testing') {
            steps {
                echo 'Running Frontend Testing'
            }
        }
        stage('Run Combined Testing') {
            steps {
                echo 'Running Combined Testing'
            }
        }
        stage('Run Clean Up') {
            steps {
                echo 'Running Cleanup'
            }
        }

    }
    post {
        failure {
            echo 'Sent email with message about error'
            //http://<JENKINS_SERVER>:<PORT>/job/<JOB_NAME>/lastSuccessfulBuild/api/json?tree=result
        }
    }
}

def checkOs(){
    if (isUnix()) {
        def uname = sh script: 'uname', returnStdout: true
        if (uname.startsWith("Darwin")) {
            return "Macos"
        }
        else {
            return "Linux"
        }
    }
    else {
        return "Windows"
    }
}