[home](../index.md)

# First step

Pour vos premiers pas sur ce projet vous devrez simuler une communication entre deux applications ou plus.
Pour cela nous allons utiliser l'API MANAGER Kong et les wrappers développés par le Socle-Technique.
* Vous devrez vous arranger entre les différentes applications sur le format des données que vous voulez envoyer et recevoir.
* Dans l'idéal, vous pourriez utiliser le format json et de vous mettre d'accord sur les attributs des messages, comme par exemple : { 'id':'1', 'app-name', 'caisse', ... }
* Vous devrez définir l'architecture de votre application, créer les fichiers dont vous aurez besoin pour votre développement etc... vous pouvez suivre le tutoriel Django 

Prenons deux applications : A et B

Il vous faut deux fonctions :

Le première sera la fonction qui permettra d'envoyer les informations de l'application A, par exemple le nom de l'application:
	
	def info(request):
		return A-name

Il va aussi falloir ajouter la route qui permettra d'utiliser cette fonction :
dans le fichier urls.py

	urlpatterns = [
		...
		path('info', views.info, name='info'),
	]

Maintenant nous allons appeler la fonction précédemment créée grâce à la route nommée 'info'.
Dans l'application blanche, l'architecture des urls est la suivante :

core.urls.py :

		urlpatterns = [  
		  path('my-app/', include('myapp.urls')),  
		  path('admin/', admin.site.urls),  
		]

myapp.urls.py :
  
	urlpatterns = [  
	  path('', views.index, name='index'),  
	  path('info', views.info, name='info'),  
	]

Donc la route à appeler dans l'application B est la suivante :

	'my-app/info'

Vous pouvez maintenant utiliser la fonction "send_request" du package de l'api manager (documentation : [https://ursi-2020.github.io/technical-base/doc/apimanager.html](https://ursi-2020.github.io/technical-base/doc/apimanager.html))


	A-name = api.send_request('A', 'my-app/info')
