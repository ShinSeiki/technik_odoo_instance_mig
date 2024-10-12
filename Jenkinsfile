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
          script {
            load ".mod_to_update"
            sh "echo Actualizando db[${env.ODOO_DEV_DATABASE}] con los modulos[${env.ODOO_DEV_MODULES}]"
            sh '. .mod_to_update; docker compose exec erp bash -c "odoo --no-http --stop-after-init --dev=all -u all -d viniteca_tk1"'
          }
        }
      }
    }
  }
}
