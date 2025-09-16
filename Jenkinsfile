pipeline {
    agent any
    environment {
        REMOTE_USER = "jenkins"
    }
    parameters {
        credentials(name: 'TARGET_IP')
    }
    stages {
        stage('Collect Logs') {
            steps {
                    sh '''
                        REMOTE_IP=$(cat $REMOTE_AGENT_IP)
                        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                        ARCHIVE_NAME="logs_${REMOTE_IP}_$TIMESTAMP.tar.gz"

                        echo "[+] Creating tarball on remote..."
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_IP} "tar -czf /tmp/$ARCHIVE_NAME /var/log"

                        echo "[+] Copying back to Jenkins workspace..."
                        scp -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_IP}:/tmp/$ARCHIVE_NAME .

                        echo "[+] Cleaning up remote..."
                        ssh -o StrictHostKeyChecking=no ${REMOTE_USER}@${REMOTE_IP} "rm -f /tmp/$ARCHIVE_NAME"
                    '''
                }
        }
        stage('Archive Logs') {
            steps {
                archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
            }
        }
    }
}
