## Valknut 0.1.001  - WSGI Local Server, GSS & SQLite3 manager
  Développé pour Python3 par Meyer Daniel, Juillet 2020
  [voir mon dépôt Github](https://github.com/daniel67-py)
  pour m'écrire : [meyer.daniel67@protonmail.com]

------
#### Sommaire.
+ Présentation de la classe Valknut_gss et utilité.
+ Fonction principale et syntaxes d'utilisation.
+ Fonctions de la classe Valknut_gss

------
#### Présentation de la classe Valknut_gss et utilité.
  Voilà ici un script basique de mon convertisseur basé sur le markdown, en Python. Il est assez simple d'utilisation et me permet de générer une ou plusieurs pages standards html sans trop de fioritures très rapidement. Je l'ai créé pour mon utilisation personnel, et il ne respecte pas totalement les règles du markdown. Certaines sont identiques, d'autres sont propres à ce module. Pour l'intégrer dans vos programmes et scripts Python, il suffit de l'importer comme ceci:

    >>> from valknut import *

  Ce script se sert également de fichiers templates au choix en html. Il y en a trois de disponible dans le dossier /templates. Ils contiennent chacun jusqu'à cinq entrées remplissables par Jinja selon le template. La première est le titre de la page (page_title), la seconde son contenu (page_contains), le troisième est le footer de la page (page_footer), la quatrième remplie automatiquement le sommaire de la colonne à gauche de la page type (page_summary) selon le modèle, et le cinquième permet de remplir le header (page_header). Il y a également une quatrième template nommé 'index.html' qui est utilisé par la classe Valknut_Server et qui permet à cette dernière de générer la page de la racine du server. Elle contient une entrée spécifique (page_index) qui retourne par défaut une liste des fichiers markdowns disponibles dans le dossier /container. Pour plus d'info, voir la documentation de la classe Valknut_Server.
  J'ai décidé d'intégrer la dernière version du moteur de templates Jinja2 afin de me simplifier la tache en générant des fichiers statiques tout en utilisant des modèles déjà définis. Il est possible de rajouter des marqueurs Jinja2 directement dans votre fichier markdown, si vous bossez strictement dans un environnement Python et que vous souhaitez créer des pages web dynamiques. Si il n'est pas encore intégré à votre Python, installez le de la manière suivante :

    sous Linux:
        pip install jinja2
    sous Windows:
        python -m install jinja2

  Pour voir le résultat avant/après : le fichier README.md contient le texte brute balisé en markdown, le fichier auto_gen.html est le résultat généré par mon script. La commande utilisée pour le générer sous Python, avec mon script a été :

    >>> convert = Valknut_gss()
    >>> convert.file = "README.md"
    >>> convert.generate()

  Aussi 'simple' que ça...

  J'ai également intégré un petit interface graphique Tkinter qui s'affiche si vous lancez le programme directement. La classe qui le contient se nomme Valknut_gss_interface() et permet de renseigner les mêmes éléments que la classe Valknut_gss(). Simple, rapide, efficace, pas prise de tête... Pâté cornichons en clair !

##### Classe principale, le point d'entrée pour l'utilisateur.
  La classe principale **Valknut_gss()** permet de créer un objet Valknut_gss et de lui définir le fichier à convertir (.file), le type de feedback (.feedback), le nom du fichier de sortir (.out_file), le titre de la page (.project_title), le contenu du header (.project_header), le contenu du footer (.project_footer) et le template à utiliser (.use_template). 

  La fonction .generate() lance la convertion du fichier. Par défaut, un fichier nommé 'auto_gen.html' va apparaitre dans le même répertoire que ce script. Cette fonction analyse dans l'ordre : la présence de titres en commençant du type h6 vers le type h1, la présence de séparateurs, la présence d'exemples de codes, la présence de paragraphes, la présence de listes, la présence de triple splats pour mettre certains passage en gras et italique, la présence de double splats afin de mettre certains passages en gras, la présence de single splat pour mettre certains passages en italique. la présence de passage barré, la présence d'images puis de liens hypertext, et pour finir, fait une indexation des titres balisés dans le corps du document (body), et récupère une liste de ces derniers pour les ajouter comme liens internes dans une colonne dédiée à cet effet (variable page_summary).

  Concernant les listes, et sachant que j'utilise toujours un modèle de document très basique quand j'écris un contenu, si elles sont insérées grâce à des signes +, elles seront numérotées, et seront à puces si utilisation du signe -. Valknut gère actuellement les listes standards avec un seul niveau inférieur de listes.

  Il faut savoir aussi que la variable feedback est optionnel : si elle n'est pas spécifiée, elle vaudra 0, et donc le retour se fera dans le fichier 'auto_gen.html'. Si par contre elle est différente de 0, le retour se fera via une fonction intégrée 'return' sous la forme d'une suite de caractères. Ceci peut être intéressant si vous souhaitez transmettre (retourner) directement au CGI un fichier markdown, sans créer le moindre fichier html. Ceci peut être utile si vous utiliser un framework du genre flask ou cherrypy, sans devoir se soucier d'un contenu autre que des fichiers markdown ou texte.

  Les variables *project_title, project_header et project_footer* permettent de personnaliser le titre, le header et le footer de la page que votre navigateur va afficher dans l'onglet. Par défaut, ce sera dans l'ordre : 'knut_page', 'knut_header', 'knut_footer', mais il suffit de spécifier d'autre valeurs lors de la définition de l'objet pour les changer.

  Il faut également savoir que la variable *out_file* est aussi optionnelle : si feedback vaut 0, le retour sera enregistré dans le fichier dont le nom est passé dans cet argument, par défaut 'auto_gen.html'.

  De façon simple, voilà comment poser les symboles dans votre fichier markdown ou texte:

    ###### titre en taille h6 à gauche de la page
    ##### titre en taille h5 à gauche de la page
    #### titre en taille h4 à gauche de la page
    ### titre en taille h3 à gauche de la page
    ## titre en taille h2 à gauche de la page
    # titre en taille h1 à gauche de la page
    ------ 6 tirets seuls sur une ligne permettent d'intégrer un séparateur
    *** passage en gras et italique, doit être compris entre deux triple-splats ***
    ** passage en gras, doit être compris entre deux double-splats **
    * passage en italique, doit être compris entre deux single-splat *
    ~~ passage barré, doit être compris entre deux symboles d'approximation ~~
    __ passage souligné, doit être compris entre deux double-underscore __
    + en début de ligne génère une liste numérotée
    ++ en début de ligne génère un sous-niveau de liste numérotée (la limite actuelle est à 15 niveaux)
    +++ etc...
    - en début de ligne génère une liste à puces
    -- en début de ligne génère un sous-niveau de liste à puces (la limite actuelle est à 15 niveaux)
    --- etc...
    [lien vers un site](http://www.adresse_du_site.com)  pour intégrer un lien vers un site
    ![image à insérer](chemin_vers_image.jpeg)  pour intégrer une image
    [adresse.messagerie@email.com]  pour intégrer un lien vers un mail
    pour définir un paragraphe, laissez 2 espaces libres à son début
    et si vous laissez 4 espaces vides en début de ligne, survivaltool_gss génère un exemple de code comme ces quelques lignes de syntaxes.

  La fonction principale utilise neuf autres fonctions afin de créer le balisage dans le texte. Ceci me permet de pouvoir adapter ce petit programme facilement si je souhaite m'en servir pour chercher d'autres suites de caractères et leur attribuer des valeurs différentes.

------
#### Fonctions de la classe Valknut_gss.
##### Fonction détectant les titres et les séparateurs.
  La première fonction **per_lines(sequence, symbol_to_modify, replace_open_parse, replace_closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *symbol_to_modify* précise le caractère ou la suite de caractères qu'il faut changer. Les arguments *replace_open_parse* et *replace_closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut inserer au moment où la fonction trouve la première occurence du/des caractère(s), et quelle balise de fermeture il faut insérer avant le retour à la ligne. Elle est utilisée pour baliser les titres dans un document si elle trouve un sharp ou une suite de sharps au début d'une ligne et ne réagit qu'à cette condition.
  Il faut savoir aussi que le programme fait une indexation automatique des titres du document, et récupère ces derniers pour générer automatiquement des liens internes qui seront placés par défaut dans une colonne à gauche de la page. 

##### Fonction détectant les exemple de codes / programmes.
  La seconde fonction **per_coding_example(sequence, number_of_spaces, opening_parse, closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *number_of_spaces* précise le nombre d'espaces vides que la fonction doit trouver avant de réagir et déduire qu'il y a un exemple de code. Dans le script, j'ai posé quatres intervalles vides. Les arguments *opening_parse* et *closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve une ligne qui débute par l'intervalle d'espaces libres spécifiés, et quelle balise de fermeture il faut insérer quand la fonction va trouver une ligne vide à la suite d'un exemple de code.

##### Fonction détectant les listes.
  La troisième fonction **per_list(sequence, begins, opening_parse, closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *begins* précise le symbole à trouver au début d'une ligne et qui va générer une liste à puces ou une liste numérotée. Les arguments *opening_parse* et *closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve un début de liste, et quelle balise de fermeture il faut insérer quand la fonction va trouver une ligne vide à la suite de la liste. Valknut permet de faire une arborescence allant jusqu'à 15 niveaux (voir les fichiers essai.md et essai.html pour se faire une idée). Cependant il vaut mieux utiliser qu'un seul type de puces pour les arborescences complexes à plusieurs niveaux, sous peine de générer une ou plusieurs erreurs.

##### Fonction détectant la typographie.
  La quatrième fonction **per_emphasis(sequence, symbol_to_modify, replace_open_parse, replace_closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *symbol_to_modify* précise le caractère ou la suite de caractères qu'il faut changer. Les arguments *replace_open_parse* et *replace_closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve la première occurence du/des caractère(s), et quelle balise de fermeture il faut insérer à l'occurence suivante du/des caractère(s). Elle est utilisée pour baliser les passages en gras (bold), italique (italic), barrés (strikethrough) ou soulignés (underline) grâce aux divers caractères clés.

##### Notes concernant les listes et la typographie.
  Concernant **per_lines** et **per_emphasis** : j'ai opté pour un fonctionnement de ce genre simplement pour pouvoir les utiliser séparemment, si j'ai besoin de rechercher/remplacer des séquences dans une suite de caractères ou un texte qui n'ont rien à voir avec le balisage markdown, dans un projet futur. 

##### Fonctions détectant les urls, les images et les emails.
  La cinquième fonction **per_links(sequence)** analyse le texte (suite de caractères) passé dans l'argument *sequence* et pose les liens hypertext.
  La sixième fonction **per_images(sequence)** analyse le texte (suite de caractères) passé dans l'argument *sequence* et intègre les liens vers les images souhaitées.
  La septième fonction **per_mails(sequence)** analyse le texte (suite de caractères) passé dans l'argument *sequence* et intègre les liens vers les adresses emails.
  Notez que les images insérées seront automatiquement centrées sur la page du navigateur si vous utilisez les templates propres à Valknut.

##### Fonction d'indexation du document.
  La huitième fonction **indexer(sequence)** analyse le texte passé dans l'argument *sequence* et modifie toutes les balises de titres html *<h.>* en y intégrant un id suivi d'un numéro unique incrémenté de 1 à chaque titre. Ceci commence à 0 (premier titre trouvé) et fini au dernier titre trouvé.
  Notez que l'id de la balise header est automatiquement 'home' si vous utilisez les templates propres à Valknut.

##### Fonction de récupération des titres.
  La neuvième fonction **chapter(sequence)** analyse le texte passé dans l'argument *sequence* et récupère le contenu des balises de titres du document. Ceci est la seule fonction qui ne modifie pas le document final, elle ne s'occupe que de collecter les données relatives aux titres et leur numéro d'index afin de créer et retourner une liste de liens internes, qui sera intégrée dans le rendu final (à condition bien sûr d'utiliser l'un des deux templates que j'ai mis à disposition, ou d'en créer un qui tient compte de ce paramètre).

------
#### Mot de fin.
  Voilà dans les grandes lignes, la base de l'utilisation du module Valknut et de ses classes Valknut et Valknut_gss. Des modifications vont suivre pour améliorer son fonctionnement. Je les posent ici en opensource pour tous. Pour toutes suggestions ou idées, envoyer moi un mail à l'adresse ci-dessous. Je peux également vous faire un programme opensource en Python intégralement pour exploiter une base de données SQLite3 avec interface Tkinter, il suffit pour cela de me contacter via le mail ici présent, ou par Telegram.

    email : meyer.daniel67@protonmail.com
    telegram : @Daniel_85

  Merci de respecter le travail fourni ici, et l'origine de celui-ci. Merci également à vous si vous utilisez mes scripts et qu'ils vous aident à arriver à vos fins.

------
  Daniel. Juillet 2020.
