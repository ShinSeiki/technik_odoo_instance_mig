pipeline {
  agent any

  environment {
    MY_GIT_COMMIT = "${GIT_COMMIT}"
    ODOO_PATH = "/opt/technik_demo01"
  }

  stages {
    stage ('Git Pull') {
      agent { label 'yesdy' }
      options { skipDefaultCheckout() }

      steps {
        echo "git commit id: ${GIT_COMMIT}"
        dir ("${ODOO_PATH}") {
          sh "git fetch"
          sh "git checkout ${GIT_COMMIT}"
          sh "LAST_COMMIT=\$(cat ${ODOO_PATH}/.last-commit); echo \${LAST_COMMIT}..${GIT_COMMIT}"
          script {
            def LAST_COMMIT_FILE = readFile "${ODOO_PATH}/.last-commit"
            env.LAST_COMMIT = LAST_COMMIT_FILE
          }
          sh '''
            echo ${LAST_COMMIT}..${MY_GIT_COMMIT};
            MODS_UPDATE=$(git diff --name-only ${LAST_COMMIT}..${MY_GIT_COMMIT} | grep ^extra-addons | sed 's|^extra-addons/||' | awk -F '/' '{ print $1 }' | sort | uniq | paste -sd ',' -);
            echo ${MODS_UPDATE};
            if [ ! -z "${MODS_UPDATE}" ]; then
              echo "Actualizando Modulos: ${MODS_UPDATE}"
              DBS=$(echo "SELECT datname FROM pg_database WHERE datname <> ALL (\'{template0,template1,postgres}\')" | docker compose exec -T erp bash -c \'PGPASSWORD=$ERP_DB_PASSWORD psql -h db -U $ERP_DB_USER -t -A  -f - template1\')
              echo "${DBS}" | while read line; do
                if [ ! -z "${line}" ]; then
                  echo "Actualizando Base de datos: ${line}"
                  docker compose exec erp odoo --no-http --stop-after-init --dev=all -u ${MODS_UPDATE} -d ${line}
                fi
              done
            fi
          '''
          //sh "echo ${GIT_COMMIT} > .last-commit"
          //sh "docker compose exec erp bash -c 'odoo --no-http --stop-after-init --dev=all -u ${env.ODOO_DEV_MODULES} -d ${env.ODOO_DEV_DATABASE}'"
        }
      }
    }
  }
}
