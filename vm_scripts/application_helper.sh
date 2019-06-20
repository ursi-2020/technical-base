#!/bin/bash

error(){
    echo "ERREUR : paramètres invalides !" >&2
    echo "utilisez l'option -h pour en savoir plus" >&2
    exit 1
}

usage(){
    echo "Usage: application_helper [options]"
    echo "-h : afficher l'aide"
    echo "-a : ajouter une application"
    echo "-r : supprimer une application"
}

[[ $# -lt 1 ]] && error

while getopts "har" option; do
    case "$option" in
        a) sudo -u socle-technique /usr/local/bin/add_application.sh ;;
        r) sudo -u socle-technique /usr/local/bin/remove_application.sh ;;
        :) error ;;
        h) usage ;;
        *) error ;;
    esac
done
exit 0