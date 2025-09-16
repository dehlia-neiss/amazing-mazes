import random
import time

# ===================== BACKTRACKING =====================
def generate_maze_backtracking(n):
    taille = 2 * n + 1
    maze = [["#" for _ in range(taille)] for _ in range(taille)]
    
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    
    def backtrack(x, y):
        maze[x][y] = "."
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < taille and 0 < ny < taille and maze[nx][ny] == "#":
                maze[x + dx//2][y + dy//2] = "."
                backtrack(nx, ny)
    
    backtrack(1, 1)
    maze[1][0] = "."  # Entrée
    maze[taille-2][taille-1] = "."  # Sortie
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

def generate_maze_kruskal(width, height):
    maze = [[1 for _ in range(width*2+1)] for _ in range(height*2+1)]
    
    def cell_id(x, y):
        return y * width + x
    
    edges = []
    for y in range(height):
        for x in range(width):
            if x < width-1:
                edges.append(((x, y), (x+1, y)))
            if y < height-1:
                edges.append(((x, y), (x, y+1)))
    
    random.shuffle(edges)
    uf = UnionFind(width*height)
    
    for (x1, y1), (x2, y2) in edges:
        if uf.union(cell_id(x1, y1), cell_id(x2, y2)):
            maze[y1*2+1][x1*2+1] = 0
            maze[y2*2+1][x2*2+1] = 0
            maze[(y1+y2)+1][(x1+x2)+1] = 0
    
    maze[1][0] = 0
    maze[height*2-1][width*2] = 0
    return maze

# ===================== CONVERSION EN ASCII =====================
def maze_to_ascii(maze):
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
    n = int(input("Taille du labyrinthe (nombre de cellules) : "))
    algo = input("Choisir l'algorithme (B = Backtracking, K = Kruskal) : ").upper()
    
    start_time = time.time()  # début chrono
    
    if algo == "B":
        maze = generate_maze_backtracking(n)
    elif algo == "K":
        maze = generate_maze_kruskal(n, n)
    else:
        print("Choix invalide, génération Backtracking par défaut.")
        maze = generate_maze_backtracking(n)
    
    end_time = time.time()  # fin chrono
    print(f"⏱ Temps d'exécution ({algo}) : {end_time - start_time:.4f} secondes")
    
    # Pour éviter d'afficher des millions de lignes, on n'affiche que si c'est petit
    if n <= 50:
        ascii_maze = maze_to_ascii(maze)
        print_maze(ascii_maze)
    else:
        print("Labyrinthe trop grand pour être affiché.")
