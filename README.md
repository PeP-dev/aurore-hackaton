# Entr'Act (Hackaton)


## A propos
Ce projet a été réalisé par un groupe d'étudiants de l'IMT Atlantique, en une journée et demi de développement

L'association Aurore proposait dans cet hackaton de développer une site web permettant de proposer une interface
permettant à des utilisateurs (particuliers ou professionnels) de proposer leur logements vacants pour des individus en situation précaire.

Les utilisateurs auraient la possibilité de proposer un logement, tandis que les professionnels peuvent notifier par mail les administrateurs car le processus est plus particulier. 
Mailgun est utilisé pour envoyer les mail. 

Ce site web est un prototype, proposant une page d'accueil de présentation de l'association, 

En pratique, il n'est possible que de créer un compte, proposer un logement en tant que professionnel, 
et visionner ses offres en tant qu'administrateur du site.
## Lancer le serveur 

Pour lancer le serveur, il suffit d'installer les dépendances dans requirements.txt, puis de lancer main.py


## Configuration nécessaire 

Pour avoir un site 'fonctionnel' (ici non terminé), il est nécessaire d'apporter plusieurs clés :

```properties
MAILGUN_API_KEY=MY_API_KEY
MAILGUN_DOMAIN=MY_MAILGUN_DOMAIN.mailgun.org
JWT_SECRET_KEY=JWT_SECRET_KEY
```