# Transactions

## Objectif

* Faire (A et B)
* Faire C

Au lieu de ça :

* Si peut faire A et peut faire B
    * faire A
    * faire B
* Faire C

Par exemple :

```python
and(
    obj.set_attr1(val1),
    obj.set_attr2(val2, val3)
)

set_attr3(val4)
```

Au lieu de :

```python
if obj.check_attr1(val1) and obj.check_attr2(val2, val3):
    obj.set_attr1(val1)
    obj.set_attr2(val2, val3)
elif not obj.check_attr1(val1):
    raise Exception("Error with attr1")
else:
    raise Exception("Error with attr2")
    
if obj.check_attr3(val4):
    obj.set_attr3(val4)
else:
    raise Exception("Error with attr3")
```

Bien sûr, dans le cadre asynchrone de WAMP.

## Exemple pris pour le code :

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

## Le code

### Version 1

Avec des `if` : verbeux et pas Pythonique.

### Version 2

Avec des `yield` : compliqué.

### Version 3

Avec des `try` : bien, mais il manque une interface pour éviter le code 
spaghetti.
