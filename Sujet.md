# Sujet 2 : Un jeu de carte en ligne - Texas Hold Em Poker : Client / Serveur

Le principe de ce sujet est d’implémenter un jeu de poker bien connu : le texas hold’em - https://en.wikipedia.org/wiki/Texas_hold_%27em

Le principe de ce projet repose sur l’utilisation de l’api documentée ici: https://deckofcardsapi.com/ Cette API met a disposition des decks de 52 de cartes classiques. Elle propose également de nombreuses opérations détaillées dans la documentation.

Cela permet de ne pas avoir a redévelopper toute la logique de tirage de cartes et de distribution.

>    Pour pimenter votre application vous pouvez bien évidemment utiliser plusieurs paquets, les mélanger les remettre a zéro comme vous le souhaitez

---

## Concept

Le Texas Hold em est une variante du poker très populaire et vous souhaitez en implémenter un jeu.

A partir d’un tirage de 2 cartes, chaque joueur décide ou non de s’engager dans la manche en misant des jetons.

Au cours d’une manche, chaque joueur peut miser

Il existe 5 manches de mise en suite, avec la révelation de cartes supplémentaires (et la destruction):

*   1 manche après la distribution des 2 cartes propres a chaque joueur.

>   Puis distribution de 3 cartes communes a chaque joueur (flop)

*   1 manche de mise

>   Puis distribution d'1 carte avant la manche suivante (river)

*   1 manche de mise

>   Puis distribution d'1 carte avant la derniere phase d’enchère (turn)

*   1 manche de mise

>   Révélation des cartes des joueurs restant et attribution des jetons.

Pour chaque manche, il faut que les joueurs (qui sont encore en lice) misent, suivent, checksi il n’y a pas de mise ou quittent la table

A la fin de la dernière manche on révèle les cartes des joueurs

Les joueurs seront sauvegardés avec leurs jetons, parties en cours, dans la base de données. Les parties permettent de retrouver les jetons de chaque joueur dans la partie et les différentes mènes. Les mênes contiennent les cartes. Les cartes contiennent des valeur, couleur, joueur et une référence a la mêne.

---

## Technique

*   Ce sujet est plus classique mais il est pertinent d’expérimenter avec SQLAlchemy / Django les différents types de drivers de base de données. En effet, il est plus pratique de travailler avec une base de donnée locale simple type SQLite.

>   Remarque: il est attendu que suite a la documentation pour démarrer l’application, la base de données soit prête a l’utilisation (donc script sql ou commandes spécifiques attendues)

*   Il est proposé deux architectures cible : soit une application web (site web avec backend intégré) donc en utilisant django. Soit une application client serveur avec une API pour gérer le jeu et l’état du jeu et la création d’un client (soit un client ligne de commande (que vous connaissez), soit un site web, soit un client python ex tkinter)

---

## Attendus de test

Il est ici attendu de tester différentes mains face a d’autres mains et de s’assurer que la règle de calcul pour la victoire est bien vérifiée.
