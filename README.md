# 🧩 Projet Labyrinthe — Génération et Résolution

## 🎯 Contexte du projet
L’objectif de ce projet est de comparer différentes approches d’algorithmes pour :
1. **Générer un labyrinthe** (via Kruskal ou Backtracking).  
2. **Résoudre un labyrinthe** (via DFS ou A\*).  

Nous avons implémenté et testé ces méthodes sur des labyrinthes de tailles variées afin d’analyser :
- Leur **temps d’exécution** ⏱️
- Leur **consommation mémoire** 💾
- Leur **scalabilité** 📈

---

## ⚙️ Algorithmes utilisés

### 🔨 Génération
- **Kruskal** : basé sur les ensembles disjoints, il construit un labyrinthe par connexions progressives des cellules.  
- **Backtracking** : explore de manière récursive pour creuser des chemins aléatoires, avec retour arrière lorsqu’aucune avancée n’est possible.

### 🚪 Résolution
- **DFS (Depth First Search)** : explore les chemins en profondeur, pas forcément optimal.  
- **A\* (A star)** : algorithme heuristique basé sur une fonction de coût `f(n) = g(n) + h(n)`, garantissant le chemin optimal.

---

## 📊 Résultats expérimentaux

### Comparaison des méthodes

| Taille | ⏱️ Génération (Kruskal) | ⏱️ Résolution (A\*) Kruskal | 💾 Mémoire (Ko) | ⏱️ Génération (Backtracking) | ⏱️ Résolution (A\*) Backtracking |
|--------|--------------------------|-----------------------------|--------------|-------------------------------|----------------------------------|
| 50     | 0.1187 sec              | 0.1052 sec                 | 456.42         | 0.0200 sec                   | 0.0553 sec                      |
| 100    | 0.3968 sec              | 0.6616 sec                 | 1762.10        | 0.0333 sec                   | 0.0304 sec                      |
| 250    | 2.3850 sec              | 8.2508 sec                 | 17315.04       | 0.4175 sec                   | 0.4106 sec                      |
| 500    | 16.7519 sec             | 50.5008 sec                | 80165.21       | 2.1185 sec                   | 1.2173 sec                      |
| 1000   | 61.9247 sec             | 197.0364 sec               | 304497.98      | 8.5226 sec                   | 3.9869 sec                      |
| 1500   | 133.1448 sec            | 536.3469 sec               | 774571.48      | 9.1704  sec                  |  5.3558 sec          |
| 2000   | 290.8975 sec            | 726.8774 sec               | 1173335.06     | 28.5364 sec                  | 28.1403 sec                     |
| 3000   | -                        | -                           | -            | 76.7569 sec                  | 75.6274 sec                     |

---

## 🔎 Analyse des résultats

- **Kruskal + A\*** :  
  - Plus lent pour la génération car basé sur un algorithme global avec gestion d’ensembles disjoints.  
  - Consomme énormément de mémoire sur de grandes tailles (jusqu’à **1.1 Go à 2000**).  
  - Résolution A\* reste optimale mais coûteuse en temps.  

- **Backtracking + A\*** :  
  - Génération beaucoup plus rapide, même sur de grandes tailles.  
  - Résolution A\* très efficace, avec des temps bien plus faibles que la combinaison Kruskal.  
  - Pas de surcharge mémoire excessive.  

---

## ✅ Conclusion

- La combinaison **Backtracking + A\*** est la plus efficace en pratique :  
  - Temps de génération et de résolution bien meilleurs.  
  - Scalabilité plus adaptée aux grandes tailles.  

- La combinaison **Kruskal + A\***, bien que correcte, souffre d’un **temps de calcul** et d’une **consommation mémoire** trop importants pour les labyrinthes de grande taille.  

👉 En résumé : **Backtracking + A\*** est le meilleur choix pour générer et résoudre efficacement des labyrinthes.  

