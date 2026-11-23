pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Package') {
      steps { sh 'docker build -t myapp:${BUILD_NUMBER} .' }
    }
    stage('Start Staging') {
      steps {
        sh '''
          docker network create cicd-net || true
          docker rm -f staging || true
          docker run -d --name staging --network cicd-net myapp:${BUILD_NUMBER}
          sleep 3
        '''
      }
    }
    stage('Test') {
      steps {
        sh '''
          docker build -t test-agent ./tests
          mkdir -p reports
          docker rm -f test-run || true
          RESULT=0
          docker run --name test-run --network cicd-net -e BASE_URL=http://staging test-agent pytest -v --junitxml=results.xml || RESULT=$?
          docker cp test-run:/tests/results.xml reports/results.xml || true
          docker rm -f test-run || true
          exit $RESULT
        '''
      }
      post {
        always { junit allowEmptyResults: true, testResults: 'reports/results.xml' }
      }
    }
    stage('Deploy') {
      steps {
        sh '''
          docker rm -f live || true
          docker run -d --name live -p 8082:80 myapp:${BUILD_NUMBER}
        '''
      }
    }
  }
  post {
    always { sh 'docker rm -f staging || true' }
  }
}