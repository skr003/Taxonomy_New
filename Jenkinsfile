pipeline {
    agent any
    environment {
        REMOTE_USER = "jenkins"
    }
    stages {
        stage('Get Remote IP') {
            steps {
                withCredentials([string(credentialsId: 'remote-agent-ip', variable: 'TARGET_IP')]) {
                    sh 'echo "[+] Using remote IP from credentials: $TARGET_IP"'
                }
            }
        }
        stage('Copy Collector Script') {
            steps {
                withCredentials([string(credentialsId: 'remote-agent-ip', variable: 'TARGET_IP')]) {
                    sh '''
                        echo "[+] Copying collector.py to remote server..."
                        scp -o StrictHostKeyChecking=no collector.py ${REMOTE_USER}@${TARGET_IP}:/home/jenkins/forensic/collect_agent.py
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "chmod +x home/jenkins/forensic/collect_agent.py"
                    '''
                }
            }
        }
        stage('Run Collector on Remote') {
            steps {
                withCredentials([string(credentialsId: 'remote-agent-ip', variable: 'TARGET_IP')]) {
                    sh '''
                        echo "[+] Running collector.py on remote..."
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "python3 /home/jenkins/forensic/collect_agent.py"

                        echo "[+] Finding archive on remote..."
                        REMOTE_ARCHIVE=$(ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "ls -t /tmp/logs_*.tar.gz | head -n1")

                        echo "[+] Copying archive back..."
                        scp -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP}:$REMOTE_ARCHIVE .

                        echo "[+] Cleaning up remote..."
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "rm -f $REMOTE_ARCHIVE /home/jenkins/forensic/collect_agent.py"
                    '''
                }
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs_*.tar.gz', fingerprint: true
            }
        }
    }
}
