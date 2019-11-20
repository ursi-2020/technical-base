#!/bin/bash

set -e
source ./tc_variables.sh
source ./tc_functions.sh

appName=
exec_user=${1}

if [[ ! -d "$mountedDirectory" ]]
then
    log_error "Impossible de trouver le répertoire ${mountedDirectory}, le script va se stopper"
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
        log_warning "L'application ${appName} n'existe pas"
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

remove_app ${appName}
return_code=${?}
if [[ ${return_code} -eq 0 ]]
then
    log_success "Le script s'est terminé sans problème"
    exit 0
else
    log_error "Une erreur s'est produit lors de l'execution du script"
    exit ${return_code}
fi