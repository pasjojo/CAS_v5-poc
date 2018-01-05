## Apache 2.4 php 5.6 et mod_auth_cas

### Construire l'image 

```
docker build -t apca/apache-cas-client:1.1 .
```

### Démarrer le conteneur

```
docker run --name apache-cas-2 apca/apache-cas-client:1.1 --rm
```

### Accéder au conteneur en HTTP :

La commande suivante utilise l'inspection du conteneur `docker inspect` pour
obtenir l'adresse IP de ce dernier. L'option --format permet de filter le
résultat et de formater l'affichage.

```
docker inspect --format='http://{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' apache-cas-2
```

ou

```
docker inspect --format='http://{{.NetworkSettings.Networks.bridge.IPAddress}}' apache-cas-2
```

