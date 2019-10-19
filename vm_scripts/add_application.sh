#!/bin/bash

set -e
source ./tc_variables.sh
source ./tc_functions.sh

appName=

if [[ ! -d "$mountedDirectory" ]]
then
    log_error "Impossible de trouver le répertoire ${mountedDirectory}, le script va se stopper"
    exit 1
fi

while [[ -z "$appName" ]] || [[ $(echo -n "$appName" | wc -m) -gt 30 ]] || [[ ! "$appName" =~ ^[a-z0-9_-]+$ ]]
do
    echo "Quel est le nom de la nouvelle application ? Le nom ne doit pas dépasser 30 caractères et ne comporter" \
    "que des caractères alphanumériques en minuscule"
    read appName

    if ([[ ! -z "$appName" ]] && grep -Fxq "$appName" "$appListFile") || [[ "$appName" == "scheduler" ]] || [[ "$appName" == "drive" ]] || [[ "$appName" == "postgres" ]] || [[ -d "${mountedDirectory}/${appName}" ]]
    then
        appName=
        log_warning "L'application ${appName} existe déjà"
    fi
done

appName2=$(echo ${appName} | tr '-' '_')
appdir="${mountedDirectory}/${appName}"
mkdir ${appdir}
log_debug "Le dossier de l'application a été créé au chemin suivant: ${appdir}"

virtualenv "${venvDirectory}/${appName}_venv"
setfacl -Rm "u:${1}:rwx" "${venvDirectory}/${appName}_venv"
log_debug "Le python virtual env de l'application a été créé au chemin suivant: ${venvDirectory}/${appName}_venv"

dbpasswd=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 7)

sudo -u postgres psql -c "CREATE USER ${appName2} WITH PASSWORD '$dbpasswd';";
sudo -u postgres psql -c "CREATE DATABASE ${appName2}_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${appName2}_db TO ${appName2};"

log_debug "Une base de données PostgreSQL a été créé avec les credentials suivants, merci de les noter."
log_debug "Nom de la base de données: ${appName2}_db"
log_debug "Utilisateur propriétaire de la base de données: ${appName2}"
log_debug "Mot de passe de l'utilisateur: ${dbpasswd}"

clonedir="/tmp/example-app/"

if [[ -d ${clonedir} ]]
then
    rm -rf ${clonedir}
fi

keyfile="/home/socle-technique/.ssh/github"
if [[ ! -f ${keyfile} ]]
then
    log_error "Impossible de trouver la clé ssh pour cloner l'appli blanche, le script va se stopper"
    exit 1
fi

ssh-agent bash -c "ssh-add ${keyfile}; git clone git@github.com:ursi-2020/example-app.git ${clonedir}"
rsync -r --exclude '.git*' ${clonedir} ${appdir}
log_debug "Un code example d'application a été copié dans le dossier de l'application (${appdir})"

envFile="${appdir}/variables.env"
echo "DJANGO_DB_USER=${appName2}" > ${envFile}
echo "DJANGO_DB_NAME=${appName2}_db" >> ${envFile}
echo "DJANGO_DB_PASSWORD=${dbpasswd}" >> ${envFile}
echo "DJANGO_APP_NAME=${appName}" >> ${envFile}
echo "WEBSERVER_PORT=8100" >> ${envFile}

echo ${appName} >> ${appListFile}
log_success "Le script est terminé sans problème"
exit 0