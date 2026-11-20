# 💡 Exemples d'utilisation - Chatbot ENSAJ

Ce fichier contient des exemples de questions à poser au chatbot pour tester ses capacités.

## 🎓 Questions académiques

### Informations générales
```
Q: Qu'est-ce que l'ENSAJ ?
Q: Où se trouve l'ENSAJ ?
Q: Quelle est l'université de tutelle ?
```

### Filières et formations
```
Q: Quelles sont les filières disponibles ?
Q: Parle-moi de la filière ISIC
Q: Quelle est la différence entre Génie Informatique et ISIC ?
Q: Combien d'années dure le cycle ingénieur ?
```

### Admission et inscription
```
Q: Comment s'inscrire à l'ENSAJ ?
Q: Quels sont les critères d'admission ?
Q: Y a-t-il un cycle préparatoire ?
Q: Quand ouvrent les inscriptions ?
```

## 📞 Questions pratiques

### Contact
```
Q: Comment contacter l'administration ?
Q: Quel est le numéro de téléphone de l'ENSAJ ?
Q: Quelle est l'adresse email de l'école ?
Q: Où est située l'école exactement ?
```

### Campus et services
```
Q: Y a-t-il une bibliothèque ?
Q: Quels sont les services disponibles sur le campus ?
Q: Y a-t-il un restaurant universitaire ?
```

## 🛠️ Tests des outils

### Outil de recherche documentaire
```
Q: Cherche des informations sur les stages en entreprise
Q: Trouve-moi le règlement intérieur
Q: Quels sont les horaires des cours ?
```

### Outil de calcul
```
Q: Calcule 25 * 48 + 120
Q: Combien font 1500 / 6 ?
Q: Quel est le résultat de 100 - 35 + 12 ?
```

### Outil d'informations statiques
```
Q: Donne-moi les coordonnées de l'ENSAJ
Q: Liste toutes les filières
Q: Quels sont les cycles de formation ?
```

## 🧠 Tests du mode Agent

### Questions nécessitant plusieurs outils
```
Q: Cherche dans les documents le coût de la scolarité et calcule le total pour 3 ans
Q: Trouve les filières disponibles et donne-moi le contact pour plus d'infos
Q: Recherche les conditions d'admission et calcule combien de places il y a au total
```

### Questions avec raisonnement
```
Q: Si je veux faire de l'intelligence artificielle, quelle filière devrais-je choisir ?
Q: Combien de temps faut-il au total pour obtenir le diplôme d'ingénieur en partant de zéro ?
Q: Quelles sont les différences entre le cycle préparatoire intégré et les autres prépas ?
```

## 📚 Tests de recherche dans les documents

### Recherche spécifique
```
Q: Cherche des informations sur le projet de fin d'études (PFE)
Q: Trouve le règlement concernant les absences
Q: Quelles sont les modalités d'évaluation ?
Q: Y a-t-il des informations sur les bourses ?
```

### Recherche contextuelle
```
Q: Comment se déroule l'année académique ?
Q: Quels sont les débouchés après le diplôme ?
Q: Y a-t-il des partenariats avec des entreprises ?
Q: Quelles sont les activités extra-scolaires ?
```

## 🎯 Tests de précision

### Questions pièges (pour tester les limites)
```
Q: Quelle est la météo à El Jadida aujourd'hui ?
   → Devrait dire qu'il n'a pas cette info dans les documents

Q: Qui est le président de la France ?
   → Devrait dire que ce n'est pas dans les documents ENSAJ

Q: Recommande-moi un restaurant à El Jadida
   → Devrait rester dans le contexte ENSAJ
```

### Questions ambiguës
```
Q: C'est où exactement ?
   → Devrait demander de préciser

Q: Combien ça coûte ?
   → Devrait demander de quoi on parle

Q: Quand est-ce que ça commence ?
   → Devrait demander de clarifier
```

## 🔄 Tests de conversation

### Suivi de contexte
```
Q1: Parle-moi de la filière Génie Informatique
Q2: Combien d'années dure cette formation ?
Q3: Quels sont les débouchés ?
```

### Questions enchaînées
```
Q1: Quelles sont toutes les filières ?
Q2: Décris la première
Q3: Et la deuxième ?
```

## 🌟 Cas d'usage réels

### Étudiant potentiel
```
Q: Je viens d'avoir mon bac en sciences maths, puis-je m'inscrire à l'ENSAJ ?
Q: Je m'intéresse à l'informatique et les réseaux, quelle filière choisir ?
Q: Y a-t-il des frais de scolarité ?
```

### Étudiant actuel
```
Q: Où puis-je trouver le planning des examens ?
Q: Quelles sont les règles concernant les rattrapages ?
Q: Comment faire une demande de stage ?
```

### Parent
```
Q: Mon fils veut devenir ingénieur en génie civil, est-ce possible à l'ENSAJ ?
Q: Quelle est la réputation de l'école ?
Q: Y a-t-il un internat ou des résidences étudiantes ?
```

## 📊 Évaluation de performance

### Mesures de qualité

Pour chaque question, évaluer :

1. **Pertinence** : La réponse est-elle pertinente ?
2. **Exactitude** : Les informations sont-elles correctes ?
3. **Complétude** : La réponse est-elle complète ?
4. **Sources** : Les sources sont-elles citées ?
5. **Clarté** : La réponse est-elle claire et bien structurée ?

### Grille d'évaluation

| Critère | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ |
|---------|---------|-------|------|----|----|
| Pertinence | Très pertinent | Pertinent | Moyennement pertinent | Peu pertinent | Pas pertinent |
| Exactitude | 100% correct | Quelques erreurs mineures | Erreurs notables | Plusieurs erreurs | Faux |
| Complétude | Très complet | Complet | Manque quelques détails | Incomplet | Très incomplet |

## 🔧 Paramètres à tester

### Température

Tester la même question avec différentes températures :

**Question** : "Décris la filière ISIC"

- Temperature 0.0 : Réponse très déterministe
- Temperature 0.3 : Réponse équilibrée (défaut)
- Temperature 0.7 : Réponse plus créative
- Temperature 1.0 : Réponse très créative/variée

### Mode Agent vs Simple

Comparer les deux modes sur la même question complexe :

**Question** : "Cherche les conditions d'admission et calcule le nombre total de places disponibles"

- Mode Agent : Devrait utiliser plusieurs outils
- Mode Simple : Pourrait avoir du mal avec le calcul

## 📝 Notes pour les tests

### Avant de tester

- [ ] Base vectorielle chargée
- [ ] Mode sélectionné (Agent ou Simple)
- [ ] Température configurée
- [ ] PDFs pertinents dans le dossier data/

### Pendant les tests

- Noter les questions qui échouent
- Observer les étapes de raisonnement (mode Agent)
- Vérifier les sources citées
- Mesurer le temps de réponse

### Après les tests

- Documenter les problèmes rencontrés
- Identifier les améliorations possibles
- Ajuster les prompts si nécessaire
- Ajouter plus de documents si manque d'information

## 🎯 Objectifs de test

### Test de base ✅
- [ ] Connexion Ollama OK
- [ ] Base vectorielle chargée
- [ ] Question simple réussie
- [ ] Sources affichées

### Test intermédiaire ✅
- [ ] Questions sur plusieurs filières
- [ ] Utilisation de la calculatrice
- [ ] Recherche multi-documents
- [ ] Contexte conversationnel maintenu

### Test avancé ✅
- [ ] Questions nécessitant raisonnement
- [ ] Utilisation de plusieurs outils en chaîne
- [ ] Gestion d'ambiguïté
- [ ] Réponses sur documents longs

Bonne exploration ! 🚀
