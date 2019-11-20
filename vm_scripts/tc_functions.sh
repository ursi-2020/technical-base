#!/bin/bash

source ./tc_variables.sh

RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'

log_error() {
    formatted_date=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "${RED} [${formatted_date}][Applications Helper]${@} ${NC}" 1>&2;
}

log_warning() {
    formatted_date=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "${YELLOW} [${formatted_date}][Applications Helper]${@} ${NC}" 1>&2;
}

log_debug() {
    formatted_date=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "${YELLOW} [${formatted_date}][Applications Helper]${@} ${NC}";
}

log_success() {
    formatted_date=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "${GREEN} [${formatted_date}][Applications Helper]${@} ${NC}";
}

create_env_then_clone_app()
{
    if [[ -z "$1" ]] || [[ -z "$2" ]] || [[ -z "$3" ]]
    then
        return 1
    fi

    appName=${1}
    appDir=${2}
    cloneAddress=${3}

    appName_formatted=$(echo ${appName} | tr '-' '_')
    virtualenv "${venvDirectory}/${appName}_venv"
    log_debug "Exec user: ${exec_user}"
    setfacl -Rm "u:${exec_user}:rwx" "${venvDirectory}/${appName}_venv"
    log_debug "Le python virtual env de l'application a été créé au chemin suivant: ${venvDirectory}/${appName}_venv"

    dbpasswd=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 7)

    sudo -u postgres psql -c "CREATE USER ${appName_formatted} WITH PASSWORD '$dbpasswd';";
    sudo -u postgres psql -c "CREATE DATABASE ${appName_formatted}_db;"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${appName_formatted}_db TO ${appName_formatted};"

    log_debug "Une base de données PostgreSQL a été créé avec les credentials suivants, merci de les noter."
    log_debug "Nom de la base de données: ${appName_formatted}_db"
    log_debug "Utilisateur propriétaire de la base de données: ${appName_formatted}"
    log_debug "Mot de passe de l'utilisateur: ${dbpasswd}"

    cloneDir="/tmp/clone-temp/"

    if [[ -d ${cloneDir} ]]
    then
        rm -rf ${cloneDir}
    fi

    if [[ ! -f ${keyfile} ]]
    then
        log_error "Impossible de trouver la clé ssh pour cloner l'appli blanche, le script va se stopper"
        exit 1
    fi

    ssh-agent bash -c "ssh-add ${keyfile}; git clone ${cloneAddress} ${cloneDir}"
    rsync -r --exclude '.git*' ${cloneDir} ${appDir}
}

add_app() {
    if [[ -z "$1" ]]
    then
        return 1
    fi

    appName=${1}

    appName_formatted=$(echo ${appName} | tr '-' '_')
    appDir="${mountedDirectory}/${appName}"
    mkdir ${appDir}
    log_debug "Le dossier de l'application a été créé au chemin suivant: ${appDir}"
    cloneAddress="git@github.com:ursi-2020/example-app.git"
    create_env_then_clone_app ${appName} ${appDir} ${cloneAddress}
    log_debug "Un code example d'application a été copié dans le dossier de l'application (${appDir})"

    envFile="${appDir}/variables.env"
    echo "DJANGO_DB_USER=${appName_formatted}" > ${envFile}
    echo "DJANGO_DB_NAME=${appName_formatted}_db" >> ${envFile}
    echo "DJANGO_DB_PASSWORD=${dbpasswd}" >> ${envFile}
    echo "DJANGO_APP_NAME=${appName}" >> ${envFile}
    echo "WEBSERVER_PORT=8100" >> ${envFile}

    echo ${appName} >> ${appListFile}
}

pull_app() {
    if [[ -z "$1" ]]
    then
        return 1
    fi

    appName=${1}
    appName_formatted=$(echo ${appName} | tr '-' '_')
    cloneAddress=$(grep "^${appName}," ${gitListFile} | cut -d, -f2)
    port=$(grep "^${appName}," ${gitListFile} | cut -d, -f3)
    appDir="${mountedDirectory}/${appName}"
    mkdir -p ${appDir}
    clonedir="/tmp/pulled-app/"

    if [[ -d "${venvDirectory}/${appName}_venv" ]]
    then
        sudo rm -rf "${venvDirectory}/${appName}_venv"
    fi

    create_env_then_clone_app ${appName} ${appDir} ${cloneAddress}
    log_debug "Le dossier de l'application a été téléchargé au chemin suivant : ${appDir}"

    envFile="${appDir}/variables.env"
    echo "DJANGO_DB_USER=${appName_formatted}" > ${envFile}
    echo "DJANGO_DB_NAME=${appName_formatted}_db" >> ${envFile}
    echo "DJANGO_DB_PASSWORD=${dbpasswd}" >> ${envFile}
    echo "DJANGO_APP_NAME=${appName}" >> ${envFile}
    echo "WEBSERVER_PORT=${port}" >> ${envFile}
    echo ${appName} >> ${appListFile}

    log_debug "L'application ${appName} a été pull"
}

remove_app() {
    if [[ -z "$1" ]]
    then
        return 1
    fi

    appName=${1}

    appName_formatted=$(echo ${appName} | tr '-' '_')
    appDir="${mountedDirectory}/${appName}"
    if [[ -d "$appDir" ]]
    then
        sudo rm -rf ${appDir}
    fi

    venvdir="${venvDirectory}/${appName}_venv"
    if [[ -d "$venvdir" ]]
    then
        sudo rm -rf ${venvdir}
    fi

    sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${appName_formatted}_db;"
    sudo -u postgres psql -c "DROP USER IF EXISTS ${appName_formatted};"

    sed -i "/^${appName}\$/d" ${appListFile}
    log_debug "L'application ${appName} a été supprimé"
}