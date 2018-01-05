## Client oauth2 implémenté en python (*Flask*) ##

Le client permet de tester différentes configurations de service et affiche les
attributs retourné par le service en json.

### Configuration des services avec retour de l'ensemble des attributs ###

```json
{
  "@class" : "org.apereo.cas.support.oauth.services.OAuthRegisteredService",
  "clientId": "clientoauth",
  "clientSecret": "passwd",
  "bypassApprovalPrompt": false,
  "serviceId" : "^http://.*:5000/.*",
  "name" : "Python flask",
  "id": 151248298499,
  "description" : "CAS for python flask oauth",
  "attributeReleasePolicy" : {
    "@class" : "org.apereo.cas.services.ReturnAllAttributeReleasePolicy"
  },
  "evaluationOrder" : 99
}

```

Exemple de résultat :

```json
{
  "attributes": {
    "cn": "KOFFI Delphine", 
    "codePostal": "56801", 
    "commonName": "KOFFI Delphine", 
    "displayName": "Delphine KOFFI", 
    "eluCA": "Non", 
    "entreprise": "Environ. 20 PFI", 
    "givenName": "Delphine", 
    "identiteChambre": "CRA53", 
    "localite": "PLOERMEL", 
    "mail": "delphine.koffi@bretagne.chambagri.fr", 
    "mobile": "+33 (0)6 32 85 35 46", 
    "salarieca": "Non", 
    "samlAuthenticationStatementAuthMethod": "urn:oasis:names:tc:SAML:1.0:am:password", 
    "sn": "KOFFI", 
    "typeTiers": "Individu", 
    "uid": "114094"
  }, 
  "id": "114094"
}

```

### Configuration des services avec correspondance des attributs (*MappedAttribute*) ###

```json
{
  "@class" : "org.apereo.cas.support.oauth.services.OAuthRegisteredService",
  "clientId": "clientoauth",
  "clientSecret": "passwd",
  "bypassApprovalPrompt": false,
  "serviceId" : "^http://.*:5000/.*",
  "name" : "Python flask oauth2.0 with mapped attributes",
  "id": 151248298550,
  "description" : "CAS for python flask oauth",
  "attributeReleasePolicy" : {
    "@class" : "org.apereo.cas.services.ReturnMappedAttributeReleasePolicy",
    "allowedAttributes" : {
      "@class" : "java.util.TreeMap",
          "cn" : "affichage",
          "mail" : "courriel",
          "entreprise" : "groovy { return attributes['entreprise'] + ' (' + attributes['cn'] + ')' }"
    }
  },
  "evaluationOrder" : 97
}

```

Exemple de résultat :

```json
{
  "attributes": {
    "affichage": "KOFFI Delphine", 
    "courriel": "delphine.koffi@bretagne.chambagri.fr", 
    "entreprise": "Environ. 20 PFI (KOFFI Delphine)", 
    "samlAuthenticationStatementAuthMethod": "urn:oasis:names:tc:SAML:1.0:am:password"
  }, 
  "id": "114094"
}
```


### Configuration des services avec utilisation d'un script pour les attributs ###

```json
{
  "@class" : "org.apereo.cas.support.oauth.services.OAuthRegisteredService",
  "clientId": "clientoauth",
  "clientSecret": "passwd",
  "bypassApprovalPrompt": false,
  "serviceId" : "^http://.*:5000/.*",
  "name" : "Python flask oauth2.0 with groovy script attributes",
  "id": 151248298560,
  "description" : "CAS for python flask oauth with groovy script attributes",
  "attributeReleasePolicy" : {
    "@class" : "org.apereo.cas.services.GroovyScriptAttributeReleasePolicy",
    "groovyScript" : "/etc/cas/config/attributes.groovy"
  },
  "evaluationOrder" : 95
}

```

Script à placer dans le répertoire de configuration :

```groovy
import java.util.*

class SampleGroovyAPCAAttributeDao {
    def Map<String, List<Object>> run(final Object... args) {
        def currentAttributes = args[0]
        def logger = args[1]

        logger.debug("Current attributes received are {}", currentAttributes)
        return[username:currentAttributes['uid'], complementInfo:["foo", "bar"], affichage:currentAttributes['cn']]
    }
}
```

Pour les tests jouer sur *evaluationOrder*.

Exemple de résultat :

```json
{
  "attributes": {
    "affichage": "KOFFI Delphine", 
    "complementInfo": [
      "bar", 
      "foo"
    ], 
    "samlAuthenticationStatementAuthMethod": "urn:oasis:names:tc:SAML:1.0:am:password", 
    "username": "114094"
  }, 
  "id": "114094"
}
```

### Configuration du LDAP ###

Configuré un repository de la façon suivante :

```properties
##
# CAS Attribute Repository
#
cas.authn.attributeRepository.ldap[0].ldapUrl=ldap://ldap:389/
cas.authn.attributeRepository.ldap[0].useSsl=false
cas.authn.attributeRepository.ldap[0].baseDn=o=tiers
cas.authn.attributeRepository.ldap[0].userFilter=login={user}
cas.authn.attributeRepository.ldap[0].bindDn=cn=Manager,o=tiers
cas.authn.attributeRepository.ldap[0].bindCredential=12345

cas.authn.attributeRepository.ldap[0].attributes.uid=uid
cas.authn.attributeRepository.ldap[0].attributes.displayName=displayName
cas.authn.attributeRepository.ldap[0].attributes.givenName=givenName
cas.authn.attributeRepository.ldap[0].attributes.cn=cn
cas.authn.attributeRepository.ldap[0].attributes.sn=sn
cas.authn.attributeRepository.ldap[0].attributes.mail=mail
cas.authn.attributeRepository.ldap[0].attributes.eluCA=eluCA
cas.authn.attributeRepository.ldap[0].attributes.company=entreprise
cas.authn.attributeRepository.ldap[0].attributes.identitechambre=identiteChambre
cas.authn.attributeRepository.ldap[0].attributes.l=localite
cas.authn.attributeRepository.ldap[0].attributes.postalcode=codePostal
cas.authn.attributeRepository.ldap[0].attributes.salarieca=salarieca
cas.authn.attributeRepository.ldap[0].attributes.typetiers=typeTiers
```

Ceci afin d'y ajouter les attributs souhaités en retour

### Références ###

* http://flask.pocoo.org/
* https://apereo.github.io/cas/5.1.x/integration/Attribute-Release-Policies.html#inline-groovy-attributes
* https://pythonhosted.org/Flask-OAuth/
