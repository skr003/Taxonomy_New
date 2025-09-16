pipeline {
    agent any
    environment {
        REMOTE_USER = "jenkins"
    }
    parameters {
        string(name: 'TARGET_IP', description: 'Enter the remote agent IP address')
    }
    stages {
        stage('Copy Collector Script') {
            steps {
                sh '''
                    echo "[+] Copying collector.py to remote server..."
                    scp -o StrictHostKeyChecking=no collector.py ${REMOTE_USER}@${TARGET_IP}:/tmp/collector.py
                    ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "chmod +x /tmp/collector.py"
                '''
            }
        }
        stage('Run Collector on Remote') {
            steps {
                sh '''
                    echo "[+] Running collector.py on remote..."
                    ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "python3 /tmp/collector.py"

                    echo "[+] Finding archive on remote..."
                    REMOTE_ARCHIVE=$(ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "ls -t /tmp/logs_*.tar.gz | head -n1")

                    echo "[+] Copying archive back..."
                    scp -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP}:$REMOTE_ARCHIVE .

                    echo "[+] Cleaning up remote..."
                    ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${TARGET_IP} "rm -f $REMOTE_ARCHIVE /tmp/collector.py"
                '''
            }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: 'logs_*.tar.gz', fingerprint: true
            }
        }
    }
}
