import heapq
import time
import tracemalloc

# ===================== OUTILS FORMAT =====================
WALL = "#"
OPEN = "."

def maze_to_ascii(maze):
    """Accepte 0/1 ou déjà ASCII; renvoie ASCII #/."""
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

# ===================== AFFICHAGE =====================
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

# ===================== SOLVEUR BACKTRACKING (DFS) =====================
def solve_backtracking(maze01, start=(1, 0), end=None):
    rows, cols = len(maze01), len(maze01[0])
    if end is None:
        end = (rows - 2, cols - 1)  # compatible avec nos générateurs
    path = []
    visited = set()

    def in_bounds(r, c): return 0 <= r < rows and 0 <= c < cols
    def is_open(r, c): return maze01[r][c] == 0

    dirs = [(-1,0),(0,1),(1,0),(0,-1)]  # haut, droite, bas, gauche

    def dfs(r, c):
        if (r, c) == end:
            path.append((r, c))
            return True
        visited.add((r, c))
        path.append((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if not in_bounds(nr, nc) or (nr, nc) in visited or not is_open(nr, nc):
                continue
            if dfs(nr, nc):
                return True
        path.pop()
        return False

    if not is_open(*start) or not is_open(*end):
        return None, visited

    ok = dfs(*start)
    if not ok:
        return None, visited
    return path, visited

# ===================== SOLVEUR A* (sans affichage intermédiaire) =====================
def a_star(maze01, start=(1, 0), end=None):
    rows, cols = len(maze01), len(maze01[0])
    if end is None:
        end = (rows - 2, cols - 1)

    def h(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]

    open_set = []
    heapq.heappush(open_set, (h(start, end), 0, start))
    came_from = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, gcur, cur = heapq.heappop(open_set)
        if cur in visited:
            continue
        visited.add(cur)

        if cur == end:
            path = []
            x = cur
            while x in came_from:
                path.append(x)
                x = came_from[x]
            path.append(start)
            path.reverse()
            return path, visited

        r, c = cur
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze01[nr][nc] == 0:
                tentative_g = gcur + 1
                nb = (nr, nc)
                if nb not in g_score or tentative_g < g_score[nb]:
                    g_score[nb] = tentative_g
                    f = tentative_g + h(nb, end)
                    heapq.heappush(open_set, (f, tentative_g, nb))
                    came_from[nb] = cur

    return None, visited

# ===================== TEST / MAIN =====================
if __name__ == "__main__":
    # Import local
    from maze_build import generate_maze_backtracking, generate_maze_kruskal
    from save import save_maze_to_file

    tracemalloc.start()

    # --- Génération ---
    n = int(input("Taille du labyrinthe : "))
    algo = input("Générer labyrinthe (B = Backtracking, K = Kruskal) : ").strip().upper() or "K"

    t0 = time.time()
    if algo == "B":
        maze = generate_maze_backtracking(n)     # ASCII #/.
    else:
        maze = generate_maze_kruskal(n, n)       # 0/1
    t1 = time.time()
    print(f"⏱️ Temps de génération ({algo}) : {t1 - t0:.4f} sec")

    # Convertir en ASCII et afficher une seule fois le labyrinthe généré
    ascii_maze = maze_to_ascii(maze)
    print("\n=== Labyrinthe généré ===")
    print_ascii(ascii_maze)

    # --- Choix du solveur ---
    method = input("\nRésoudre avec (B = Backtracking, A = A*) : ").strip().upper() or "A"

    # Toujours résoudre sur 0/1 pour éviter toute ambiguïté
    maze01 = ascii_to_binary(ascii_maze)

    # --- Résolution ---
    t2 = time.time()
    if method == "B":
        path, visited = solve_backtracking(maze01)
    else:
        path, visited = a_star(maze01)
    t3 = time.time()

    if path is None:
        print("Aucun chemin trouvé (labyrinthe invalide ?).")
        tracemalloc.stop()
        raise SystemExit

    # Affichage final: labyrinthe + chemin (o) + exploré (*)
    print("\n=== Labyrinthe résolu ===")
    print_maze_with_path(ascii_maze, path, visited)
    print(f"\n⏱️ Temps de résolution ({method}) : {t3 - t2:.4f} sec")

    # --- Mémoire ---
    current, peak = tracemalloc.get_traced_memory()
    print(f"💾 Mémoire utilisée : {current/1024:.2f} Ko ; pic : {peak/1024:.2f} Ko")
    tracemalloc.stop()

    # --- Sauvegarde ---
    save = input("Voulez-vous sauvegarder le labyrinthe ? (O/N) : ").strip().upper()
    if save == "O":
        filename = input("Nom du fichier pour sauvegarder le labyrinthe : ").strip() or "maze"
        # On sauvegarde la version ASCII avec overlays
        save_maze_to_file(ascii_maze, path, visited, filename)
