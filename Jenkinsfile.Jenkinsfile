pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }
    environment {
        //where python runs in PyCharm so I get the environment
        //would need to change this for other users
        python_run_file = '/Users/markwiltshire/PycharmProjects/DevOps/venv/bin/python'
        JOB_BASE_NAME = "${JOB_NAME.substring(JOB_NAME.lastIndexOf('/') + 1, JOB_NAME.length())}"
    }
    stages {
        stage('Pull Code') {
            steps {
                echo '${JOB_BASE_NAME}'
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
                        try {
                            bat 'start/min python rest_app.py'
                        } catch (Exception e) {
                            echo 'Exception Running Python rest_app.py!'
                            error('Aborting the build')
                        }
                    } else {
                        try {
                            //sh 'nohup python rest_app.py &'
                            //sh 'nohup python3 rest_app.py &'
                            sh 'nohup ${python_run_file} rest_app.py &'
                        } catch (Exception e) {
                            echo 'Exception Running Python rest_app.py!'
                            error('Aborting the build')
                        }
                    }
                }
            }
        }
        stage('Run Frontend Server') {
            steps {
                echo 'Running Frontend Server'
                script {
                    if (checkOs() == 'Windows') {
                        try {
                            bat 'start/min python web_app.py'
                        } catch (Exception e) {
                            echo 'Exception Running Python rest_app.py!'
                            error('Aborting the build')
                        }
                    } else {
                        try {
                            sh 'nohup ${python_run_file} web_app.py &'
                        } catch (Exception e) {
                            echo 'Exception Running Python rest_app.py!'
                            error('Aborting the build')
                        }
                    }
                }
            }
        }
        stage('Run Backend Testing') {
            steps {
                echo 'Running Backend Testing'
                script {
                    if (checkOs() == 'Windows') {
                        try {
                            bat 'python backend_testing.py'
                        } catch (Exception e) {
                            echo 'Exception Running Python rest_app.py!'
                            error('Aborting the build')
                        }
                    } else {
                        try {
                            sh '${python_run_file} backend_testing.py'
                        } catch (Exception e) {
                            echo 'Exception Running Python backend_testing.py!'
                            error('Aborting the build')
                        }
                    }
                }
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
        //failure {
        always {
            echo 'Sent email with message about error for ${env.JOB_NAME} ${env.BUILD_NUMBER}'
            //http://<JENKINS_SERVER>:<PORT>/job/<JOB_NAME>/lastSuccessfulBuild/api/json?tree=result
            emailext body: 'Look at the job here http://localhost:8080/job/${env.JOB_NAME}/${env.BUILD_NUMBER}/', recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: 'Jenkins ${env.JOB_NAME} ${env.BUILD_NUMBER}'
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