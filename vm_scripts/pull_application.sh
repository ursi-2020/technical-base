#!/bin/bash

set -e
source /usr/local/bin/tc_variables.sh
appName=

if [[ ! -d "$mountedDirectory" ]]
then
    echo "Impossible de trouver le répertoire ${mountedDirectory}, le script va se stopper"
    exit 1
fi

while [[ -z "$appName" ]]
do
    echo "Quel est le nom de l'application à pull ?"
    echo $(cat "$gitListFile" | cut -d, -f1 | tr '\n' ' ')
    read appName

    if [[ ! -z "$appName" ]] &&  ! cat "$gitListFile" | cut -d, -f1 | grep -Fxq "$appName"
    then
        appName=
        echo "L'application ${appName} n'existe pas"
    fi

    if ([[ ! -z "$appName" ]] && grep -Fxq "$appName" "$appListFile") || [[ "$appName" == "scheduler" ]] || [[ "$appName" == "drive" ]] || [[ "$appName" == "postgres" ]]
    then
        appName=
        echo "L'application ${appName} existe déjà"
    fi
done

appName2=$(echo ${appName} | tr '-' '_')
git_adress=$(grep "^${appName}," ${gitListFile} | cut -d, -f2)
appdir="${mountedDirectory}/${appName}"
mkdir -p ${appdir}
clonedir="/tmp/pulled-app/"

if [[ -d "${venvDirectory}/${appName}_venv" ]]
then
    sudo rm -rf "${venvDirectory}/${appName}_venv"
fi

virtualenv "${venvDirectory}/${appName}_venv"
setfacl -Rm "u:${1}:rwx" "${venvDirectory}/${appName}_venv"
echo "Le python virtual env de l'application a été créé au chemin suivant: ${venvDirectory}/${appName}_venv"

dbpasswd=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 7)

sudo -u postgres psql -c "CREATE USER ${appName2} WITH PASSWORD '$dbpasswd';";
sudo -u postgres psql -c "CREATE DATABASE ${appName2}_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${appName2}_db TO ${appName2};"

echo "Une base de données PostgreSQL a été créé avec les credentials suivants, merci de les noter."
echo "Nom de la base de données: ${appName2}_db"
echo "Utilisateur propriétaire de la base de données: ${appName2}"
echo "Mot de passe de l'utilisateur: ${dbpasswd}"

if [[ -d ${clonedir} ]]
then
    rm -rf ${clonedir}
fi

keyfile="/home/socle-technique/.ssh/github"
if [[ ! -f ${keyfile} ]]
then
    echo "Impossible de trouver la clé ssh pour cloner l'application "${appName}", le script va se stopper"
    exit 1
fi
ssh-agent bash -c "ssh-add ${keyfile}; git clone ${git_adress} ${clonedir}"
rsync -r ${clonedir} ${appdir}
echo "Le dossier de l'application a été téléchargé au chemin suivant : ${appdir}"

envFile="${appdir}/variables.env"
echo "DJANGO_DB_USER=${appName2}" > ${envFile}
echo "DJANGO_DB_NAME=${appName2}_db" >> ${envFile}
echo "DJANGO_DB_PASSWORD=${dbpasswd}" >> ${envFile}
echo "DJANGO_APP_NAME=${appName}" >> ${envFile}
echo "WEBSERVER_PORT=8100" >> ${envFile}

echo ${appName} >> ${appListFile}
echo "Le script est terminé"
exit 0