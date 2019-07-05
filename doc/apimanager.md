[home](/doc/environnement_setup.md)

## Wrappers pour l'utilisation de l'apimanager


Pour utiliser les wrappers vous devez utiliser le package déjà installer sur votre environnement :

	from apipkg import api_manager as api

## Fonctions développées par le socle technique 

Pour utiliser les fonctions du package : api.fonction 
**Exemple** : api.register()

 - **register(url, service_name)**



*url*: L'adresse sur laquel le service est exposé
*service_name*: le nom du service 

**Exemple** :

	 register('http://localhost:5000', 'scheduler')

Cette fonction permet d'enregistrer votre application à l'api manager et de créer une route par défaut dont le nom de la route sera le nom de l'application.

- **unregister(service_name)**

*service_name*: le nom du service

**Exemple** :

	unregister('scheduler')

La fonction "unregister" supprimer de l'api manager les routes associés au service renseigner par "service_name" et le service  lui-même.

 - **send_request(host, url)**

*host* : Nom du service avec lequel on veut communiquer
*url*: requête dont vous voulez parler

**Exemple**: 

	time = api.send_request('scheduler', 'clock/time')

La fonction "send_request" vas exécuter une requête http à l'api manager kong et nécessite le Hostname (nom de l'application enregistrer sur l'apimanager) et la requête que vous voulez appeler.
Dans l'exemple précédent une application peut demander le temps à l'application "clock" précédemment enregistrer sur Kong.

D'autre fonction on été développé mais qui pour l'instant vous semble pas utile, vous pouvez regarder les autres fonctions développer sur le repo suivant : 
https://github.com/ursi-2020/technical-base-package/blob/master/apipkg/api_manager.py
