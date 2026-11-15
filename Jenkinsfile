pipeline {
  agent any
  environment {
    IMAGE = "dp7049/health-api"
    TAG   = "${BUILD_NUMBER}"
    PATH  = "/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:${PATH}"
    DOCKER_CONFIG = "/tmp/docker-health"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Secret Scan - Gitleaks') {
      steps {
        sh 'docker run --rm -v "$PWD":/repo zricethezav/gitleaks:latest detect --source /repo --no-git --redact'
      }
    }
    stage('SAST - Bandit') {
      steps {
        sh '''
          python3 -m venv /tmp/venv-health
          . /tmp/venv-health/bin/activate
          pip install -q bandit pip-audit
          bandit app.py -ll
        '''
      }
    }
    stage('Dependency Scan - pip-audit') {
      steps {
        sh '''
          . /tmp/venv-health/bin/activate
          pip-audit -r requirements.txt
        '''
      }
    }
    stage('Build Image') {
      steps { sh 'docker build -t $IMAGE:$TAG .' }
    }
    stage('Image Scan - Trivy') {
      steps {
        sh '''
          mkdir -p $HOME/.trivy-cache
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v $HOME/.trivy-cache:/root/.cache/ aquasec/trivy:latest image --severity CRITICAL --ignore-unfixed --exit-code 1 --no-progress $IMAGE:$TAG
        '''
      }
    }
    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh '''
            mkdir -p $DOCKER_CONFIG
            echo $P | docker login -u $U --password-stdin
            docker push $IMAGE:$TAG
          '''
        }
      }
    }
    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          kubectl config use-context docker-desktop
          sed "s|__IMAGE__|$IMAGE:$TAG|" k8s/deployment.yaml | kubectl apply -f -
          kubectl rollout status deployment/health-api
        '''
      }
    }
  }
}
