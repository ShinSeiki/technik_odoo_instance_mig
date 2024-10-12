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
            echo "Inicio carga"
            loadEnvironmentVariablesFromFile(".mod_to_update")
            def props = readProperties file: '.mod_to_update'
            echo "Fin carga"
            echo "${env.ODOO_DEV_DATABASE}"
            echo "${env.ODOO_DEV_MODULES}"
            sh "source .mod_to_update; Actualizando db[${ODOO_DEV_DATABASE}] con los modulos[${ODOO_DEV_MODULES}]"
            sh "echo Actualizando db[${env.ODOO_DEV_DATABASE}] con los modulos[${env.ODOO_DEV_MODULES}]"
            sh '. .mod_to_update; docker compose exec erp bash -c "odoo --no-http --stop-after-init --dev=all -u all -d viniteca_tk1"'
          }
        }
      }
    }
  }
}
