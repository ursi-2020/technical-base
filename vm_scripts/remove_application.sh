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
    echo "Quel est le nom de l'application à supprimer ?"
    echo $(tr '\n' ' ' < ${appListFile})
    read appName

    if [[ ! -z "$appName" ]] &&  ! grep -Fxq "$appName" "$appListFile"
    then
        appName=
        echo "L'application ${appName} n'existe pas"
    fi
done

reply=
while [[ ! ${reply} =~ ^[Oo]$ ]] && [[ ! ${reply} =~ ^[Nn]$ ]]
do
    read -p "Êtes vous sûr de vouloir supprimer l'application ${appName} (o/n)?" choice
    case "$choice" in
        o|O ) break;;
        n|N ) exit 0;;
        * ) echo "Choix invalide";;
    esac
done

appName2=$(echo ${appName} | tr '-' '_')
appdir="${mountedDirectory}/${appName}"
if [[ -d "$appdir" ]]
then
    sudo rm -rf ${appdir}
fi

venvdir="${venvDirectory}/${appName}_venv"
if [[ -d "$venvdir" ]]
then
    sudo rm -rf ${venvdir}
fi

sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${appName2}_db;"
sudo -u postgres psql -c "DROP USER IF EXISTS ${appName2};"

sed -i "/^${appName}\$/d" ${appListFile}
echo "L'application ${appName} a été supprimé, le script est terminé"
exit 0