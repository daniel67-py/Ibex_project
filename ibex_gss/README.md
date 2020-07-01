## Ibex 0.1.a  -  *Ibex & Ibex_gss*
###### Développé pour Python3 par Meyer Daniel, Juin 2020 

------
#### Sommaire.
+ Présentation du module Ibex_gss et utilité.
+ Fonction principale et syntaxes d'utilisation.
+ Fonctions du module Ibex_gss
+ Mot de fin

------
#### Présentation du module Ibex_gss et utilité.
Voilà ici un script basique de mon convertisseur basé sur le markdown en Python. Il est assez simple d'utilisation et me permet de générer une page standard html sans trop de fioritures très rapidement. Je l'ai créé pour mon utilisation personnel, et il ne respecte pas totalement les règles du markdown. Certaines sont identiques, d'autres sont propres à ce module. Les fichiers 'mode_emploi.txt' et 'ibex_gss.html' illustrent ces quelques lignes d'explications pour vous montrer ce qu'il est possible de faire : le fichier texte contient le texte brute avec les balises de mise en forme, le fichier html retourne le résultat après traitement.

Ce module se sert également de deux fichiers .html et un fichier .css contenu dans le dossier *ibex_ressources*. Le fichier *ibex_gss_head.html* contient une en-tête type html, le fichier *ibex_gss_foot.html* contient un pied de page type en html, et le fichier *ibex_gss.css* contient le script css utilisé pour la mise en forme du document. Ils sont accessibles et modifiables pour l'utilisateur.


##### Fonction principale, le point d'entrée pour l'utilisateur.
La fonction principale **ibex_gss('nom_du_fichier', feedback = 0, out_file = 'ibex_gss.html')** lance la convertion du fichier passé en argument, et un fichier nommé 'ibex_gss.html' va apparaitre dans le même répertoire que ce script. Cette fonction analyse dans l'ordre : la présence de titres en commençant du type h6 vers le type h1, la présence de séparateurs, la présence d'exemples de codes, la présence de listes, la présence de double splats afin de mettre certains passages en gras, et pour finir la présence de single splat pour mettre certains passages en italique.
Concernant les listes, et sachant que j'utilise toujours un modèle de document très basique quand j'écris un contenu, si elles sont insérées grâce à des signes +, elles seront numérotées, et seront à puces si utilisation du signe -.

Il faut savoir aussi que l'argument feedback est optionnel : si il n'est pas spécifié, il vaudra 0, et donc le retour se fera dans le fichier 'ibex_gss.html'. Si par contre il est différent de 0, le retour se fera via une fonction intégrée 'return' sous la forme d'une suite de caractères. Ceci peut être intéressant si vous souhaitez transmettre (retourner) directement au CGI un fichier markdown, sans passer par un fichier html.

Il faut également savoir que l'argument out_file est aussi optionnel : par défaut, si feedback vaut 0, le retour sera enregistré dans le fichier dont le nom est passé dans cet argument.

De façon simple, voilà comment poser les symboles dans votre fichier markdown ou texte:

    ###### titre en taille h6 à gauche de la page
    ##### titre en taille h5 à gauche de la page
    #### titre en taille h4 à gauche de la page
    ### titre en taille h3 à gauche de la page
    ## titre en taille h2 à gauche de la page
    # titre en taille h1 à gauche de la page
    >###### titre en taille h6 centré sur la page
    >##### titre en taille h5 centré sur la page
    >#### titre en taille h4 centré sur la page
    >### titre en taille h3 centré sur la page
    >## titre en taille h2 centré sur la page
    ># titre en taille h1 centré sur la page
    ------      6 tirets seuls sur une ligne permettent d'intégrer un séparateur
    ***passage en gras et italique, doit être compris entre deux triple-splats***
    **passage en gras, doit être compris entre deux double-splats**
    *passage en italique, doit être compris entre deux single-splat*
    + en début de ligne génère une liste numérotée
    - en début de ligne génère une liste à puces
    [+url]www.adresse_url.com[+url+]lien_vers_adresse[url+] pour intégrer un lien vers un site
    [+img]image_a_integrer.jpeg[img+]
    et si vous laissez 4 espaces vides en début de ligne, ibex_gss génère un exemple de code 
    comme ces quelques lignes de syntaxes.
    [HDR+] ... [+HDR] pour définir le contenu de l'en-tête de votre document.
    [BDY+] ... [+BDY] pour définir le contenu du corps de votre document.
    [FTR+] ... [+FTR] pour définir le contenu du pied de page de votre document.

La fonction principale utilise cinq autres fonctions afin de créer le balisage dans le texte. Ceci me permet de pouvoir adapter ce petit programme facilement si je souhaite m'en servir pour chercher d'autres suites de caractères et leur attribuer des valeurs différentes.

------
#### Fonctions du module Ibex_gss.
##### Fonction détectant les titres et les séparateurs.
La première fonction **per_lines(sequence, symbol_to_modify, replace_open_parse, replace_closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *symbol_to_modify* précise le caractère ou la suite de caractères qu'il faut changer. Les arguments *replace_open_parse* et *replace_closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut inserer au moment où la fonction trouve la première occurence du/des caractère(s), et quelle balise de fermeture il faut insérer avant le retour à la ligne. Elle est utilisée pour baliser les titres dans un document si elle trouve un sharp ou une suite de sharps au début d'une ligne et ne réagit qu'à cette condition.

##### Fonction détectant les exemple de codes / programmes.
La seconde fonction **per_coding_example(sequence, number_of_spaces, opening_parse, closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *number_of_spaces* précise le nombre d'espaces vides que la fonction doit trouver avant de réagir et déduire qu'il y a un exemple de code. Dans le script, j'ai posé quatres intervalles vident. Les arguments *opening_parse* et *closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve une ligne qui débute par l'intervalle d'espaces libres spécifiés, et quelle balise de fermeture il faut insérer quand la fonction va trouver une ligne vide à la suite d'un exemple de code.

##### Fonction détectant les listes.
La troisième fonction **per_list(sequence, begins, opening_parse, closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *begins* précise le symbole à trouver au début d'une ligne et qui va générer une liste à puces ou une liste numérotée. Les arguments *opening_parse* et *closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve un début de liste, et quelle balise de fermeture il faut insérer quand la fonction va trouver une ligne vide à la suite de la liste.

##### Fonction détectant la typographie.
La quatrième fonction **per_emphasis(sequence, symbol_to_modify, replace_open_parse, replace_closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *symbol_to_modify* précise le caractère ou la suite de caractères qu'il faut changer. Les arguments *replace_open_parse* et *replace_closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve la première occurence du/des caractère(s), et quelle balise de fermeture il faut insérer à l'occurence suivante du/des caractère(s). Elle est utilisée pour baliser les passages en gras (bold) ou italique (italic) grâce aux double-splats ou single-splat.

##### Note :
Concernant **per_lines** et **per_emphasis** : j'ai opté pour un fonctionnement de ce genre simplement pour pouvoir les utiliser séparemment, si j'ai besoin de rechercher/remplacer des séquences dans une suite de caractères ou un texte qui n'ont rien à voir avec le balisage markdown, dans un projet futur. 

##### Fonction détectant les urls et images.
>>> La cinquième fonction **per_links(sequence, symbol_to_modify, replace_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *symbol_to_modify* précise le caractère ou la suite de caractères qu'il faut changer. L'argument *replace_parse* permet de définir la balise à intégrer à la place. Petit rappel pour intégrer un lien vers une page internet quelconque, ou simplement insérer une image, il vous faudra utiliser les balises suivantes comme ceci : 

    [+url]adresse_url_du_lien[+url+]texte_lien[url+]
    [+img]image_à_insérer[img+]

>>> Notez que les images insérées seront automatiquement centrées sur la page du navigateur. Cependant ce module ne gère pas encore la création de tableaux. Je planche dessus pour ajouter des nouvelles fonctionnalitées.

------
#### Mot de fin.
Voilà dans les grandes lignes, la base de l'utilisation du module Ibex_gss. Des modifications vont suivre pour améliorer son fonctionnement. Je les posent ici en opensource pour tous. Pour toutes suggestions ou idées, envoyer moi un mail à l'adresse ci-dessous. Je peux également vous faire un programme opensource en Python intégralement pour exploiter une base de données SQLite3 avec interface Tkinter, il suffit pour cela de me contacter via le mail ici présent, ou par Telegram.

    email : meyer.daniel67@protonmail.com
    telegram : @Daniel_85

Merci de respecter le travail fourni ici, et l'origine de celui-ci. Merci également à vous si vous utilisez mes scripts et qu'ils vous aident à arriver à vos fins.

------

Daniel. Juillet 2020.


