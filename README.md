Guillaume TARPIN-BERNARD / Charles CARRERE
# Sujet : Un jeu de carte en ligne - Texas Hold Em Poker

  
## Quickstart
```bash
git clone https://github.com/KioKah/texas-hold-em
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
L'interface est accessible à l'adresse http://127.0.0.1:8000/ 

## Description 
### Généralités 
L'objectif principal de ce projet de jeu de poker Texas Hold'em en ligne est de fournir une plateforme interactive où les joueurs peuvent participer à des parties de poker.

Le jeu est conçu pour simuler l'expérience du poker Texas Hold'em, en respectant ses règles traditionnelles.
### Organisation du Code
Le code est organisé autour d'une architecture modulaire qui sépare clairement la logique du jeu, la gestion des utilisateurs, et l'interface utilisateur. Ceci est réalisé à travers l'utilisation du framework Django,
#### Applications
##### authentication
Gere la creation des comptes et l'authentifications des utilisateurs
##### holdem
Gere la table de poker en elle meme

#### Modules
L'arborescence des modules est celle traditionnellement utilisée pour les projets Django
Dans ce projet, le coeur du code se situe dans les vues et le module game dans l'application holdem.

### Fonctionnement général du code
#### La base de données
(voir diagramme de classes base de données)
La base de données est composée des différentes tables nécessaires au fonctionnement de Django et de deux classe qui nous sont utiles pour l'application
##### User
Nous utilisons la table User de base de Django que nous surchargeons pour nos besoin 
###### Round
Nous stockons les données des rounds qui nous permettent de faire avancer le jeu

#### Logique
La logique est gérée dans les views, en particulier celle de l'application holdem
Lorsque l'utilisateur charge la page home, il déclenche l'execution du code de cette vue sur le serveur.
Le code vérifie alors l'état du user et du round en cours dans la base de données et le fait évoluer en fonction de cet état et des actions utilisateurs
La logique propre au jeu est implémenté dans le module game.

  

## Diagramme de classe

  
### La base de données
```mermaid

---

title: Texas Hold'em

---

classDiagram

direction LR

User "2..10" <-- "*" Round : is played by

class User{

int id

str name

str password

int chips

int bet

int total_bet

str hand

str action

date last_action

int order

}

class Round{

int id

str community_cards

ManyToManyRelationship players

int player_to_play

int stage

int pot

int blind

int min_raise

str winners_name

str winner_hand

}

```
### Les classes métier
```mermaid
classDiagram

class  Card  {

-value:  str

-suit:  str

-code:  str

-image:  str

-name:  str

-unicode:  str

+__init__(value:  str, suit:  str, code:  str, image:  str)

+from_deck_of_cards_api(api_dict:  dict):  Card

+from_code(code:  str):  Card

+from_code_string(code_string:  str):  List[Card]

+__eq__(other:  Card):  bool

+__ne__(other:  Card):  bool

+__str__():  str

+__repr__():  str

}

  

class  Deck  {

-deck_id:  Optional[str]

+__init__(deck_id:  Optional[str])

+new_deck()

+draw(count:  int):  List[Card]

+shuffle()

+__str__():  str

+__repr__():  str

}

  

class  FinalHandPower{

<<enumeration>>

HIGH_CARD

ONE_PAIR

TWO_PAIRS

THREE_OF_A_KIND

STRAIGHT

FLUSH

FULL_HOUSE

FOUR_OF_A_KIND

STRAIGHT_FLUSH

ROYAL_FLUSH

}

  

class  FinalHand  {

-cards:  List[Card]

-power:  int

-value:  List[str]

-suit:  Optional[str]

-name:  str

+__init__(cards:  List[Card], hand_power:  FinalHandPower, suit:  str)

+name():  str

+compare(other:  FinalHand):  int

+__ge__(other):  bool

+__gt__(other):  bool

+__le__(other):  bool

+__lt__(other):  bool

+__eq__(other):  bool

+__ne__(other):  bool

+__str__():  str

}

  

class  Hand  {

-cards:  List[Card]

-sep_suits:  dict

-sep_values:  dict

-final_hand:  FinalHand

+__init__(cards:  List[Card])

+separate_by_suits():  dict

+separate_values():  dict

+detect_royal_flush():  Optional[FinalHand]

+detect_straight_flush():  Optional[FinalHand]

+detect_four_of_a_kind():  Optional[FinalHand]

+detect_full_house():  Optional[FinalHand]

+detect_flush():  Optional[FinalHand]

+detect_straight():  Optional[FinalHand]

+detect_three_of_a_kind():  Optional[FinalHand]

+detect_two_pairs():  Optional[FinalHand]

+detect_one_pair():  Optional[FinalHand]

+detect_high_card():  FinalHand

+detect_final_hand():  FinalHand

+__str__():  str

}

  

Card  --|>  FinalHand

Deck  "1"  --  "*"  Card  :  contains

FinalHand  "*"  --  "1"  FinalHandPower  :  has

Hand  "*"  --  "1..*"  Card  :  contains

Hand  "1"  --  "1"  FinalHand  :  has
```
  
  

## Scénario d'Utilisation : 
1. Inscription sur la page dédiée
2. Connexion 
3. Arrivée dans un round vide
	1. Attente jusqu'à l'arrivée d'un deuxième joueur
	2. lancement de la partie
4.  Arrivée lors d'un round en cours
	1. Jouer le prochain round
5. Jouer la partie à l'aide de l'interface

## Tests
### Application
Pour tester plusieurs profils en même temps et jouer contre vous-même, vous pouvez utiliser le mode incognito ou une extension comme Firefox Multi-Account Containers.

### Lancement des tests pour le calcul des meilleures mains
``` bash
python3 test_hand.py
```
