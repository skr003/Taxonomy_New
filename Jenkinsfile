pipeline {
    agent { label 'forensic-agent' }

    environment {
        WORKSPACE_DIR = "/tmp/forensic_collection"
        OUTPUT_FILE   = "/tmp/forensic_collection.json"
        MONGO_URI = credentials('MONGODB_ATLAS_URI')
        LOKI_URL  = credentials('LOKI_ENDPOINT')
    }

    stages {
        stage('Initialize') {
            steps {
                sh 'mkdir -p ${WORKSPACE_DIR}'
            }
        }

        stage('Run Collector') {
            steps {
                sh 'python3 ${WORKSPACE}/collector.py'
            }
        }

        stage('Archive Results') {
            steps {
                sh 'cp ${OUTPUT_FILE} ${WORKSPACE_DIR}/'
                archiveArtifacts artifacts: 'forensic_collection/forensic_collection.json', followSymlinks: false
            }
        }

        stage('Push to MongoDB Atlas') {
            steps {
                sh 'python3 ${WORKSPACE}/controller/store_metadata.py --mongo-uri "${MONGO_URI}" --input ${OUTPUT_FILE}'
            }
        }

        stage('Format for Loki') {
            steps {
                sh 'python3 ${WORKSPACE}/controller/format_logs_for_loki.py --input ${OUTPUT_FILE} --output ${WORKSPACE_DIR}/loki_payload.json'
            }
        }

        stage('Push to Loki') {
            steps {
                sh 'curl -X POST "${LOKI_URL}" -H "Content-Type: application/json" -d @${WORKSPACE_DIR}/loki_payload.json'
            }
        }

        stage('Visualization Setup') {
            steps {
                echo "✅ Grafana will pick up logs from Loki and metadata from MongoDB Atlas."
            }
        }
    }

    post {
        always {
            echo "✅ Forensic pipeline finished on agent VM."
        }
        failure {
            echo "⚠️ Forensic pipeline failed on agent VM."
        }
    }
}
