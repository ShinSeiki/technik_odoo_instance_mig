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
            def props = readProperties file: '.mod_to_update'
            def ODOO_DEV_DATABASE= props['ODOO_DEV_DATABASE']
            def ODOO_DEV_MODULES= props['ODOO_DEV_MODULES']
            echo "Fin carga"
            echo "${ODOO_DEV_DATABASE}"
            echo "${ODOO_DEV_MODULES}"
            sh ". .mod_to_update; Actualizando db[${ODOO_DEV_DATABASE}] con los modulos[${ODOO_DEV_MODULES}]"
            sh "echo Actualizando db[${env.ODOO_DEV_DATABASE}] con los modulos[${env.ODOO_DEV_MODULES}]"
            sh '. .mod_to_update; docker compose exec erp bash -c "odoo --no-http --stop-after-init --dev=all -u all -d viniteca_tk1"'
          }
        }
      }
    }
  }
}
