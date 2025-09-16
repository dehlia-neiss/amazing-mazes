import heapq
import time   # <-- ajouté

# ===================== BACKTRACKING =====================
def solve_backtracking(maze, start=(1,0), end=None):
    rows, cols = len(maze), len(maze[0])
    if end is None:
        end = (rows-2, cols-1)

    path = []
    visited = set()

    def backtrack(x, y):
        if (x, y) == end:
            path.append((x,y))
            return True
        if (x,y) in visited or maze[x][y] in [1, "#"]:
            return False
        
        if not (0 <= x < rows and 0 <= y < cols):
            return False


        visited.add((x,y))
        path.append((x,y))

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            if backtrack(x+dx, y+dy):
                return True

        path.pop()
        return False

    backtrack(*start)
    return path, visited

# ===================== A* =====================
def a_star(maze, start=(1,0), end=None):
    rows, cols = len(maze), len(maze[0])
    if end is None:
        end = (rows-2, cols-1)

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    def heuristic(a,b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    open_set = []
    heapq.heappush(open_set, (heuristic(start,end), 0, start))
    came_from = {}
    g_score = {start:0}
    visited = set()

    while open_set:
        _, g, current = heapq.heappop(open_set)
        visited.add(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited

        for dx,dy in directions:
            nx,ny = current[0]+dx, current[1]+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny]==0:
                neighbor = (nx,ny)
                tentative_g = g+1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor,end)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))
                    came_from[neighbor] = current

    return None, visited

# ===================== AFFICHAGE =====================
def print_maze_with_path(maze, path, visited):
    path_set = set(path) if path else set()
    for i,row in enumerate(maze):
        line = ""
        for j,cell in enumerate(row):
            if (i,j) in path_set:
                line += "o"
            elif (i,j) in visited and maze[i][j]==0:
                line += "*"
            elif cell in [1,"#"]:
                line += "#"
            else:
                line += "."
        print(line)

# ===================== TEST =====================
if __name__ == "__main__":
    from maze_build import generate_maze_backtracking, generate_maze_kruskal, maze_to_ascii
    from save import save_maze_to_file

    n = int(input("Taille du labyrinthe : "))
    algo = input("Générer labyrinthe (B = Backtracking, K = Kruskal) : ").upper()

    # chrono génération
    t0 = time.time()
    if algo == "B":
        maze = generate_maze_backtracking(n)
    else:
        maze = generate_maze_kruskal(n,n)
    t1 = time.time()
    print(f"⏱️ Temps de génération ({algo}) : {t1 - t0:.4f} sec")

    ascii_maze = maze_to_ascii(maze)

    method = input("Résoudre avec (B = Backtracking, A = A*) : ").upper()

    # chrono résolution
    t2 = time.time()
    if method == "B":
        path, visited = solve_backtracking(maze)
    else:
        path, visited = a_star(maze)
    t3 = time.time()
    print(f"⏱️ Temps de résolution ({method}) : {t3 - t2:.4f} sec")

    print_maze_with_path(maze, path, visited)

    save = input("Voulez-vous sauvegarder le labyrinthe ? (O/N) : ").upper()
    if save == "O":
        filename = input("Nom du fichier pour sauvegarder le labyrinthe : ")
        save_maze_to_file(maze, path, visited, filename)
