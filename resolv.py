import heapq
import time
import tracemalloc
import sys

WALL = "#"
OPEN = "."

# ===================== Conversion / Affichage =====================
def maze_to_ascii(maze):
    """Accepte 0/1 ou déjà ASCII ; renvoie ASCII #/."""
    out = []
    for row in maze:
        new_row = []
        for cell in row:
            if cell in (1, "#"):
                new_row.append("#")
            else:
                new_row.append(".")
        out.append(new_row)
    return out

def ascii_to_binary(ascii_maze):
    """'#' -> 1 (mur), '.' -> 0 (ouvert)"""
    return [[1 if ch == "#" else 0 for ch in row] for row in ascii_maze]

def print_ascii(ascii_maze):
    for row in ascii_maze:
        print("".join(row))

def print_maze_with_path(ascii_maze, path, visited):
    path_set = set(path) if path else set()
    visited_set = set(visited) if visited else set()
    for i, row in enumerate(ascii_maze):
        line = []
        for j, ch in enumerate(row):
            if (i, j) in path_set:
                line.append("o")
            elif (i, j) in visited_set and ch == OPEN:
                line.append("*")
            else:
                line.append(ch)
        print("".join(line))

def find_border_openings_binary(maze01):
    """Détecte les ouvertures (valeur 0) sur la bordure d'une grille 0/1."""
    rows, cols = len(maze01), len(maze01[0])
    openings = []
    for c in range(cols):
        if maze01[0][c] == 0:
            openings.append((0, c))
        if maze01[rows - 1][c] == 0:
            openings.append((rows - 1, c))
    for r in range(1, rows - 1):
        if maze01[r][0] == 0:
            openings.append((r, 0))
        if maze01[r][cols - 1] == 0:
            openings.append((r, cols - 1))
    # dédoublonnage
    seen = set()
    uniq = []
    for rc in openings:
        if rc not in seen:
            seen.add(rc)
            uniq.append(rc)
    return uniq

# ===================== Backtracking (itératif, sans récursion) =====================
def solve_backtracking(maze01, start=None, end=None):
    """
    DFS itératif (pile) pour éviter RecursionError.
    maze01: grille 0/1 (0 = libre, 1 = mur)
    """
    rows, cols = len(maze01), len(maze01[0])

    # Détection auto si start/end non fournis ou fermés
    if start is None or end is None or not (0 <= start[0] < rows and 0 <= start[1] < cols) or not (0 <= end[0] < rows and 0 <= end[1] < cols) or maze01[start[0]][start[1]] == 1 or maze01[end[0]][end[1]] == 1:
        openings = find_border_openings_binary(maze01)
        if len(openings) >= 2:
            start, end = openings[0], openings[1]
        else:
            # fallback aux positions classiques
            start, end = (1, 0), (rows - 2, cols - 1)

    stack = [start]
    visited = {start}
    parent = {}  # pour reconstruire le chemin
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]  # haut, droite, bas, gauche

    while stack:
        r, c = stack.pop()
        if (r, c) == end:
            # reconstruire le chemin
            path = []
            x = end
            while x != start:
                path.append(x)
                x = parent[x]
            path.append(start)
            path.reverse()
            return path, visited

        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            nb = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and maze01[nr][nc] == 0 and nb not in visited:
                visited.add(nb)
                parent[nb] = (r, c)
                stack.append(nb)

    return None, visited

# ===================== A* (implémentation originale, avec timer) =====================
def a_star(maze01, start=None, end=None):
    rows, cols = len(maze01), len(maze01[0])

    if start is None or end is None or not (0 <= start[0] < rows and 0 <= start[1] < cols) or not (0 <= end[0] < rows and 0 <= end[1] < cols) or maze01[start[0]][start[1]] == 1 or maze01[end[0]][end[1]] == 1:
        openings = find_border_openings_binary(maze01)
        if len(openings) >= 2:
            start, end = openings[0], openings[1]
        else:
            start, end = (1, 0), (rows - 2, cols - 1)

    def heuristic(a,b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    open_set = []
    heapq.heappush(open_set, (heuristic(start,end), 0, start))
    came_from = {}
    g_score = {start:0}
    visited = set()
    start_time = time.time()
    step = 0

    while open_set:
        _, g, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        step += 1

        # Timer en direct toutes les 100 étapes (comportement original)
        if step % 100 == 0:
            elapsed = time.time() - start_time
            sys.stdout.write(f"\rTemps écoulé (A*) : {elapsed:.2f}s")
            sys.stdout.flush()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            print()  # retour ligne après le timer
            return path, visited

        r, c = current
        for dx, dy in directions:
            nr, nc = r + dx, c + dy
            if 0 <= nr < rows and 0 <= nc < cols and maze01[nr][nc] == 0:
                neighbor = (nr, nc)
                tentative_g = g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor,end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    came_from[neighbor] = current

    print()
    return None, visited

# ===================== Main =====================
if __name__ == "__main__":
    from maze_build import generate_maze_backtracking, generate_maze_kruskal, maze_to_ascii as build_maze_to_ascii  # [[13]]
    from save import save_maze_to_file  # [[11]]

    tracemalloc.start()

    # --- Génération ---
    n = int(input("Taille du labyrinthe : "))
    algo = input("Générer labyrinthe (B = Backtracking, K = Kruskal) : ").strip().upper() or "K"

    t_gen0 = time.time()
    if algo == "B":
        maze = generate_maze_backtracking(n)   # peut renvoyer ASCII (#/.)
    else:
        maze = generate_maze_kruskal(n, n)     # renvoie 0/1
    t_gen1 = time.time()

    # Afficher le labyrinthe généré (ASCII) une seule fois
    ascii_maze = build_maze_to_ascii(maze)
    print("\n=== Labyrinthe généré ===")
    print_ascii(ascii_maze)

    # --- Choix du solveur ---
    method = input("\nRésoudre avec (B = Backtracking, A = A*) : ").strip().upper() or "A"

    # Résolution toujours sur 0/1
    maze01 = ascii_to_binary(ascii_maze)

    # --- Résolution ---
    t_res0 = time.time()
    if method == "B":
        path, visited = solve_backtracking(maze01)   # itératif -> pas de RecursionError
    else:
        path, visited = a_star(maze01)               # A* original
    t_res1 = time.time()

    if path is None:
        print("Aucun chemin trouvé (labyrinthe invalide ?).")
        # Statistiques avant sortie
        current, peak = tracemalloc.get_traced_memory()
        print(f"\n⏱️ Génération: {t_gen1 - t_gen0:.4f}s | Résolution: {t_res1 - t_res0:.4f}s")
        print(f"💾 Mémoire: courant {current/1024:.2f} Ko | pic {peak/1024:.2f} Ko")
        tracemalloc.stop()
        sys.exit(1)

    # --- Affichage final: labyrinthe + chemin ---
    print("\n=== Labyrinthe résolu ===")
    print_maze_with_path(ascii_maze, path, visited)

    # --- Statistiques (juste avant la demande de sauvegarde) ---
    current, peak = tracemalloc.get_traced_memory()
    print(f"\n⏱️ Génération: {t_gen1 - t_gen0:.4f}s | Résolution: {t_res1 - t_res0:.4f}s")
    print(f"💾 Mémoire: courant {current/1024:.2f} Ko | pic {peak/1024:.2f} Ko")

    # --- Demande de sauvegarde (après affichage des stats) ---
    save = input("Voulez-vous sauvegarder le labyrinthe ? (O/N) : ").strip().upper()
    if save == "O":
        filename = input("Nom du fichier pour sauvegarder le labyrinthe : ").strip() or "maze"
        # save_maze_to_file accepte 0/1 ou '#/.' et surimprime 'o' et '*' [[11]]
        save_maze_to_file(ascii_maze, path, visited, filename)

    tracemalloc.stop()
