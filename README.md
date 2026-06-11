*This project has been created as part of the 42 curriculum by jstomps and wwiedijk.*

# A-Maze-ing

Description
-----------
This project implements a configurable maze generator and renderer. It can
generate mazes, export them in the required hexadecimal per-cell format and
provide a visual rendering (terminal or MLX when available). The generator is
packaged as a reusable module `mazegen.py`.

Instructions
------------
- Run the generator:

		make 

The program reads the provided config file and writes the maze to the
OUTPUT_FILE specified in the config (defaults to `maze.txt`).

Module usage
------------
Import `MazeGenerator` from `mazegen` to programmatically generate mazes and
write the hex output. See `mazegen.py` docstring for a short example.

Resources
---------
- Maze generation algorithms: Prim, Kruskal, recursive backtracker.
- AI usage: code refactor, doc generation, and small helper patches were
	produced with assistance from an AI; all logic was reviewed and adapted by
	the project author.
