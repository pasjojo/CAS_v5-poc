# -*- coding: ISO-8859-1 -*-
#!/usr/bin/env python3

##
# ce script s'occupe d'anonymiser les fichiers LDIF pour les données : nom,
# prenom, courriel, uid, login
#

import re
import hashlib
import csv
import random
try:
    maketrans = str.maketrans
except :
    import string
    maketrans = string.maketrans

# Expression régulière pour identifier un courriel
REGEXP_COURRIEL = re.compile('(.*)@(.*)\.(.*)')
# Domaine utilisé pour anonymiser les courrielrs
DUMMY_DOMAIN = 'yopmail.com'

# Expression régulière générique pour identifier une entrée LDAP dans un
# fichier ldif
REGEXP_LDAP = re.compile('(\w+):(.*)')
# Expression régulière pour le dn de type dn: uid
REGEXP_LDAP_DN = re.compile('(dn: *uid=)(.*?)(,.*)')

##
# Fonction d'anonymisation d'un courriel (fabrique un hash du courriel existant
# et y ajouter le domaine DUMMY_DOMAIN
#
def anonymiserCourriel(p_courriel):
    m = REGEXP_COURRIEL.match(p_courriel)
    if m is not None:
        hash_courriel = hashlib.md5(p_courriel.encode())
        return REGEXP_COURRIEL.sub(hash_courriel.hexdigest()+'@'+DUMMY_DOMAIN, p_courriel)
    else:
        return 'dummy@yopmail.com'
##
# Fonction d'initialisation d'un liste de prénom pour l'anomymisation
# à partir du csv liste_des_prenoms_2004_a_2012.csv cf.
# https://opendata.paris.fr/explore/dataset/liste_des_prenoms_2004_a_2012/
#
def chargerPrenom():
    prenoms = []
    with open('liste_des_prenoms_2004_a_2012.csv') as fd_prenom:
        prenom_reader = csv.reader(fd_prenom, delimiter=';')
        prenoms = [p for p, n, s, a in prenom_reader]
    return prenoms
PRENOMS = chargerPrenom()

##
# Fonction pour charger un corpus de mot à partir de nltk.curpus
# nécessite le package nltk et d'importer le package brown
# nltk.download() et choisir brown
#
def chargerBrown():
    from nltk.corpus import brown
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    mots = {}
    for w in brown.words():
        if len(w) >= 3 :
            wt = tokenizer.tokenize(w)
            if wt != [] and len(wt[0]) >= 3:
                mots[wt[0]] = 1
    return list(mots.keys())
BROWN_CORPUS = chargerBrown()

##
# Fonction d'initialisation d'une liste de lipsum pour les noms
#
def chargerLipsum():
    tr = maketrans('\n.,', '   ')
    mots = []
    with open('lipsum.txt') as fd_lipsum:
        contenu = fd_lipsum.read()
        for m in contenu.split(' '):
            mot = m.translate(tr).strip()
            if mot != '' and len(mot) > 3 and mot not in mots:
                mots.append(mot)
    return mots
LIPSUM = chargerLipsum()

##
# Fonction pour obtenir un mot tiré aléatoirement dans une liste donnée
#
def getMot(p_listeMots, p_unique=False):
    index = random.randint(1, len(p_listeMots))
    mot = p_listeMots[index-1]
    if p_unique:
        del p_listeMots[index-1]
    return mot
        
##
# Fonction d'anoymisation général
#  p_anoObject: objet de type Anonyme() permet d'utiliser les mêmes données nom
#  prenom sur une entrée LDAP
#  p_valeur: la valeur de l'attribut
#  p_type: courriel|nom|prenom|login ou un mix séparé par des espaces :
#  'nom prenom'|'prenom nom'
#
def anonymiserLigne(p_anoObject, p_valeur, p_type):
    if p_type == 'courriel':
        return anonymiserCourriel(p_valeur)
    if p_type == 'nom':
        return p_anoObject.nom
    if p_type == 'prenom':
        return p_anoObject.prenom
    if p_type == 'login':
        return p_valeur.replace(p_valeur[:-4], p_anoObject.nom.lower())
    val = []
    for t in p_type.split(' '):
        val.append(anonymiserLigne(p_anoObject, p_valeur, t))
    return ' '.join(val)

##
# Nom et prenom utilisé pour l'anonymisation d'une entrée LDAP
#
class Anonyme :
    def __init__(self):
        self.nom = getMot(BROWN_CORPUS, p_unique=True).upper()
        self.prenom = getMot(PRENOMS)

   
##
# Anoymiser un fichier LDIF
#
# p_fichierLdif: nom du fichier ldif
# p_champs: dictionnaire conteneur le nom d'attribut ldap à anonymiser et en
# valeur le type (nom|prenom|courriel|login)
# par exemple {'displayName': 'prenom nom', 'sn': 'nom', 'givenName': 'prenom',
# 'mail': 'courriel'}
# 
# le résultat est enregistré dans p_fichierLdif.anonyme
#
def anonymiserLdiff(p_fichierLdif, p_champs):
    attributs = p_champs.keys()

    # Traitement principal   
    with open(p_fichierLdif+'.cache', 'w') as fd_anonyme: 
        with open(p_fichierLdif) as fd_ldiff:
            ano = Anonyme()
            for ligne in fd_ldiff:  
                m = REGEXP_LDAP.match(ligne)
                if m is not None and m.group(1) == 'dn':
                    ano = Anonyme()
                if m is not None and m.group(1) in attributs:    
                    fd_anonyme.write('{}: {}\n'.format(m.group(1), anonymiserLigne(ano, m.group(2), p_champs.get(m.group(1)))))
                else:
                    fd_anonyme.write(ligne)

    # Correctif de l'dn / uid
    with open(p_fichierLdif+'.anonyme', 'w') as fd_final: 
        with open(p_fichierLdif+'.cache', 'r') as fd_anonyme: 
            dn = ''
            uid = ''
            beforeUid = []
            for ligne in fd_anonyme:  
                m = REGEXP_LDAP_DN.match(ligne)
                if m is not None:
                    dn = ligne
                    uid = ''
                else:
                    m = REGEXP_LDAP.match(ligne)
                    if m is not None and m.group(1) == 'uid':
                        uid = m.group(2).strip()
                        fd_final.write(REGEXP_LDAP_DN.sub(r'\g<1>%s\3' %uid , dn))
                        for l in beforeUid:
                            fd_final.write(l)
                        fd_final.write(ligne)
                        beforeUid = []
                    else:
                        if uid == '':
                            beforeUid.append(ligne)
                        else:
                            fd_final.write(ligne)
    
        
                

if __name__ == "__main__":
    print(len(BROWN_CORPUS))
    anonymiserLdiff('prepopulate/11_201711_externes.ldif', {'displayName': 'prenom nom', 'sn': 'nom', 'givenName': 'prenom', 'mail': 'courriel'})
    anonymiserLdiff('prepopulate/12_201711_externes_tmp.ldif', {'displayName': 'prenom nom', 'sn': 'nom', 'givenName': 'prenom', 'mail': 'courriel', 'cn': 'nom prenom', 'login': 'login', 'uid': 'login'})
    anonymiserLdiff('prepopulate/12_201711_externes_tmp.ldif', {'displayName': 'prenom nom', 'sn': 'nom', 'givenName': 'prenom', 'mail': 'courriel', 'cn': 'nom prenom', 'login': 'login', 'uid': 'login'})
    anonymiserLdiff('prepopulate/13_201711_ressources_lilo.ldif', {'displayName': 'prenom nom', 'sn': 'nom', 'givenName': 'prenom', 'mail': 'courriel', 'cn': 'nom prenom', 'login': 'login', 'uid': 'login'})
    anonymiserLdiff('prepopulate/14_201711_internes.ldif', {'displayName': 'prenom nom', 'sn': 'nom', 'givenName': 'prenom', 'mail': 'courriel', 'cn': 'nom prenom', 'login': 'login', 'uid': 'login', 'mailAlias': 'courriel'})
    print(len(BROWN_CORPUS))
