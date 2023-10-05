//
//DevOps Project DOCKER Pipeline
// - now with MySQL in Docker Compose
//
pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '20', daysToKeepStr: '5'))
    }
    environment {
        python_run_file = '/Users/markwiltshire/PycharmProjects/DevOps/venv/bin/python'
        email_message = "ERROR Running ${env.JOB_NAME}  Build ${env.BUILD_NUMBER} on ${env.JENKINS_URL}\n\n Look at the job here ${env.BUILD_URL}\n\n"
        // combined testing passed test parameters
        cmb_test_user_id = 22
        cmb_test_user_name = "Mark"
        // Remote DB Hosting settings
        remote_db_host = "sql8.freesqldatabase.com"
        remote_db_port = 3306
        // Remote MySQL Credentials in Jenkins
        REMOTE_MYSQL_CREDS     = credentials('remote-mysql')
        // Docker Local DB Hosting settings
        local_db_host = "devops-db"
        local_db_port = 3306
        // Docker Container Local MySQL Credentials in Jenkins
        DOCKER_MYSQL_CREDS     = credentials('docker-local-mysql')
        DOCKER_ROOT_MYSQL_CREDS = credentials('docker-local-mysql-root')
        // Docker Credentials in Jenkins
        MYDOCKER_CREDS  = credentials('Docker')
        docker_image_name = "devops-rest"
        // Versioning - combined with env.BUILD_NUMBER to tag docker push commands
        // SHOULD really do this from git tags
        base_version = "version1.0."
    }
    stages {
        stage('Pull Code') {
            steps {
                echo "Running ${env.JOB_NAME}  Build ${env.BUILD_NUMBER} on ${env.JENKINS_URL} Local then DOCKER testing"
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
                            bat 'start/min python rest_app.py --db_host=$remote_db_host --db_port=$remote_db_port --db_user=$REMOTE_MYSQL_CREDS_USR --db_pass=$REMOTE_MYSQL_CREDS_PSW'
                        } else {
                            //sh 'nohup python rest_app.py &'
                            //sh 'nohup python3 rest_app.py &'
                            sh 'nohup ${python_run_file} rest_app.py --db_host=$remote_db_host --db_port=$remote_db_port --db_user=$REMOTE_MYSQL_CREDS_USR --db_pass=$REMOTE_MYSQL_CREDS_PSW &'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python rest_app.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Wait for Backend Server') {
            steps {
                echo 'Waiting for Backend Server...'
                script {
                    timeout(2) {
                        waitUntil {
                            try {
                                //should do windows version aswell
                                sh "curl -s --head  --request GET  localhost:5000/users/1 | grep '200'"
                                return true
                            } catch (Exception e) {
                                return false
                            }
                        }
                    }
                }
            }
        }
        stage('Run Backend Testing') {
            steps {
                echo 'Running Backend Testing'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'python backend_testing.py $remote_db_host $remote_db_port $REMOTE_MYSQL_CREDS_USR $REMOTE_MYSQL_CREDS_PSW'
                        } else {
                            sh '${python_run_file} backend_testing.py $remote_db_host $remote_db_port $REMOTE_MYSQL_CREDS_USR $REMOTE_MYSQL_CREDS_PSW'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python backend_testing.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Running Build Docker Image'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'docker build -t $docker_image_name .'
                        } else {
                            sh 'docker build -t $docker_image_name .'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Docker Build!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Tag, Login & Push Docker Image') {
            steps {
                echo 'Running Tag, Login & Push Docker Image'
                // using https://docs.docker.com/docker-hub/access-tokens/ to login to docker hub
                // hub login credentials setup in Jenkins
                // tag twice - 1st - with latest - 2nd with latest version number
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'docker tag $docker_image_name $MYDOCKER_CREDS_USR/$docker_image_name:latest'
                            bat 'docker tag $docker_image_name $MYDOCKER_CREDS_USR/$docker_image_name:$base_version$BUILD_NUMBER'
                            bat 'echo $MYDOCKER_CREDS_PSW | docker login -u $MYDOCKER_CREDS_USR --password-stdin'
                            bat 'docker push -a $MYDOCKER_CREDS_USR/$docker_image_name'
                        } else {
                            sh 'docker tag $docker_image_name $MYDOCKER_CREDS_USR/$docker_image_name:latest'
                            sh 'docker tag $docker_image_name $MYDOCKER_CREDS_USR/$docker_image_name:$base_version$BUILD_NUMBER'
                            sh 'echo $MYDOCKER_CREDS_PSW | docker login -u $MYDOCKER_CREDS_USR --password-stdin'
                            sh 'docker push -a $MYDOCKER_CREDS_USR/$docker_image_name'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Docker Tag, Login & Push!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Set Environment variables') {
            steps {
                echo 'Set Environment variables'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'echo IMAGE_TAG=$base_version$BUILD_NUMBER > .env'
                            bat 'echo db_host=$local_db_host >> .env'
                            bat 'echo db_port=$local_db_port >> .env'
                            bat 'echo db_user=$DOCKER_MYSQL_CREDS_USR >> .env'
                            bat 'echo $DOCKER_ROOT_MYSQL_CREDS_PSW > db_root_password.txt'
                            bat 'echo $DOCKER_MYSQL_CREDS_PSW > db_password.txt'
                        } else {
                            sh 'echo IMAGE_TAG=$base_version$BUILD_NUMBER > .env'
                            sh 'echo db_host=$local_db_host >> .env'
                            sh 'echo db_port=$local_db_port >> .env'
                            sh 'echo db_user=$DOCKER_MYSQL_CREDS_USR >> .env'
                            sh 'echo $DOCKER_ROOT_MYSQL_CREDS_PSW > db_root_password.txt'
                            sh 'echo $DOCKER_MYSQL_CREDS_PSW > db_password.txt'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Set Environment variables!'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Docker-Compose up and wait') {
            steps {
                echo 'Docker-Compose up and wait'
                // --wait implies -d so don't need it.
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'docker-compose up --wait'
                        } else {
                            sh 'docker-compose up --wait'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running docker-compose up'
                        error('Aborting the build')
                    }
                }
            }
        }
        stage('Docker-Compose test') {
            steps {
                echo 'Docker-Compose test'
                script {
                    try {
                        if (checkOs() == 'Windows') {
                            bat 'python docker_backend_testing.py localhost $local_db_port $DOCKER_MYSQL_CREDS_USR $DOCKER_MYSQL_CREDS_PSW'
                        } else {
                            sh '${python_run_file} docker_backend_testing.py localhost $local_db_port $DOCKER_MYSQL_CREDS_USR $DOCKER_MYSQL_CREDS_PSW'
                        }
                    } catch (Exception e) {
                        echo 'Exception Running Python backend_testing.py!'
                        error('Aborting the build')
                    }
                }
            }
        }
    }
    post {
        always {
            //we always want to clean up even if the build failed
            // 1. run cleanenvironment
            // 1. Docker-compose down
            // 2. docker delete image
            // 3. .env file
            // can get image id from - docker images | grep rest_app | awk '{print $3}'
            //we always want to clean up even if the build failed
            echo 'Running Cleanup'
            script {
                // clean up environment - remove docker container, images and .env file.
                try {
                    if (checkOs() == 'Windows') {
                        bat 'python clean_environment.py'
                        bat 'docker-compose down -v'
                        bat 'docker rmi $docker_image_name'
                        bat 'docker rmi $docker_image_name:$base_version$BUILD_NUMBER'
                        bat 'docker rmi $MYDOCKER_CREDS_USR/$docker_image_name:latest'
                        bat 'docker rmi $MYDOCKER_CREDS_USR/$docker_image_name:$base_version$BUILD_NUMBER'
                        bat 'del .env'
                        bat 'del db_password.txt'
                        bat 'del db_root_password.txt'
                    } else {
                        sh '${python_run_file} clean_environment.py'
                        //sh 'docker-compose down -v'
                        //sh 'docker rmi $docker_image_name'
                        //sh 'docker rmi $docker_image_name:$base_version$BUILD_NUMBER'
                        //sh 'docker rmi $MYDOCKER_CREDS_USR/$docker_image_name:latest'
                        //sh 'docker rmi $MYDOCKER_CREDS_USR/$docker_image_name:$base_version$BUILD_NUMBER'
                        sh 'rm .env'
                        sh 'rm db_password.txt'
                        sh 'rm db_root_password.txt'
                    }
                } catch (Exception e) {
                    echo 'Exception Running Cleanup! {e}'
                }
            }
        }
        failure {
            echo "Sent email with message about error for ${env.JOB_NAME}  Build ${env.BUILD_NUMBER} on ${env.JENKINS_URL}"
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