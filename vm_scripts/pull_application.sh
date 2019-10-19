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

while [[ -z "$appName" ]]
do
    echo "Quel est le nom de l'application à pull ?"
    echo $(cat "$gitListFile" | cut -d, -f1 | tr '\n' ' ')
    read appName

    if [[ ! -z "$appName" ]] &&  ! cat "$gitListFile" | cut -d, -f1 | grep -Fxq "$appName"
    then
        appName=
        log_warning "L'application ${appName} n'existe pas"
    fi

    if ([[ ! -z "$appName" ]] && grep -Fxq "$appName" "$appListFile") || [[ "$appName" == "scheduler" ]] || [[ "$appName" == "drive" ]] || [[ "$appName" == "postgres" ]]
    then
        appName=
        log_warning "L'application ${appName} existe déjà"
    fi
done

pull_app ${appName}
return_code=${?}
if [[ ${return_code} -eq 0 ]]
then
    log_success "Le script s'est terminé sans problème"
    exit 0
else
    log_error "Une erreur s'est produit lors de l'execution du script"
    exit ${return_code}
fi