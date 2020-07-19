## Valknut 0.1.001  - WSGI Local Server, GSS & SQLite3 manager
  Développé pour Python3 par Meyer Daniel, Juillet 2020
  [voir mon dépôt Github](https://github.com/daniel67-py)
  pour m'écrire : [meyer.daniel67@protonmail.com]

------
#### Sommaire.
+ Présentation de la classe Valknut_Server et utilité.
+ Fonctions de la classe Valknut_Server.
+ Exemple d'utilisation de Valknut_Server.

------
#### Présentation de la classe Valknut_Server et utilité.
  Valknut intègre un module qui permet de créer un serveur WSGI (Web Service Gateway Interface) et ainsi de générer un petit serveur en réseau local. Ne pas l'utiliser comme serveur de production car il est vraiment très basique et permet surtout de vérifier le rendu d'un projet utilisant Valknut. Pour l'importer :

    >>> from valknut_server import *

  Il utilise la bibliothèque wsgiref intégrée dans Python 3 nativement, et utilise le module Valknut_gss pour afficher ses propres pages. De ce fait, Jinja2 se trouve chargé également car utilisé dans le module Valknut_gss. 

#### Fonctions de la classe Valknut_Server().
  Par défaut, son mode de débugage est désactivé et le port d'émission est le 8008. Pour l'utiliser, il suffit de créer un objet.

    >>> s = Valknut_Server()

  Pour utiliser le mode de débugage ou non, il suffit de spécifier à cet objet True pour l'activer, False pour de désactiver :

    >>> s.debuging = True ( ou False )

  Il est possible également de changer le port de communication, comme ceci :

    >>> s.port = 7777 ( ou n'importe quel nombre entier compris entre 1024 et 65535 )

  Pour lancer le serveur, il suffit de taper la commande suivante :

    >>> s.serve_now()

  Et le programme se lance... Pour l'arrêter, il suffira d'appuyer sur la combinaison de touches Ctrl+C dans le shell Python le concernant. De base, il mettra automatiquement en ligne les fichiers markdown se trouvant dans le dossier /container et affichera la liste des documents consultables si vous tapez dans la bar d'url de votre navigateur : localhost:8008/ .
  Si tout se passe bien, un message apparaîtra à cette page, et une liste si votre dossier contient quelquechose. De base, la documentation de Valknut se trouve dedans.
  Il est possible également de lui définir des pages manuellements grâce à la fonction .transmission . Elle s'utilise de cette manière:

    >>> s.transmission(path = "/salut", contains = "Hello world et salut à tous !")

  Ce qui aura pour effet de créer un embranchement sur localhost:8008/salut qui retournera le message passé ici dans l'argument *contains*. L'argument *path* définissant quant à lui le chemin de l'embranchement.

#### Exemple d'utilisation de la classe Valknut_Server().
  Voici un petit exemple rapide pour donner une idée de ce qu'il est possible de faire. Je vais créer un petit serveur. Il suffit de lancer le shell Python et de lui donner quelques instructions :

    >>> from valknut_server import *
    >>> s = Valknut_Server()
    >>> s.transmission(path = "/salut", contains = "Salut à tous !")
    >>> s.transmission(path = "/hello", contains = "Hello world !")
    >>> s.serve_now()

  Ces quelques instructions vont générer un serveur. Une fois lancée, allez dans votre navigateur et tapez dans la bar d'url : 

    localhost:8008/salut

  Le message propre à cette page apparaît.
  Ensuite, allez à l'url suivante :

    localhost:8008/hello

  Le message propre à cette page apparaît également.
  Si vous tapez un mauvais url, Valknut va afficher une petite page d'erreur disant qu'il ne connait pas ce chemin. Et si vous tapez simplement :

    localhost:8008/

  Une page de base va apparaître faisant la liste des documents disponibles dans le dossier 'container'.
  
  Et voilà.

------
#### Mot de fin.
  Voilà dans les grandes lignes, la base de l'utilisation du module Valknut et de ses classes Valknut_sqlite, Valknut_gss et Valknut_Server. Des modifications vont suivre pour améliorer son fonctionnement. Je tiens à préciser que j'ai monté ce projet en partant de zéro, juste par passion d'essayer de comprendre comment tout ceci peut fonctionner, par challenge personnel, et par envie de reconversion professionnelle. Je précise également que je suis auto-didacte en programmation et que je n'ai aucun cursus scolaire lié à cette activité (à la base je suis technicien usineur/tourneur-fraiseur, niveau bac, travaillant en usine depuis presque vingt ans). 

  Je pose ici mes modules en opensource pour tous. Pour toutes suggestions ou idées, envoyer moi un mail à l'adresse ci-dessous. Je peux également vous faire un programme opensource en Python intégralement pour exploiter une base de données SQLite3 avec interface Tkinter, il suffit pour cela de me contacter via le mail ici présent, ou par Telegram.

    email : meyer.daniel67@protonmail.com
    telegram : @Daniel_85

  Merci de respecter le travail fourni ici, et l'origine de celui-ci. Merci également à vous si vous utilisez mes scripts et qu'ils vous aident à arriver à vos fins.

------
  Daniel. Juillet 2020.
