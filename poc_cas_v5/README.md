## POC Configuration CAS APCA

Générer une clé (pour le https java)

```
   ${JAVA_HOME}/bin/keytool -genkey -alias cas -keyalg RSA -validity 999 -keystore thekeystore -ext san=dns:localhost
```

Avec Tomcat configurer le server.xml sur le port 8443 avec cette même clé cf.
server.xml ajout de keystoreFile et keystorePass :

```
    <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
               maxThreads="150" SSLEnabled="true" scheme="https" secure="true"
               keystoreFile="/etc/cas/thekeystore" keystorePass="changeit"
               clientAuth="false" sslProtocol="TLS" />
```

Il est nécessaire d'ajouter les certificat au niveau du keystore du JRE dans le
conteneur (TODO vérifier s'il est possible de spécifier un autre chemin au
niveau JVM). Dans le conteneur (ou dans un Dockerfile)

```
   keytool -import -alias cas_docker -keystore /etc/ssl/certs/java/cacerts -file /etc/cas/config/apca_test_docker.crt 

```
PS : obtenir le certificat depuis FF par exemple.

Il est également possible d'utiliser le war auto-executable. cf. composition openjdk

Pour le POC j'ai commencé par un conteneur openjdk Alpine puis je suis passé
sur un conteneur Tomcat afin de déployer la webapps cas-management sur le même
Tomcat (c'est uniquement pour les besoins du POC). 

Pour que cas-management fonctionne il faut mettre à jour son pom.xml (cf.
projet dans gitlab)

## Configurer pom.xml avec les éléments nécessaires

### Remarques sur la version CAS 5.2.0-RC4 / 5.1.5 

Lors des tests nous avons rencontré des dysfonctionnements avec la version
5.2.0-SNAPSHOT (RC4).

Après l'ajout du module cas-server-support-oidc le serveur cas ne démarre plus
sur une erreur de service registry.

Nous avons donc utilisé la version 5.1.5 pour les besoins du POC.


### Ajout de config security (Spring security)

Pour l'accès à /cas/status/

cf. https://apereo.github.io/cas/5.1.x/installation/Monitoring-Statistics.html#spring-security

Ajout support configuration (pour l'accès à /status/)

```
  <dependency>
    <groupId>org.apereo.cas</groupId>
    <artifactId>cas-server-webapp-config-security</artifactId>
    <version>${cas.version}</version>
  </dependency>
```

Ajout des propriétés correpondances dans cas.properties pour définir l'identification basique et un filtre sur IP :

```
    security.basic.enabled=true
    security.basic.realm=CAS
    security.user.name=master
    security.user.password=master
    cas.adminPagesSecurity.ip=172\.17\.0\.[0-9]+
```

### Ajout du support LDAP

```
  <dependency>
     <groupId>org.apereo.cas</groupId>
     <artifactId>cas-server-support-ldap</artifactId>
     <version>${cas.version}</version>
  </dependency>
```

Pour la configuration configuration du LDAP : https://apereo.github.io/2017/03/24/cas51-ldapauthnjasypt-tutorial/
Je n'ai pas encodé le mot de passe

Les propriétés à utiliser pour configurer le LDAP :https://apereo.github.io/cas/5.1.x/installation/Configuration-Properties.html#ldap

```
    cas.authn.ldap[0].type=AUTHENTICATED
    cas.authn.ldap[0].ldapUrl=ldap://ldap:389/
    cas.authn.ldap[0].useSsl=false
    cas.authn.ldap[0].baseDn=ou=Personnes,dc=localhost,dc=localdomain
    cas.authn.ldap[0].userFilter=cn={user}
    cas.authn.ldap[0].bindDn=cn=admin,dc=localhost,dc=localdomain
    cas.authn.ldap[0].bindCredential=12345


```


## Ajout du registry JSON

Ajout du registry JSON (cf. https://apereo.github.io/cas/5.1.x/installation/JSON-Service-Management.html) :

```
  <dependency>
    <groupId>org.apereo.cas</groupId>
    <artifactId>cas-server-support-json-service-registry</artifactId>
    <version>${cas.version}</version>
  </dependency>
```

Récupération des configurations par défaut :

* Apereo-\*.json	      
* HTTPSandIMAPS-\*.json		       
* RegexRegisteredService-\*.json

cas.serviceRegistry.config.location=file:/etc/cas/services



### Ajout du support openid connect

Ajout du support OpenID (cf. https://apereo.github.io/cas/5.1.x/installation/OIDC-Authentication.html):

```
  <dependency>
    <groupId>org.apereo.cas</groupId>
    <artifactId>cas-server-support-oidc</artifactId>
    <version>${cas.version}</version>
  </dependency>
```

Configration oidc :

```
    cas.authn.oidc.issuer=https://localhost:8443/cas/oidc
    cas.authn.oidc.skew=5
    cas.authn.oidc.jwksFile=file:/etc/cas/config/keystore.jwks
```

Pour la génération de keystore.jwks utilisation de https://mkjwk.org/ comme indiqué dans la documentation

Configuration du service pour l'applicationde demo, demoOpenIdConnect-10000.json :
```
    {
      "@class" : "org.apereo.cas.services.OidcRegisteredService",
      "clientId": "client-1",
      "clientSecret": "Password1",
      "serviceId" : "https://localhost:5443/callback",
      "signIdToken": true,
      "implicit": false,
      "name": "demoOpenIdConnect",
      "id": 10000,
      "evaluationOrder": 100,
      "encryptIdToken": false,
      "idTokenEncryptionAlg": "RSA",
      "idTokenEncryptionEncoding": "AQAB"
    }
```

TODO vérifier le fonctionnement de la configuration de jwks au niveau du servvice.


#### PS : générer keystore

```
    /opt/jdk/jdk1.8.0_65/jre/bin/keytool -genkey -alias cas -keyalg RSA -validity 999 -keystore thekeystore -ext san=dns:localhost
```
