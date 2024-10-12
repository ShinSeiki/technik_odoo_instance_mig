pipeline {
  agent any

  environment {
    MY_GIT_COMMIT = "${GIT_COMMIT}"
  }

  stages {
    stage ('Git Pull') {
      agent { label 'yesdy' }
      options { skipDefaultCheckout() }

      steps {
        echo "git commit id: ${GIT_COMMIT}"
        dir ("/opt/technik_demo01") {
          sh "git fetch"
          sh "git checkout ${GIT_COMMIT}"
        }
      }
      
    }
  }
}
