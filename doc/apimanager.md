
[Sommaire](https://ursi-2020.github.io/Documentation/)

## Wrappers pour l'utilisation de l'APImanager


Pour utiliser les wrappers vous devez importer le package déjà installé sur votre environnement :

	from apipkg import api_manager as api

## Fonctions développées par le socle technique 

Pour utiliser les fonctions du package : api.< fonction >
**Exemple** : api.register()

---
 - **register(url, service_name)**

**Arguments:**

| Paramètre     | Type | Description |
| :--- |:---| :-- |
| *url*     | string    | Adresse sur laquel le service est exposé |
|*service_name*  | string| Nom du service |


**Exemple** :

	 register('http://localhost:5000', 'scheduler')

**Description:**
Cette fonction permet d'enregistrer votre application à l'APImanager et de créer une route par défaut dont le nom sera le nom de l'application.

---
- **unregister(service_name)**

**Arguments:**

| Paramètre   | Type  | Description |
| :--- |:---| :--
|*service_name* | string |  Nom du service |



**Exemple** :

	unregister('scheduler')

**Description:**
La fonction "unregister" permet de  supprimer de l'APImanager les routes associées au service renseigné par "service_name" et le service lui-même.

---
 - **send_request(host, url)**

**Arguments**:

| Paramètre     | Type | Description |
| :--- |:---|:-- |
| *host*     | string   | Nom du service avec lequel on veut communiquer | 
| *url*       | string  |  URL exposée par le service |


**Retour de la fonction:**
Le retour de la requête envoyée, de type texte.

**Exemple**: 

	time = api.send_request('scheduler', 'clock/time')

**Description:**
La fonction "send_request" va envoyer une requête GET à l'APImanager et celui-ci redirigera la requête vers l'application cible (host).

Dans l'exemple précédent une application peut demander le *time* à l'application "scheduler" précédemment enregistrée sur Kong.

---
 - **get_request(host, url)**

**Arguments**:

| Paramètre    | Type | Description |
| :--- |:---| :--- |
| *host*       | string  | Nom du service avec lequel on veut communiquer |
| *url*         |  string |URL exposé par le service |


**Retour de la fonction:**
Le retour de la fonction est un tuple (status_code, data)

**Exemple**: 

	code_status, products = api.get_request('catalogue-produit', 'api/get-magasin')  
	print("Data: %r" % products)
	print("Code status: %r" % code_status)
Output:
>Data: {"produits": [{"id": 25, "codeProduit": "X1-0", "familleProduit": "Frigos", "descriptionProduit": "Frigos:P1-0", "quantiteMin": 15, "packaging": 2, "prix": 424, "exclusivite": ""}, ...]}
>Code status: 200

**Description:**
La fonction "get_request" a la même fonctionnalité que "send_request" mais elle vous permettra de gérer les cas d'erreur:

	code_status, err = api.get_request('catalogue-produit', 'api/get-magasin')
	if code_status != 200:
		print(err)  // err de type HTTPError



---
 - **post_request(host, url, body)**

**Arguments**:

| Paramètre   | type | Description |
| :--- |:---| :--- |
| *host*     | string    | Nom du service avec lequel on veut communiquer |
| *url*  | string  | URL exposé par le service |
| *body* | string / json | Body avec un format JSON passé à la requête POST |


**Retour de la fonction:**
Le retour de la fonction est un tuple (status_code, response)

**Exemple**: 

	post_request('stock', 'create-ticket', {'id': 2, 'qty': 400})

De la même façon que send_request la fonction post_request va envoyer une requête post à une autre application à l'aide du hostname passé en paramètre, via l'APImanager, avec cette fois ci un body au format json.

**NOTES:**
- Pour ces fonctions post qui appel l'APImanager vous devez désactivé la protection "Cross site request forgery" (CSRF).  [En savoir plus.](https://docs.djangoproject.com/fr/2.2/ref/csrf/)
- Pour utiliser les fonctions POST du scheduler veuillez vous référer à la documentation du scheduler.  [En savoir plus.](https://ursi-2020.github.io/technical-base/doc/scheduler.html)

**Exemple**: 

	from django.views.decorators.csrf import csrf_exempt
	
	@csrf_exempt
	def create-ticket-from-stock() :
		status_code, data = api.post_request('stock', 'create-ticket', {'id': 2, 'qty': 400})
		if status_code != 200:
			print(data) // ici data sera de type HTTPError

---

 - **schedule_task(host, url, time, recurrence, data, source, name)**

**Arguments:**

| Paramètre    | Type | Description |
| :--- |:---| :--- |
| *host*  |  string      | Nom du service avec lequel on veut communiquer. |
| *url*  | string |URL exposée par le service. |
| *time* |Datetime object | Moment à laquelle la tache sera exécutée. |
|*recurrence*| string | Récurrence de la tache avec une des options suivantes : "none", "minute", "hour", "day", "week", "month", "year".
| *data* | string | Data optionnelle qui peut être passée à la route appelée, à travers le body de la requête.
| *source* | string | Nom de l'application qui schedule la tache (en l'occurrence le nom de votre application).
| *name* | string | Nom de votre tache qui permettra de l'identifié. Faites en sorte qu'il soit unique et compréhensible.



**Exemple**: 

	clock_time = api.send_request('scheduler', 'clock/time')  
	api.schedule_task('gestion-magasin', '/products/update/', clock_time, 'day', '{}', 'gestion-magasin', 'Magasin: Update Products')
	
**Description:**
Dans l'exemple ci-contre l'application Gestion-Magasin schedule une tache qui a pour nom 'Magasin: Update Products'  et qui effectuera à partir du moment (ici de l'heure) de la clock, tous les jours, une requête sur '/products/update/'.

**NOTE:**
* Pour éviter que votre tache soit schedule en retard par rapport au temps de la clock, ajoutez du temps à l'argument *time* passé en paramètre à la fonction schedule_task()

---

D'autres fonctions ont été développées mais qui pour l'instant ne vous seront pas utile. Vous pouvez retrouver la totalité des fonctions au répo suivant : https://github.com/ursi-2020/technical-base-package/blob/master/apipkg/api_manager.py

Pour plus d'information sur le fonctionnement de [Kong](https://docs.konghq.com/0.4.x/getting-started/introduction/).
