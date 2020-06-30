## Ibex 0.1.a  -  *Ibex & Ibex_gss*
###### Développé pour Python3 par Meyer Daniel, Juin 2020 

------
#### Sommaire.
+ Présentation du module Ibex et utilité.
+ Fonctions du module Ibex.
+ Exemple d'utilisation d'Ibex.

------
#### Présentation du module Ibex et utilité.
Le module Ibex pour Python 3 est un framework permettant d'utiliser une base de données de type SQLite3 facilement en économisant des lignes de codes et donc de gagner du temps en intégrant plus facilement ce type de bases dans vos projets et programmes en Python. Il n'y a pas d'installation particulière pour l'utiliser, comme pour certains modules ou dépendances. Il est autonome et n'utilise que des librairies intégrées nativement dans le langage. 
Son appel depuis un script Python se fait simplement, en utilisant 'import':

    import Ibex

Il est possible également de l'utiliser en l'exécutant directement tel un programme.

Il est ensuite possible de créer un objet Ibex et ainsi de manipuler la base de données en faisant appel aux fonctions intégrées du module dans sa classe. J'en profite pour préciser que sur une base de données SQLite3, certaines fonctionnalités ne sont pas disponible comme sur une table PostGreSQL ou MySQL. Par exemple, mon module embarque une fonction permettant d'ajouter une colonne dans une table déjà existante, mais aucune fonction permettant de supprimer une colonne. Simplement car une telle opération est impossible à faire sur une table SQLite3 avec une simple requête SQL.

------
#### Fonctions du module Ibex.

##### Ibex_new(database)
Cette fonction permet d'initier une nouvelle base de données en créant un nouveau fichier dont le nom est passé par l'argument *database* . Une fois la base créée, la fonction va retourner un message signalant à l'utilisateur une fois le fichier disponible.

##### Ibex(database)
Cette fonction permet d'initier un objet Ibex en faisant appel au fichier passé par l'argument *database* . Il signale à l'utilisateur si la connection à la base de données est opérationnel ou non. Elle contient aussi deux variables qui influencent les retours que va donner le module :

    ibex.debug_sqlite_instruction = True / False

True si vous souhaitez qu'Ibex affiche la requête SQLite utilisée lors de vos opérations, agit comme un mode debug en cas de difficultés à opérer sur la base de données elle même.

    ibex.displaying_line = True / False

True si vous souhaitez qu'Ibex affiche (print) les résultats des fonctions de recherches, False si vous souhaitez qu'Ibex les retournent (return).

##### Ibex.new_table(table, columns)
Permet de créer une nouvelle table sans incrémentation automatique dans la base de données. L'argument *table* permet de passer le nom voulu pour la table. L'argument *columns* est un argument multiple permettant de définir les noms des colonnes. Syntaxe d'exemple:

    ibex.new_table('amis', 'nom', 'prenom', 'adresse', 'code_postal', 'ville', 'telephone')

Ceci va générer une table 'amis' contenant les colonnes qui suivent dans l'ordre : nom, prenom, adresse, code postal, ville, telephone.

##### Ibex.new_increased_table(table, columns)
Permet de créer une nouvelle table avec une incrémentation automatique dans la base de données. L'argument *table* permet de passer le nom voulu pour la table. L'argument *columns* est un argument multiple permettant de définir les noms des colonnes. En plus sera rajouté une colonne 'id' qui s'auto-incrémentera de 1 pour chaque nouvelle entrée ajoutée. Syntaxe d'exemple:

    ibex.new_increased_table('amis', 'nom', 'prenom', 'adresse', 'code_postal', 'ville', 'telephone')

Ceci va générer une table 'amis' contenant les colonnes qui suivent dans l'ordre : id, nom, prenom, adresse, code postal, ville, telephone.

##### Ibex.copy_table(source_table, destination_table)
Permet de copier une table existante vers une nouvelle table de destination. L'argument *source_table* permet de passer le nom de la table à copier, l'argument *destination_table* permet de donner le nom de la table à créer et à remplir avec la table 'source'.

##### Ibex.copy_control_table(source_table, destination_table, columns)
Permet de copier une table existante vers une nouvelle table de destination en ne tenant compte que de certaines colonnes. L'argument *source_table* permet de passer le nom de la table à copier, l'argument *destination_table* permet de donner le nom de la table à créer et à remplir avec les colonnes passées via l'argument multiple *columns*. Supposons une table 't1' contenant les colonnes 'A', 'B' et 'C', que nous souhaitons copier dans une table 't2' mais en ne tenant compte que des colonnes 'A' et 'C', ceci donnerait :

    ibex.copy_control_table('t1', 't2', 'A', 'C')

##### Ibex.redo_table(source_table, columns)
Permet de retoucher une table en supprimant une ou plusieurs colonnes. Comme je l'expliquais en introduction, SQLite ne permet pas de faire certaines choses comme supprimer une ou plusieurs colonnes. Cette fonction contourne ce manque en copiant la table à modifier dans une table temporaire nommé 'ibex_temporary_table' avec les colonnes que l'on souhaite garder. Elle supprime ensuite la table d'origine, puis en créée une nouvelle portant le même nom qu'elle va remplir avec la table temporaire, avant de supprimer cette dernière. L'argument *source_table* permet de passer le nom de la table à retoucher, l'argument multiple *columns* permet de définir les colonnes que l'on souhaite conserver. Supposons une table 't1' contenant les colonnes 'A', 'B' et 'C', que nous souhaitons retoucher pour ne garder que les colonnes 'A' et 'B', ceci donnerait :

    ibex.redo_table('t1', 'A', 'B')

Notez que cette fonction se sert des fonctions *delete_table* et *copy_table* du module pour arriver à ses fins.

##### Ibex.add_values(table, elements)
Permet d'ajouter une entrée dans une table non incrémentale. L'argument *table* permet de passer le nom de la table dans laquelle les éléments doivent être ajoutés. L'argument *elements* est un argument multiple permettant de passer les données à inscrire dans la table. Syntaxe d'exemple:

    ibex.add_values('amis', 'dupont', 'maurice', '2 rue des champs', '67000', 'strasbourg', '0609080706')

##### Ibex.add_increased_values(table, elements)
Permet d'ajouter une entrée dans une table auto-incrémentale. L'argument *table* permet de passer le nom de la table dans laquelle les éléments doivent être ajoutés. L'argument *elements* est un argument multiple permettant de passer les données à inscrire dans la table. La colonne 'id' sera renseignée automatiquement. Syntaxe d'exemple:

    ibex.add_increased_values('amis', 'dupont', 'maurice', '2 rue des champs', '67000', 'strasbourg', '0609080706')

##### Ibex.modification_values(table, column_to_modify, new_value, reference_column, reference_value)
Permet de modifier une entrée dans une table en faisant appel à une valeur de référence. L'argument *table* permet de passer le nom de la table dans laquelle l'entrée à modifier se trouve. L'argument *column_to_modify* permet de passer la colonne de la valeur à modifier, *new_value* permet de passer la nouvelle valeur à rentrer dans la colonne. L'argument *reference_column* permet de passer la colonne qui sert de référence d'identification de l'entrée, *reference_value* permet de définir la valeur de la colonne de référence d'identification de l'entrée. Syntaxe d'exemple:

    ibex.modification_values('amis', 'adresse', '4 rue des prairies', 'nom', 'dupont')

Ceci va modifier dans la table 'amis', la valeur de 'adresse' par '4 rue des prairies', là où la colonne 'nom' vaut 'dupont'. Je précise que dans le cas d'une table auto-incrémentée, il est possible d'utiliser la colonne 'id' pour référence, en précisant l'index de l'entrée que l'on souhaite modifier.

##### Ibex.delete_table(table)
Permet de supprimer une table ainsi que son contenu. L'argument *table* permet de passer le nom de la table que l'on souhaite supprimer.

##### Ibex.purge_table(table)
Permet de supprimer le contenu d'une table sans supprimer la table elle-même, ni ses colonnes. Dans le cas d'une table auto-incrémentée, la numérotation recommencera à zéro. L'argument *table* permet de passer le nom de la table que l'on souhaite purger.

##### Ibex.add_column(table, column)
Permet de rajouter une nouvelle colonne dans une table déjà existante. L'argument *table* permet de passer le nom de la table où l'on souhaite rajouter la colonne, l'argument *column* permet de définir le nom de la colonne à rajouter.

##### Ibex.delete_entry(table, column, value)
Permet de supprimer une entrée dans une table. L'argument *table* permet de passer le nom de la table où se trouve l'entrée à supprimer, l'argument *column* permet de définir le nom de la colonne de référence pour indentifier l'entrée à supprimer, l'argument *value* définit la valeur contenu dans la colonne. Une fois identifié, l'entrée entière est supprimée, et pas juste la valeur de la colonne. Attention cependant, si plusieurs entrées comprennent la même valeur pour cette colonne, elles seront toutes supprimées.

##### Ibex.search_seems_like_value(table, column, value)
Permet de rechercher une ou plusieurs entrées correspondant aux critères de recherche et contenant le caractère ou la suite de caractères spécifié. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line*. Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous la forme d'itérable via une fonction intégrée 'return'.

##### Ibex.search_start_like_value(table, column, value)
Permet de recherche une ou plusieurs entrées correspondant aux critères de recherche et commençant par le caractère ou la suite de caractères spécifié. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line*. Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous la forme d'itérable via une fonction intégrée 'return'.

##### Ibex.search_end_like_value(table, column, value)
Permet de recherche une ou plusieurs entrées correspondant aux critères de recherche et finissant par le caractère ou la suite de caractères spécifié. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line*. Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous la forme d'itérable via une fonction intégrée 'return'.

##### Ibex.search_value(table, column, value)
Permet de rechercher une ou plusieurs entrées correspondant aux critères de recherche. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, et l'argument *value* permet de définir la valeur qui nous intéresse. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction 'print' intégrée à Python, si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### Ibex.between_value(table, column, interval_1, interval_2)
Permet de recherche une ou plusieurs entrées se trouvant entre les limites spécifiées. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, l'argument *interval_1* permet de fixer une limite 'basse', l'argument *interval_2* permet de fixer une limite 'haute'. Cette fonction permet d'extraire un groupe de correspondances. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### Ibex.not_between_value(table, column, interval_1, interval_2)
Permet de rechercher une ou plusieurs entrées se trouvant en dehors des limites spécifiées. L'argument *table* permet de passer le nom de la table dans laquelle effectuer la recherche, l'argument *column* permet de définir la colonne de recherche, l'argument *interval_1* permet de fixer une limite 'basse', l'argument *interval_2* permet de fixer une limite 'haute'. Cette fonction permet d'extraire un groupe de correspondances. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### Ibex.sort_value(table, sens, column)
Permet d'afficher les entrées d'une table dans par ordre alphabétique ou numérique, de plus petit au plus grand ou inversement. L'argument *table* permet de passer le nom de la table dans laquelle effectuer le tri. L'argument *sens* permet de choisir le sens : 0 pour un sens ascendant, 1 pour un sens descendant. Toutes autres valeurs génère une erreur. L'argument *column* permet de choisir la colonne de référence à utiliser pour effectuer le tri : c'est un argument multiple qui permet de faire un tri sur plusieurs colonnes, dans l'ordre des colonnes spécifiées. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### Ibex.return_structure()
Permet de retourner via une fonction intégrée 'return' la structure de la base de données, sous forme de variable de type 'dictionnaire'.

##### Ibex.show_all()
Permet d'afficher le contenu de la base de données, table par table, en affichant également le nom des colonnes, le tout sous forme d'arborescence.

##### Ibex.show_structure()
Permet d'afficher la structure de la base de données sous forme d'arborescence. Cette fonction se contente de donner le nom des tables et des colonnes.

##### Ibex.column_sum(table, column)
Permet de faire la somme des valeurs contenues dans une colonne et retourne la valeur sous forme de Int ou Float. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer.

##### Ibex.column_total(table, column)
Permet de faire la somme des valeurs contenues dans une colonne et retourne la valeur sous forme de Float. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer.

##### Ibex.data_minimal(table, column)
Permet de trouver la valeur minimale dans la colonne spécifiée. Ceci correspond au nombre le plus faible contenu ou à la première entrée par ordre alphabétique. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer. La fonction retournera la valeur via une fonction intégrée 'return'.

##### Ibex.data_maximal(table, column)
Permet de trouver la valeur maximale dans la colonne spécifiée. Ceci correspond au nombre le plus fort contenu ou à la dernière entrée par ordre alphabétique. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer. La fonction retournera la valeur via une fonction intégrée 'return'.

##### Ibex.data_average(table, column)
Retournera exclusivement la valeur numérique moyenne d'une colonne. L'argument *table* permet de spécifier la table, l'argument *column* permet de spécifier la colonne sur laquelle opérer. La fonction retournera la valeur via une fonction intégrée 'return'.

##### Ibex.data_crosscheck(table_1, table_2, column_t1, column_t2)
Permet d'afficher uniquement les entrées identiques à deux tables distinctes. Les arguments *table_1* et *table_2* permettent de passer le nom des tables à analyser, l'argument *column_t1* permet de définir la colonne de référence de la table_1, l'argument *column_t2* permet de définir la colonne de référence de la table_2. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### Ibex.data_union(table_1, table_2)
Permet d'afficher l'intégralité de deux tables distinctes, sans répéter les doublons. Les arguments *table_1* et *table_2* permettent de définir les deux tables à comparer. Cette fonction réagit avec la variable *displaying_line* . Si cette dernière vaut True, l'affichage se fera via une fonction intégrée 'print', si elle vaut False, la fonction retournera le résultat sous forme d'itérable via une fonction intégrée 'return'.

##### Ibex.edit_structure_txt(nom_fichier_sortie = "analyse_ibex.txt")
Permet d'écrire la structure d'une base de données dans un fichier texte. Par défaut, le fichier se nommera 'analyse_ibex.txt'. Il est possible cependant de changer le nom du fichier de sortie lors de l'appel de la fonction via l'argument *nom_fichier_sortie* .

##### Ibex.edit_contains_csv(table, nom_fichier_sortie = "analyse_ibex.csv")
Permet d'écrire le contenu d'une table dans un fichier spreadsheet (type excel). Par défaut, le fichier se nommera 'analyse_ibex.csv'. Il est possible cependant de changer le nom du fichier de sortie lors de l'appel de la fonction via l'argument *nom_fichier_sortie* .

------
#### Exemple d'utilisation d'Ibex.
Après ces quelques lignes de descriptions des fonctionnalités du module Ibex, voici un exemple d'utilisation rapide pour la prise en main. Je vais créer une nouvelle base de données que je vais nommer 'exemple.db', et y intégrer deux tables contenant une listes d'amis. Je lance ici le module directement sans l'importer, tel un script, dans l'interpreteur Python.

Création d'une nouvelle base de données :

    >>> a = Ibex_new('exemple.db')
    ###      Ibex - SQLite3 operative Framework     ###
    ### dev. by Meyer Daniel, June 2020 - ver.0.1.a ###
    ...verification if access path to file is ok... True
    ...verification if path is a valid file... True
    ...ACCESS DATA OK - NEW DATABASE READY TO OPERATE...

Accès à ma nouvelle base de données :

    >>> a = Ibex('exemple.db')
    ###      Ibex - SQLite3 operative Framework     ###
    ### dev. by Meyer Daniel, June 2020 - ver.0.1.b ###
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


------
#### Mot de fin.
Voilà dans les grandes lignes, la base de l'utilisation du module Ibex. Des modifications vont suivre pour améliorer son fonctionnement. Je les posent ici en opensource pour tous. Pour toutes suggestions ou idées, envoyer moi un mail à l'adresse ci-dessous. Je peux également vous faire un programme opensource en Python intégralement pour exploiter une base de données SQLite3 avec interface Tkinter, il suffit pour cela de me contacter via le mail ici présent, ou par Telegram.

    email : meyer.daniel67@protonmail.com
    telegram : @Daniel_85

Merci de respecter le travail fourni ici, et l'origine de celui-ci. Merci également à vous si vous utilisez mes scripts et qu'ils vous aident à arriver à vos fins.

Daniel.



