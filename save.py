from PIL import Image

def save_maze_to_file(maze, path=None, visited=None, filename="maze.txt"):
    """
    Sauvegarde un labyrinthe et éventuellement sa solution :
    - en fichier texte (.txt)
    - optionnellement en image (.jpg)

    maze    : labyrinthe sous forme de liste de listes (0/1 ou ./#)
    path    : liste de coordonnées (chemin final)
    visited : set de coordonnées (cases explorées)
    filename: nom du fichier de sortie (sans extension)
    """
    # Nettoyer le nom de fichier (enlever extension si donnée)
    if filename.endswith(".txt") or filename.endswith(".jpg"):
        filename = filename.rsplit(".", 1)[0]

    path_set = set(path) if path else set()
    visited_set = set(visited) if visited else set()

    # ================== Sauvegarde en texte ==================
    with open(filename + ".txt", "w") as f:
        for i, row in enumerate(maze):
            line = ""
            for j, cell in enumerate(row):
                if (i, j) in path_set:
                    line += "o"  # chemin final
                elif (i, j) in visited_set and cell in [0, "."]:
                    line += "*"  # exploré mais pas sur le chemin
                elif cell in [1, "#"]:
                    line += "#"  # mur
                else:
                    line += "."  # passage libre
            f.write(line + "\n")

    print(f"Labyrinthe sauvegardé dans {filename}.txt")

    # ================== Option : Sauvegarde en image ==================
    choix = input("Voulez-vous aussi sauvegarder en JPG ? (O/N) : ").upper()
    if choix == "O":
        cell_size = 10  # taille d’une case en pixels
        rows, cols = len(maze), len(maze[0])
        img = Image.new("RGB", (cols * cell_size, rows * cell_size), "white")
        pixels = img.load()

        for i in range(rows):
            for j in range(cols):
                color = (255, 255, 255)  # blanc par défaut
                if (i, j) in path_set:
                    color = (0, 200, 0)      # vert pour le chemin
                elif (i, j) in visited_set and maze[i][j] in [0, "."]:
                    color = (255, 100, 100)  # rouge clair pour exploré
                elif maze[i][j] in [1, "#"]:
                    color = (0, 0, 0)        # noir pour mur

                # Remplir la case
                for x in range(cell_size):
                    for y in range(cell_size):
                        pixels[j * cell_size + x, i * cell_size + y] = color

        img.save(filename + ".jpg")
        print(f"Labyrinthe sauvegardé dans {filename}.jpg")
