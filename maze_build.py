import random
import time

# ===================== BACKTRACKING (itératif, sans affichage) =====================
def generate_maze_backtracking(n, seed=None):
    """
    Génère un labyrinthe parfait en ASCII (#/.) via Backtracking itératif (pile).
    - n: nombre de cellules par côté (grille ASCII finale: 2*n+1)
    - seed: graine aléatoire (None pour aléatoire)
    Retour: liste de listes de caractères '#' et '.'
    """
    if seed is not None:
        random.seed(seed)

    grid_size = 2 * n + 1
    maze = [['#' for _ in range(grid_size)] for _ in range(grid_size)]

    stack = []
    visited = set()
    start_x, start_y = 1, 1

    # cellule de départ
    maze[start_y][start_x] = '.'
    stack.append((start_x, start_y))
    visited.add((start_x, start_y))

    # directions de 2 cases (dx, dy) : haut, droite, bas, gauche
    base_dirs = [(0, -2), (2, 0), (0, 2), (-2, 0)]

    while stack:
        current_x, current_y = stack[-1]
        dirs = base_dirs[:]  # copie
        random.shuffle(dirs)
        found = False

        for dx, dy in dirs:
            nx, ny = current_x + dx, current_y + dy
            if (0 < nx < grid_size - 1 and
                0 < ny < grid_size - 1 and
                (nx, ny) not in visited):

                # abattre le mur entre current et next
                wall_x, wall_y = current_x + dx // 2, current_y + dy // 2
                maze[wall_y][wall_x] = '.'
                maze[ny][nx] = '.'

                stack.append((nx, ny))
                visited.add((nx, ny))
                found = True
                break

        if not found:
            stack.pop()

    # Entrée (gauche) et sortie (droite), cohérentes avec le reste du projet
    maze[1][0] = '.'
    maze[grid_size - 2][grid_size - 1] = '.'

    return maze  # ASCII (#/.)

# ===================== (Optionnel) BACKTRACKING animé =====================
def generate_maze_backtracking_animated(n, delay=0.02, seed=None):
    """
    Variante animée (console) du backtracking.
    Utilise la même logique mais affiche à chaque ouverture de mur.
    """
    import os
    if seed is not None:
        random.seed(seed)

    grid_size = 2 * n + 1
    maze = [['#' for _ in range(grid_size)] for _ in range(grid_size)]

    stack = []
    visited = set()
    start_x, start_y = 1, 1

    def display():
        os.system("cls" if os.name == "nt" else "clear")
        for row in maze:
            print("".join(row))
        time.sleep(delay)

    maze[start_y][start_x] = '.'
    stack.append((start_x, start_y))
    visited.add((start_x, start_y))

    base_dirs = [(0, -2), (2, 0), (0, 2), (-2, 0)]

    while stack:
        current_x, current_y = stack[-1]
        dirs = base_dirs[:]
        random.shuffle(dirs)
        found = False

        for dx, dy in dirs:
            nx, ny = current_x + dx, current_y + dy
            if (0 < nx < grid_size - 1 and
                0 < ny < grid_size - 1 and
                (nx, ny) not in visited):

                wall_x, wall_y = current_x + dx // 2, current_y + dy // 2
                maze[wall_y][wall_x] = '.'
                maze[ny][nx] = '.'
                display()

                stack.append((nx, ny))
                visited.add((nx, ny))
                found = True
                break

        if not found:
            stack.pop()
            display()

    maze[1][0] = '.'
    maze[grid_size - 2][grid_size - 1] = '.'
    return maze

# ===================== KRUSKAL =====================
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[ry] = rx
            return True
        return False

def generate_maze_kruskal(width, height, seed=None):
    """
    Génère un labyrinthe parfait via Kruskal.
    - width, height: dimensions en cellules
    - seed: graine (None = aléatoire)
    Retour: grille 0/1 (1 = mur, 0 = passage)
    """
    if seed is not None:
        random.seed(seed)

    maze = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]

    def cell_id(x, y):
        return y * width + x

    edges = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                edges.append(((x, y), (x + 1, y)))
            if y < height - 1:
                edges.append(((x, y), (x, y + 1)))

    random.shuffle(edges)
    uf = UnionFind(width * height)

    for (x1, y1), (x2, y2) in edges:
        if uf.union(cell_id(x1, y1), cell_id(x2, y2)):
            # ouvrez les deux cellules et le mur entre elles
            maze[y1 * 2 + 1][x1 * 2 + 1] = 0
            maze[y2 * 2 + 1][x2 * 2 + 1] = 0
            maze[(y1 + y2) + 1][(x1 + x2) + 1] = 0

    # Entrée/sortie
    maze[1][0] = 0
    maze[height * 2 - 1][width * 2] = 0
    return maze  # 0/1

# ===================== CONVERSION EN ASCII =====================
def maze_to_ascii(maze):
    """
    Convertit une grille 0/1 ou déjà ASCII (#/.) en ASCII (#/.).
    """
    ascii_maze = []
    for row in maze:
        ascii_row = []
        for cell in row:
            if cell in [1, "#"]:
                ascii_row.append("#")
            else:
                ascii_row.append(".")
        ascii_maze.append(ascii_row)
    return ascii_maze

# ===================== AFFICHAGE =====================
def print_maze(maze):
    for row in maze:
        print("".join(row))

# ===================== PROGRAMME PRINCIPAL =====================
if __name__ == "__main__":
    print("Générer un labyrinthe (B = Backtracking, K = Kruskal)")
    algo = (input("Choix [B/K] (défaut B): ").strip().upper() or "B")
    seed_in = input("Graine (entier, vide = aléatoire): ").strip()
    seed = int(seed_in) if seed_in else None

    start_time = time.time()
    if algo == "K":
        w = int(input("Largeur (cellules) [15]: ").strip() or "15")
        h = int(input("Hauteur (cellules) [15]: ").strip() or "15")
        maze_raw = generate_maze_kruskal(w, h, seed=seed)
        ascii_maze = maze_to_ascii(maze_raw)
        size_info = f"{w}x{h}"
    else:
        n = int(input("Taille (n cellules par côté) [15]: ").strip() or "15")
        # Backtracking non-animé (basé sur ton code)
        ascii_maze = generate_maze_backtracking(n, seed=seed)
        size_info = f"{n}x{n}"

    end_time = time.time()
    print(f"⏱ Temps d'exécution ({algo}, {size_info}) : {end_time - start_time:.4f} sec")

    # Affiche le labyrinthe final uniquement
    if len(ascii_maze) <= 101 and len(ascii_maze[0]) <= 201:
        print_maze(ascii_maze)
    else:
        print("Labyrinthe trop grand pour être affiché.")
