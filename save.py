# save_maze.py

def save_maze_to_file(maze, path=None, visited=None, filename="maze.txt"):
    """
    Sauvegarde un labyrinthe et éventuellement sa solution dans un fichier texte.
    
    maze    : labyrinthe sous forme de liste de listes (0 = passage, 1 = mur)
    path    : liste de coordonnées (chemin final)
    visited : set de coordonnées (cases explorées)
    filename: nom du fichier de sortie
    """
    path_set = set(path) if path else set()
    visited_set = set(visited) if visited else set()
    
    with open(filename, "w") as f:
        for i, row in enumerate(maze):
            line = ""
            for j, cell in enumerate(row):
                if (i,j) in path_set:
                    line += "o"  # chemin final
                elif (i,j) in visited_set and maze[i][j]==0:
                    line += "*"  # exploré mais pas sur le chemin
                elif cell in [1, "#"]:
                    line += "#"  # mur
                else:
                    line += "."  # passage libre
            f.write(line + "\n")
    print(f"Labyrinthe sauvegardé dans {filename}")
