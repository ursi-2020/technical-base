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

add_app ${appName}
return_code=${?}
if [[ ${return_code} -eq 0 ]]
then
    log_success "Le script s'est terminé sans problème"
    exit 0
else
    log_error "Une erreur s'est produit lors de l'execution du script"
    exit ${return_code}
fi