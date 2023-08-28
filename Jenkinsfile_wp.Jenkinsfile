pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }
    parameters {
        // choice for which testing is carried out.
        // could use active choices - using jenkins plugin - https://plugins.jenkins.io/uno-choice/
        // see more here - https://devopscube.com/declarative-pipeline-parameters/
        choice(name: 'testing', choices: [3, 2, 1], description: 'What testing should be done? - 1 = frontend, 2 = backend, 3 [default] = combined')
    }
    environment {
        python_run_file = '/Users/markwiltshire/PycharmProjects/DevOps/venv/bin/python'
        email_message = "ERROR Running ${env.JOB_NAME}  Build ${env.BUILD_ID} on ${env.JENKINS_URL}\n\n Look at the job here ${env.BUILD_URL}\n\n"
        // combined testing passed test parameters
        cmb_test_user_id = 22
        cmb_test_user_name = "Mark"
        // DB Hosting settings
        db_host = "sql8.freesqldatabase.com"
        db_port = 3306
        // MySQL Credentials in Jenkins
        MYSQL_CREDS     = credentials('mysql')
    }
    stages {
        stage('Pull Code') {
            steps {
                echo "Running ${env.JOB_NAME}  Build ${env.BUILD_ID} on ${env.JENKINS_URL}"
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
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'start/min python rest_app.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW'
                        } else {
                            //sh 'nohup python rest_app.py &'
                            //sh 'nohup python3 rest_app.py &'
                            sh 'nohup ${python_run_file} rest_app.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW &'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python rest_app.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Run Frontend Server') {
            steps {
                echo 'Running Frontend Server'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'start/min python web_app.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW'
                        } else {
                            sh 'nohup ${python_run_file} web_app.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW &'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python rest_app.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Run Frontend Testing') {
            when {
                expression {
                   return testing == 1
                }
            }
            steps {
                echo 'Running Frontend Testing'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'python frontend_testing.py'
                        } else {
                            sh '${python_run_file} frontend_testing.py'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python frontend_testing.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Run Backend Testing') {
            when {
                expression {
                   return testing == 2
                }
            }
            steps {
                echo 'Running Backend Testing'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'python backend_testing.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW'
                        } else {
                            sh '${python_run_file} backend_testing.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python backend_testing.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Run Combined Testing') {
            when {
                expression {
                   return params.testing.toInteger() == 3
                }
            }
            steps {
                echo 'Running Combined Testing'
                //passing parameters for user input
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'python combined_testing.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW -i $cmb_test_user_id -n $cmb_test_user_name'
                        } else {
                            sh '${python_run_file} combined_testing.py $db_host $db_port $MYSQL_CREDS_USR $MYSQL_CREDS_PSW -i $cmb_test_user_id -n $cmb_test_user_name'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python combined_testing.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
    }
    post {
        always {
            //we always want to clean up even if the build failed
            echo 'Running Cleanup'
            script {
                try {
                    if (checkOs() == 'Windows') {
                        bat 'python clean_environment.py'
                    } else {
                        sh '${python_run_file} clean_environment.py'
                    }
                } catch (Exception e) {
                    echo 'Exception Running Python clean_environment.py!'
                }
            }
        }
        failure {
            echo "Sent email with message about error for ${env.JOB_NAME}  Build ${env.BUILD_ID} on ${env.JENKINS_URL}"
            emailext body: email_message, recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']], subject: "FAILED: Jenkins ${env.JOB_NAME} Build ${env.BUILD_NUMBER}"
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