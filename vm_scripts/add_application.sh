#!/bin/bash

set -e
mountedDirectory="/mnt/technical_base"
venvDirectory="/home/socle-technique/python_venv"
appName=

if [[ ! -d "$mountedDirectory" ]]
then
    echo "Impossible de trouver le répertoire ${mountedDirectory}, le script va se stopper"
    exit 1
fi

while [[ -z "$appName" ]] || [[ $(echo -n "$appName" | wc -m) -gt 30 ]] || [[ ! "$appName" =~ ^[a-zA-Z0-9_]+$ ]]
do
    echo "Quel est le nom de la nouvelle application ? Le nom ne doit pas dépasser 30 caractères et ne comporter" \
    "que des caractères alphanumériques"
    read appName

    if [[ ! -z "$appName" ]] && [[ -e "${mountedDirectory}/${appName}" ]]
    then
        appName=
        echo "L'application ${appName} existe déjà"
    fi
done

appdir="${mountedDirectory}/${appName}"
mkdir ${appdir}
echo "Le dossier de l'application a été créé au chemin suivant: ${appdir}"
virtualenv "${venvDirectory}/${appName}_venv"
echo "Le python virtual env de l'application a été créé au chemin suivant: ${venvDirectory}/${appName}_venv"

dbpasswd=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13)

sudo -u postgres psql -c "CREATE USER $appName WITH PASSWORD '$dbpasswd';";
sudo -u postgres psql -c "CREATE DATABASE ${appName}_db;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${appName}_db TO ${appName};"

echo "Une base de données PostgreSQL a été créé avec les credentials suivants, merci de les noter."
echo "Nom de la base de données: ${appName}_db"
echo "Utilisateur propriétaire de la base de données: ${appName}"
echo "Mot de passe de l'utilisateur: ${dbpasswd}"

clonedir="/tmp/example-app/"

if [[ -d ${clonedir} ]]
then
    rm -rf ${clonedir}
fi

keyfile="/home/socle-technique/.ssh/github"
if [[ ! -f ${keyfile} ]]
then
    echo "Impossible de trouver la clé ssh pour cloner l'appli blanche, le script va se stopper"
    exit 1
fi

ssh-agent bash -c "ssh-add ${keyfile}; git clone git@github.com:ursi-2020/example-app.git ${clonedir}"
rsync -r --exclude '.git*' ${clonedir} ${appdir}
echo "Un code example d'application a été copié dans le dossier de l'application (${appdir})"

echo "Le script est terminé"
exit 0