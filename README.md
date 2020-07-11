## Valknut 0.1.001  -  GSS & SQLite3 manager
  Développé pour Python3 par Meyer Daniel, Juillet 2020
  [voir mon dépôt Github](https://github.com/daniel67-py)
  pour m'écrire : [meyer.daniel67@protonmail.com]

------
#### Sommaire.
+ Présentation du module Valknut et utilité.
+ Fonctions du module Valknut.
+ Exemple d'utilisation de Valknut.
+ Présentation de la classe Valknut_gss et utilité.
+ Fonction principale et syntaxes d'utilisation.
+ Fonctions de la classe Valknut_gss

------
#### Présentation du module Valknut et utilité.
  Le module Valknut pour Python 3 est un framework permettant d'utiliser une base de données de type SQLite3 facilement en économisant des lignes de codes et donc de gagner du temps en intégrant plus facilement ce type de bases dans vos projets et programmes en Python. Il utilise le moteur de template Jinja2 pour la classe Valknut_gss mais pour le reste, il est autonome et n'utilise que des librairies intégrées nativement dans le langage. 
  Son appel depuis un script Python se fait simplement, en utilisant 'from *x* import ...':

    >>> from valknut import *

  Il est possible également de l'utiliser en l'exécutant directement tel un programme.

  Au cas où vous n'avez pas encore Jinja2 intégré dans votre Python, installez le avec la commande suivante :

    pour Linux :
        pip install jinja2
    pour Windows :
        python -m pip install jinja2

  Il est ensuite possible de créer un objet Valknut et ainsi de manipuler la base de données en faisant appel aux fonctions intégrées du module dans sa classe. J'en profite pour préciser que sur une base de données SQLite3, certaines fonctionnalités ne sont pas disponible comme sur une table PostGreSQL ou MySQL. Par exemple: mon module embarque une fonction permettant d'ajouter une colonne dans une table déjà existante tout en se servant d'une requête SQLite, mais aucune fonction permettant de supprimer une colonne. Simplement car une telle opération est impossible à faire sur une table SQLite3 avec une simple requête SQL. Cependant, Valknut contourne le problème en copiant une table existante dans une nouvelle table, tout en sélectionnant les colonnes voulues, et supprime la table d'origine.

------
#### Fonctions du module Valknut.

##### Valknut_new(database)
  Cette fonction permet d'initier une nouvelle base de données en créant un nouveau fichier dont le nom est passé par l'argument *database* . Une fois la base créée, la fonction va retourner un message signalant à l'utilisateur que le fichier disponible.

##### Valknut(database)
  Cette fonction permet d'initier un objet Valknut en faisant appel au fichier passé par l'argument *database* . Il signale à l'utilisateur si la connection à la base de données est opérationnelle ou non. Elle contient aussi deux variables qui influencent les retours que va donner le module :

    .debug_sqlite_instruction = True / False

  True si vous souhaitez que Valknut affiche la requête SQLite utilisée lors de vos opérations, agit comme un mode debug en cas de difficultés à opérer sur la base de données elle même.

    .displaying_line = True / False

  True si vous souhaitez que Valknut affiche (print) les résultats des fonctions de recherches, False si vous souhaitez qu'il les retournent (return).

##### .new_table(table, columns)
  Permet de créer une nouvelle table sans incrémentation automatique dans la base de données. L'argument *table* permet de passer le nom voulu pour la table. L'argument *columns* est un argument multiple permettant de définir les noms des colonnes. Syntaxe d'exemple:

    .new_table('amis', 'nom', 'prenom', 'adresse', 'code_postal', 'ville', 'telephone')

  Ceci va générer une table 'amis' contenant les colonnes qui suivent dans l'ordre : nom, prenom, adresse, code postal, ville, telephone.

##### .new_increased_table(table, columns)
  Permet de créer une nouvelle table avec une incrémentation automatique dans la base de données. L'argument *table* permet de passer le nom voulu pour la table. L'argument *columns* est un argument multiple permettant de définir les noms des colonnes. En plus sera rajouté une colonne 'id' qui s'auto-incrémentera de 1 pour chaque nouvelle entrée ajoutée. Syntaxe d'exemple:

    .new_increased_table('amis', 'nom', 'prenom', 'adresse', 'code_postal', 'ville', 'telephone')

  Ceci va générer une table 'amis' contenant les colonnes qui suivent dans l'ordre : id, nom, prenom, adresse, code postal, ville, telephone.

##### .copy_table(source_table, destination_table)
  Permet de copier une table existante vers une nouvelle table de destination. L'argument *source_table* permet de passer le nom de la table à copier, l'argument *destination_table* permet de donner le nom de la table à créer et à remplir avec la table 'source'.

##### .copy_control_table(source_table, destination_table, columns)
  Permet de copier une table existante vers une nouvelle table de destination en ne tenant compte que de certaines colonnes. L'argument *source_table* permet de passer le nom de la table à copier, l'argument *destination_table* permet de donner le nom de la table à créer et à remplir avec les colonnes passées via l'argument multiple *columns*. Supposons une table 't1' contenant les colonnes 'A', 'B' et 'C', que nous souhaitons copier dans une table 't2' mais en ne tenant compte que des colonnes 'A' et 'C', ceci donnerait :

    .copy_control_table('t1', 't2', 'A', 'C')

##### .redo_table(source_table, columns)
  Permet de retoucher une table en supprimant une ou plusieurs colonnes. Comme je l'expliquais en introduction, SQLite ne permet pas de faire certaines choses comme supprimer une ou plusieurs colonnes. Cette fonction contourne ce manque en copiant la table à modifier dans une table temporaire nommé 'valknut_temporary_table' avec les colonnes que l'on souhaite garder. Elle supprime ensuite la table d'origine, puis en créée une nouvelle portant le même nom qu'elle va remplir avec la table temporaire, avant de supprimer cette dernière. L'argument *source_table* permet de passer le nom de la table à retoucher, l'argument multiple *columns* permet de définir les colonnes que l'on souhaite conserver. Supposons une table 't1' contenant les colonnes 'A', 'B' et 'C', que nous souhaitons retoucher pour ne garder que les colonnes 'A' et 'B', ceci donnerait :

    .redo_table('t1', 'A', 'B')

  Notez que cette fonction se sert des fonctions *delete_table* et *copy_table* du module pour arriver à ses fins.

##### .add_values(table, elements)
  Permet d'ajouter une entrée dans une table non incrémentale. L'argument *table* permet de passer le nom de la table dans laquelle les éléments doivent être ajoutés. L'argument *elements* est un argument multiple permettant de passer les données à inscrire dans la table. Syntaxe d'exemple:

    .add_values('amis', 'dupont', 'maurice', '2 rue des champs', '67000', 'strasbourg', '0609080706')

##### .add_increased_values(table, elements)
  Permet d'ajouter une entrée dans une table auto-incrémentale. L'argument *table* permet de passer le nom de la table dans laquelle les éléments doivent être ajoutés. L'argument *elements* est un argument multiple permettant de passer les données à inscrire dans la table. La colonne 'id' sera renseignée automatiquement. Syntaxe d'exemple:

    .add_increased_values('amis', 'dupont', 'maurice', '2 rue des champs', '67000', 'strasbourg', '0609080706')

##### .modification_values(table, column_to_modify, new_value, reference_column, reference_value)
  Permet de modifier une entrée dans une table en faisant appel à une valeur de référence. L'argument *table* permet de passer le nom de la table dans laquelle l'entrée à modifier se trouve. L'argument *column_to_modify* permet de passer la colonne de la valeur à modifier, *new_value* permet de passer la nouvelle valeur à rentrer dans la colonne. L'argument *reference_column* permet de passer la colonne qui sert de référence d'identification de l'entrée, *reference_value* permet de définir la valeur de la colonne de référence d'identification de l'entrée. Syntaxe d'exemple:

    .modification_values('amis', 'adresse', '4 rue des prairies', 'nom', 'dupont')

  Ceci va modifier dans la table 'amis', la valeur de 'adresse' par '4 rue des prairies', là où la colonne 'nom' vaut 'dupont'. Je précise que dans le cas d'une table auto-incrémentée, il est possible d'utiliser la colonne 'id' pour référence, en précisant l'index de l'entrée que l'on souhaite modifier.

##### .delete_table(table)
  Permet de supprimer une table ainsi que son contenu. L'argument *table* permet de passer le nom de la table que l'on souhaite supprimer.

##### .purge_table(table)
  Permet de supprimer le contenu d'une table sans supprimer la table elle-même, ni ses colonnes. Dans le cas d'une table auto-incrémentée, la numérotation recommencera à zéro. L'argument *table* permet de passer le nom de la table que l'on souhaite purger.

##### .add_column(table, column)
  Permet de rajouter une nouvelle colonne dans une table déjà existante. L'argument *table* permet de passer le nom de la table où l'on souhaite rajouter la colonne, l'argument *column* permet de définir le nom de la colonne à rajouter.

##### .delete_entry(table, column, value)
  Permet de supprimer une entrée dans une table. L'argument *table* permet de passer le nom de la table où se trouve l'entrée à supprimer, l'argument *column* permet de définir le nom de la colonne de référence pour indentifier l'entrée à supprimer, l'argument *value* définit la valeur contenu dans la colonne. Une fois identifié, l'entrée entière est supprimée, et pas juste la valeur de la colonne. Attention cependant, si plusieurs entrées comprennent la même valeur pour cette colonne, elles seront toutes supprimées.

##### .search_seems_like_value(table, column, value)
  Permet de rechercher une ou plusieurs entrées correspondant aux critères de recherche et contenant le caractère ou la suite de caractères spécifié. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line*. Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous la forme d'itérable via une fonction intégrée 'return'.

##### .search_start_like_value(table, column, value)
  Permet de recherche une ou plusieurs entrées correspondant aux critères de recherche et commençant par le caractère ou la suite de caractères spécifié. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line*. Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous la forme d'itérable via une fonction intégrée 'return'.

##### .search_end_like_value(table, column, value)
  Permet de recherche une ou plusieurs entrées correspondant aux critères de recherche et finissant par le caractère ou la suite de caractères spécifié. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line*. Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous la forme d'itérable via une fonction intégrée 'return'.

##### .search_value(table, column, value)
  Permet de rechercher une ou plusieurs entrées correspondant aux critères de recherche. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### .between_value(table, column, interval_1, interval_2)
  Permet de recherche une ou plusieurs entrées se trouvant entre les limites spécifiées. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, l'argument *interval_1* permet de fixer une limite 'basse', l'argument *interval_2* permet de fixer une limite 'haute'. Cette fonction permet d'extraire un groupe de correspondances. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### .not_between_value(table, column, interval_1, interval_2)
  Permet de rechercher une ou plusieurs entrées se trouvant en dehors des limites spécifiées. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, l'argument *interval_1* permet de fixer une limite 'basse', l'argument *interval_2* permet de fixer une limite 'haute'. Cette fonction permet d'extraire un groupe de correspondances. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### .sort_value(table, sens, column)
  Permet d'afficher les entrées d'une table dans par ordre alphabétique ou numérique, de plus petit au plus grand ou inversement. L'argument *table* permet de passer le nom de la table dans laquelle effectuer le tri. L'argument *sens* permet de choisir le sens : 0 pour un sens ascendant, 1 pour un sens descendant. Toutes autres valeurs génère une erreur. L'argument *column* permet de choisir la colonne de référence à utiliser pour effectuer le tri : c'est un argument multiple qui permet de faire un tri sur plusieurs colonnes, dans l'ordre des colonnes spécifiées. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### .return_structure()
  Permet de retourner via une fonction intégrée 'return' la structure de la base de données, sous forme de variable de type 'dictionnaire'.

##### .show_all()
  Permet d'afficher le contenu de la base de données, table par table, en affichant également le nom des colonnes, le tout sous forme d'arborescence.

##### .show_structure()
  Permet d'afficher la structure de la base de données sous forme d'arborescence. Cette fonction se contente de donner le nom des tables et des colonnes.

##### .column_sum(table, column)
  Permet de faire la somme des valeurs contenues dans une colonne et retourne la valeur sous forme de Int ou Float. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer.

##### .column_total(table, column)
  Permet de faire la somme des valeurs contenues dans une colonne et retourne la valeur sous forme de Float. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer.

##### .data_minimal(table, column)
  Permet de trouver la valeur minimale dans la colonne spécifiée. Ceci correspond au nombre le plus faible contenu ou à la première entrée par ordre alphabétique. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer. La fonction retournera la valeur via une fonction intégrée 'return'.

##### .data_maximal(table, column)
  Permet de trouver la valeur maximale dans la colonne spécifiée. Ceci correspond au nombre le plus fort contenu ou à la dernière entrée par ordre alphabétique. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer. La fonction retournera la valeur via une fonction intégrée 'return'.

##### .data_average(table, column)
  Retournera exclusivement la valeur numérique moyenne d'une colonne. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer. La fonction retournera la valeur via une fonction intégrée 'return'.

##### .data_crosscheck(table_1, table_2, column_t1, column_t2)
  Permet d'afficher uniquement les entrées identiques à deux tables distinctes. Les arguments *table_1* et *table_2* permettent de passer le nom des tables à analyser, l'argument *column_t1* permet de définir la colonne de référence de la table_1, l'argument *column_t2* permet de définir la colonne de référence de la table_2. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### .data_union(table_1, table_2)
  Permet d'afficher l'intégralité de deux tables distinctes, sans répéter les doublons. Les arguments *table_1* et *table_2* permettent de définir les deux tables à comparer. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### .edit_structure_txt(nom_fichier_sortie = "analyse_survival.txt")
  Permet d'écrire la structure d'une base de données dans un fichier texte. Par défaut, le fichier se nommera 'analyse_valknut.txt'. Il est possible cependant de changer le nom du fichier de sortie lors de l'appel de la fonction via l'argument *nom_fichier_sortie* .

##### .edit_contains_csv(table, nom_fichier_sortie = "analyse_survival.csv")
  Permet d'écrire le contenu d'une table dans un fichier spreadsheet (type excel). Par défaut, le fichier se nommera 'analyse_valknut.csv'. Il est possible cependant de changer le nom du fichier de sortie lors de l'appel de la fonction via l'argument *nom_fichier_sortie* .

------
#### Exemple d'utilisation de Valknut.
  Après ces quelques lignes de descriptions des fonctionnalités du module, voici un exemple d'utilisation rapide pour la prise en main. Je vais créer une nouvelle base de données que je vais nommer 'exemple.db', et y intégrer deux tables contenant une listes d'amis. Je lance ici le module directement sans l'importer, tel un script, dans l'interpreteur Python.

  Création d'une nouvelle base de données :

    >>> a = Valknut_new('exemple.db')
    ### Valknut - SQLite3 manager ###
    ...verification if access path to file is ok... True
    ...verification if path is a valid file... True
    ...ACCESS DATA OK - NEW DATABASE READY TO OPERATE...

  Accès à ma nouvelle base de données :

    >>> a = Valknut('exemple.db')
    ### Valknut - SQLite3 manager ###
    ...verification if access path to file is ok... True
    ...verification if path is a valid file... True
    ...ACCESS DATAS OK !...

  Je créé deux tables, la première se nommera 'amis_a', la seconde 'amis_b', contenant chacune les :

    >>> a.new_table('amis_a', 'nom', 'prenom', 'age')
    New table create
    True
    >>> a.new_table('amis_b', 'nom', 'prenom', 'age')
    New table create
    True

  Maintenant remplissons un peu les deux tables :

    >>> a.add_values('amis_a', 'dupont', 'maurice', '44')
    True
    >>> a.add_values('amis_a', 'durant', 'jean-jacques', '32')
    True
    >>> a.add_values('amis_a', 'tartenpion', 'didier', '33')
    True
    >>> a.add_values('amis_a', 'jeunot', 'alain', '21')
    True
    >>> a.add_values('amis_b', 'phong', 'lee', '34')
    True
    >>> a.add_values('amis_b', 'sanchez', 'manuella', '29')
    True
    >>> a.add_values('amis_b', 'durant', 'jean-jacques', '32')
    True
    >>> a.add_values('amis_b', 'tartenpion', 'didier', '33')
    True

  Regardons le contenu de notre base de données :

    >>> a.show_all()
    ...OK... The database contains :
    exemple.db
      |
      + - amis_a
      |       \ _ _ _ _ _ ['nom', 'prenom', 'age']
      |		            	 dupont - maurice - 44 - 
      |		            	 durant - jean-jacques - 32 - 
      |	            		 tartenpion - didier - 33 - 
      |		            	 jeunot - alain - 21 - 
      + - amis_b
      |       \ _ _ _ _ _ ['nom', 'prenom', 'age']
      |			             phong - lee - 34 - 
      |	            		 sanchez - manuella - 29 - 
      |		            	 durant - jean-jacques - 32 - 
      |		            	 tartenpion - didier - 33 - 
      | 
      |_ END OF DATAS !

  Ou plus simplement, si je veux connaitre la structure :

    >>> a.show_structure()
    ...OK... This is database's tree :
    exemple.db
      |
      + - amis_a
      |       \ _ _ _ _ _ ['nom', 'prenom', 'age']
      + - amis_b
      |       \ _ _ _ _ _ ['nom', 'prenom', 'age']
      | 
      |_ END OF DATAS !

  Si je veux le contenu des deux tables sans les doublons :

    >>> a.data_union('amis_a', 'amis_b')
    ('dupont', 'maurice', '44')
    ('durant', 'jean-jacques', '32')
    ('jeunot', 'alain', '21')
    ('phong', 'lee', '34')
    ('sanchez', 'manuella', '29')
    ('tartenpion', 'didier', '33')

  Si je veux connaitre les entrées identiques aux deux tables :

    >>> a.data_crosscheck('amis_a', 'amis_b', 'nom', 'nom')
    ('durant', 'jean-jacques', '32', 'durant', 'jean-jacques', '32')
    ('tartenpion', 'didier', '33', 'tartenpion', 'didier', '33')

  Si je veux connaitre les gens trentenaires de la table 'amis_a' :

    >>> a.between_value('amis_a', 'age', 30, 39)
    ('durant', 'jean-jacques', '32')
    ('tartenpion', 'didier', '33')

  Si je veux connaitre les gens non trentenaires de la table 'amis_a' :

    >>> a.not_between_value('amis_a', 'age', 30, 39)
    ('dupont', 'maurice', '44')
    ('jeunot', 'alain', '21')

  Si je souhaite rechercher une personne par son nom :

    >>> a.search_value('amis_b', 'nom', 'sanchez')
    ('sanchez', 'manuella', '29')

  Si je veux lister la table 'amis_a' par ordre alphabétique ascendant, par nom ou par age :

    >>> a.sort_value('amis_a', 0, 'nom')
    ('dupont', 'maurice', '44')
    ('durant', 'jean-jacques', '32')
    ('jeunot', 'alain', '21')
    ('tartenpion', 'didier', '33')

    >>> a.sort_value('amis_a', 0, 'age')
    ('jeunot', 'alain', '21')
    ('durant', 'jean-jacques', '32')
    ('tartenpion', 'didier', '33')
    ('dupont', 'maurice', '44')

  Si je souhaite connaitre la moyenne d'age de la liste 'amis_a' :

    >>> a.data_average('amis_a', 'age')
    32.5

  Si je souhaite modifier une valeur dans une entrée , supposons que je souhaite modifier le 'nom' de 'Phong' en 'Jet', et vérification du résultat :

    >>> a.modification_values('amis_b', 'nom', 'jet', 'nom', 'phong')
    True
    >>> a.show_all()
    ...OK... The database contains :
    exemple.db
      |
      + - amis_a
      |       \ _ _ _ _ _ ['nom', 'prenom', 'age']
      |			             dupont - maurice - 44 - 
      |		            	 durant - jean-jacques - 32 - 
      |		            	 tartenpion - didier - 33 - 
      |		            	 jeunot - alain - 21 - 
      + - amis_b
      |       \ _ _ _ _ _ ['nom', 'prenom', 'age']
      |			             jet - lee - 34 - 
      |	            		 sanchez - manuella - 29 - 
      |		            	 durant - jean-jacques - 32 - 
      |		               	 tartenpion - didier - 33 - 
      | 
      |_ END OF DATAS !

  Si je souhaite supprimer une entrée de la liste 'amis_b' :

    >>> a.delete_entry('amis_b', 'nom', 'tartenpion')
    The value tartenpion from the column nom has been deleted !
    True

  Voilà pour l'aperçu rapide des fonctions.

------
#### Présentation de la classe Valknut_gss et utilité.
  Voilà ici un script basique de mon convertisseur basé sur le markdown en Python. Il est assez simple d'utilisation et me permet de générer une ou plusieurs pages standards html sans trop de fioritures très rapidement. Je l'ai créé pour mon utilisation personnel, et il ne respecte pas totalement les règles du markdown. Certaines sont identiques, d'autres sont propres à ce module. Pour l'intégrer dans vos programmes et scripts Python, il suffit de l'importer comme ceci:

    >>> from valknut import *

  Ce script se sert également de fichiers templates au choix en html. Il y en a trois de disponible dans le dossier /templates. Ils contiennent chacun jusqu'à cinq entrées remplissables par Jinja selon le template. La première est le titre de la page (page_title), la seconde son contenu (page_contains), le troisième est le footer de la page (page_footer), la quatrième remplie automatiquement le sommaire de la colonne à gauche de la page type (page_summary) selon le modèle, et le cinquième permet de remplir le header (page_header). J'ai décidé d'intégrer la dernière version du moteur de templates Jinja2 afin de me simplifier la tache en générant des fichiers statiques tout en utilisant des modèles déjà définis. Il est possible de rajouter des marqueurs Jinja2 directement dans votre fichier markdown, si vous bossez strictement dans un environnement Python et que vous souhaitez créer des pages web dynamiques. Si il n'est pas encore intégré à votre Python, installez le de la manière suivante :

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

  La fonction .generate() lance la convertion du fichier. Par défaut, un fichier nommé 'auto_gen.html' va apparaitre dans le même répertoire que ce script. Cette fonction analyse dans l'ordre : la présence de titres en commençant du type h6 vers le type h1, la présence de séparateurs, la présence d'exemples de codes, la présence de paragraphes, la présence de listes, la présence de triple splats pour mettre certains passage en gras et italique, la présence de double splats afin de mettre certains passages en gras, la présence de single splat pour mettre certains passages en italique. la présence de passage barré, la présence d'images puis de liens hypertext,  et pour finir, fait une indexation des titres balisés dans le corps du document (body), et récupère une liste de ces derniers pour les ajouter comme liens internes dans une colonne dédiée à cet effet (variable page_summary).

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
    ------      6 tirets seuls sur une ligne permettent d'intégrer un séparateur
    *** passage en gras et italique, doit être compris entre deux triple-splats ***
    ** passage en gras, doit être compris entre deux double-splats **
    * passage en italique, doit être compris entre deux single-splat *
    ~~ passage barré, doit être compris entre ces deux symboles ~~
    + en début de ligne génère une liste numérotée
    ++ en début de ligne génère un sous-niveau de liste numérotée
    - en début de ligne génère une liste à puces
    -- en début de ligne génère un sous-niveau de liste à puces
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

##### Fonction détectant les exemple de codes / programmes.
  La seconde fonction **per_coding_example(sequence, number_of_spaces, opening_parse, closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *number_of_spaces* précise le nombre d'espaces vides que la fonction doit trouver avant de réagir et déduire qu'il y a un exemple de code. Dans le script, j'ai posé quatres intervalles vides. Les arguments *opening_parse* et *closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve une ligne qui débute par l'intervalle d'espaces libres spécifiés, et quelle balise de fermeture il faut insérer quand la fonction va trouver une ligne vide à la suite d'un exemple de code.

##### Fonction détectant les listes.
  La troisième fonction **per_list(sequence, begins, opening_parse, closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *begins* précise le symbole à trouver au début d'une ligne et qui va générer une liste à puces ou une liste numérotée. Les arguments *opening_parse* et *closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve un début de liste, et quelle balise de fermeture il faut insérer quand la fonction va trouver une ligne vide à la suite de la liste.

##### Fonction détectant la typographie.
  La quatrième fonction **per_emphasis(sequence, symbol_to_modify, replace_open_parse, replace_closing_parse)** analyse le texte (suite de caractères) passé dans l'argument *sequence*. L'argument *symbol_to_modify* précise le caractère ou la suite de caractères qu'il faut changer. Les arguments *replace_open_parse* et *replace_closing_parse* sont utilisés pour préciser quelle balise d'ouverture il faut insérer au moment où la fonction trouve la première occurence du/des caractère(s), et quelle balise de fermeture il faut insérer à l'occurence suivante du/des caractère(s). Elle est utilisée pour baliser les passages en gras (bold) ou italique (italic) grâce aux double-splats ou single-splat.

##### Notes concernant les listes et la typographie.
  Concernant **per_lines** et **per_emphasis** : j'ai opté pour un fonctionnement de ce genre simplement pour pouvoir les utiliser séparemment, si j'ai besoin de rechercher/remplacer des séquences dans une suite de caractères ou un texte qui n'ont rien à voir avec le balisage markdown, dans un projet futur. 
  Il faut savoir aussi que le programme fait une indexation automatique des titres du document, et récupère ces derniers pour générer automatiquement des liens internes qui seront placés par défaut dans une colonne à gauche de la page.

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
