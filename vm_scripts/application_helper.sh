#!/bin/bash

source ./tc_functions.sh

error(){
    log_error "ERREUR : paramètres invalides !" >&2
    echo "utilisez l'option -h pour en savoir plus" >&2
    exit 1
}

usage(){
    echo "Usage: application_helper [options]"
    echo "-h : afficher l'aide"
    echo "-a : ajouter une application"
    echo "-r : supprimer une application"
    echo "-p : pull une application existante depuis l'adresse git"
}

[[ $# -lt 1 ]] && error

while getopts "harp" option; do
    case "$option" in
        a) sudo -u socle-technique /usr/local/bin/add_application.sh ${USER} ;;
        r) sudo -u socle-technique /usr/local/bin/remove_application.sh ${USER} ;;
        p) sudo -u socle-technique /usr/local/bin/pull_application.sh ${USER} ;;
        :) error ;;
        h) usage ;;
        *) error ;;
    esac
done
exit 0