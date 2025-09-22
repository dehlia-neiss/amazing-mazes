# 🌀 Amazing Mazes

## 📌 Contexte du projet
Ce projet a pour objectif de générer et résoudre des labyrinthes de différentes tailles en utilisant plusieurs algorithmes classiques.  
L'idée est d'étudier leurs performances (temps d'exécution et mémoire utilisée) et de comparer leurs comportements selon la taille du labyrinthe.  

Le travail se divise en deux grandes parties :
- **Génération de labyrinthes** avec différents algorithmes.
- **Résolution de labyrinthes** avec plusieurs stratégies de recherche de chemin.

---

## ⚙️ Algorithmes utilisés

### 🔨 Génération
- **Kruskal** : basé sur les ensembles disjoints (Union-Find), garantit un labyrinthe parfait (un seul chemin entre deux cases).  
- **Backtracking (Recursive Backtrack)** : construit un chemin en profondeur puis revient en arrière lorsqu’il est bloqué.  

### 🧭 Résolution
- **DFS (Depth-First Search)** : exploration en profondeur, efficace mais peut explorer de nombreux chemins inutiles et ne peut pas explorer de trop grand labyrinthe.  
- **A*** : algorithme heuristique utilisant une fonction de coût (distance de Manhattan) pour accélérer la recherche du chemin optimal.  

---

## 📊 Données collectées

Nous avons mesuré pour chaque taille :
- ⏱️ Temps de génération
- ⏱️ Temps de résolution
- 💾 Mémoire utilisée (Ko)
- 📈 Pic mémoire (Ko)

### Résultats comparatifs

| Taille | ⏱️ Génération (Backtracking) | ⏱️ Génération (Kruskal) | ⏱️ Résolution (DFS) | ⏱️ Résolution (A*) | 💾 Mémoire utilisée | 📈 Pic mémoire |
|--------|-------------------------------|-------------------------|---------------------|-------------------|---------------------|---------------|
| 50     | —                             | 0.1187 sec              | 0.2535 sec          | 0.1052 sec        | 456.42 Ko           | 1025.21 Ko    |
| 100    | —                             | 0.3968 sec              | 0.0913 sec          | 0.6616 sec        | 1762.10 Ko          | 4176.35 Ko    |
| 250    | —                             | 2.3850 sec              | 9.1930 sec          | 8.2508 sec        | 17315.04 Ko         | 30866.13 Ko   |
| 500    | —                             | 16.7519 sec             | 58.2133 sec         | 50.5008 sec       | 80165.21 Ko         | 135454.54 Ko  |
| 1000   | —                             | 61.9247 sec             | 237.8936 sec        | 197.0364 sec      | 304497.98 Ko        | 525305.95 Ko  |
| 1500   | —                             | 133.1448 sec            | ❌ Trop long         | 536.3469 sec      | 774571.48 Ko        | —             |
| 2000   | —                             | 290.8975 sec            | ❌ Trop long         | 726.8774 sec      | 1173335.06 Ko       | —             |

---

## 🔎 Analyse

- **Kruskal** : très performant sur les petites tailles, mais sa complexité augmente fortement avec la taille du labyrinthe.  
- **DFS** : fonctionne bien jusqu’à ~250 cases, mais explose en temps au-delà de 500 cases (trop long dès 1500).  
- **A*** : reste plus efficace que DFS sur les grandes tailles grâce à l’heuristique, mais consomme beaucoup de mémoire.  
- **Backtracking (génération)** : efficace mais non testé à grande échelle dans cette campagne de mesures.  

---

## ✅ Conclusion

Ce projet nous a permis de :
- Implémenter et comparer différents algorithmes classiques de **génération** et **résolution** de labyrinthes.
- Observer concrètement l’impact de la **complexité algorithmique** sur les performances.
- Constater que :
  - **DFS** est simple mais peu scalable.
  - **A*** est plus adapté aux grands labyrinthes.
  - **Kruskal** est un bon choix pour générer des labyrinthes mais devient coûteux sur des tailles très grandes.

👉 Pour de futures améliorations, on pourrait tester :
- Des algorithmes de génération plus rapides (**Prim**, **division récursive**).
- Des algorithmes de résolution plus optimisés (**Dijkstra**, **Bidirectional Search**).
- Une visualisation graphique pour suivre l’évolution en temps réel.

---
