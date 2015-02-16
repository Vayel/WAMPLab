**Objectif :** faire des transactions du style MySQL. Par exemple :

* Si ok(A) et ok(B)
    * faire(A)
    * faire(B)
* Faire(C)

**Exemple pris pour le code :** 

Un composant `Data` se charge de manipuler les 
données, partagées avec les autres composants. Ici, il s'agit simplement d'un 
tableau `positions` contenant à l'origine des chaînes de caractères vides : 
`positions = ['', '', '', '']`

Certaines cases ont une certaine propriété : elles sont marquable. Cela est 
enregistré dans ce tableau : `markables = [True, True, False, True]`

Au départ, on se situe à la position 0 : `position = 0`. L'UI est constituée d'un simple 
bouton `Move`, permettant :

* Si la position courante est marquable (`markables[position] is True`) et que 
la position suivante (`positions[position + 1]`) existe :
    * de marquer la position courante (`positions[position] = 'marked'`)
    * d'aller à la position suivante (`position += 1`)
* De faire une autre action bidon (`foo += 1`), peu importe ce qu'il s'est 
passé au-dessus

Par exemple :

Variable | Valeur
---------|-------
position | `0`
markables | `[True, True, False, True]`
positions | `['', '', '', '']`
foo | `0`

Clic sur `Move`.

Variable | Valeur
---------|-------
position | `1`
markables | `[True, True, False, True]`
positions | `['marked', '', '', '']`
foo | `1`

Clic sur `Move`.

Variable | Valeur
---------|-------
position | `2`
markables | `[True, True, False, True]`
positions | `['marked', 'marked', '', '']`
foo | `2`

Clic sur `Move`.

Variable | Valeur
---------|-------
position | `2`
markables | `[True, True, False, True]`
positions | `['marked', 'marked', '', '']`
foo | `3`

Clic sur `Move`.

Variable | Valeur
---------|-------
position | `2`
markables | `[True, True, False, True]`
positions | `['marked', 'marked', '', '']`
foo | `4`

Oui, c'est débile. Mais ça illustre simplement le problème.
