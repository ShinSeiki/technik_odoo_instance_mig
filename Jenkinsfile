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
          sh "LAST_COMMIT=$(.last-commit); echo ${LAST_COMMIT}..${GIT_COMMIT}"
          script {
            def props = readProperties file: '/opt/technik_demo01/.mod_to_update'
            env.ODOO_DEV_DATABASE = props.ODOO_DEV_DATABASE
            env.ODOO_DEV_MODULES = props.ODOO_DEV_MODULES
            echo "${env.ODOO_DEV_DATABASE}"
            echo "${env.ODOO_DEV_MODULES}"
          }
          sh "echo Actualizando db[${env.ODOO_DEV_DATABASE}] con los modulos[${env.ODOO_DEV_MODULES}]"
          sh "docker compose exec erp bash -c 'odoo --no-http --stop-after-init --dev=all -u ${env.ODOO_DEV_MODULES} -d ${env.ODOO_DEV_DATABASE}'"
        }
      }
    }
  }
}
