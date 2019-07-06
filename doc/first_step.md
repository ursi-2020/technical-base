Pour vos premier pas sur ce projet vous devrait simuler une communication entre deux applications ou plus.
Pour cela nous allons utiliser l'API MANAGER Kong et les wrappers développés par le Socle-Technique.
* Se sera à vous de vous arranger entre application sur le format des données que vous voulez envoyer et recevoir.
* Le mieux serai d'utiliser le format json et de vous mettre daccord sur les attributs des messages par exemple : { 'id':'1', 'app-name', 'caisse', ... }
* Ce sera aussi à vous de définir l'architecture de votre application, coder sur quel fichier etc... vous pouvez suivre le tutorial Django 

Prenons deux applications : A et B

Il vous faut deux fonctions :


Le première sera la fonction qui permettra d'envoyer les informations de l'application A , par exemple le nom de l'application:
	
	def info(request):
		return A-name

Il va aussi falloir ajouter la route qui permettra d'utiliser cette fonction :
dans le fichier urls.py

	urlpatterns = [
		...
		path('info', views.info, name='info'),
	]

Maintenant nous allons appeler la fonction précédemment créer au travers de la route défini 'info'.
Dans l'application example l'architecture des urls est la suivante :

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

Donc la route à appeler dans l'application B et la suivante :

	'my-app/info'

Vous pouvez maintenant utiliser la fonction "send_request" du package de l'api manager (documentation : [https://ursi-2020.github.io/technical-base/doc/apimanager.html](https://ursi-2020.github.io/technical-base/doc/apimanager.html))


	A-name = api.send_request('A', 'my-app/info')
