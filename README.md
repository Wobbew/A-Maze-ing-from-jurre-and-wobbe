*This project has been created as part of the 42 curriculum by jstomps and wwiedijk.*

# A-Maze-ing

## Table of Contents
1. [Description](#description)
2. [Features](#features)
3. [Instructions](#instructions)
4. [Configuration File Format](#configuration-file-format)
5. [Maze Generation Algorithm](#maze-generation-algorithm)
6. [Code Reusability](#code-reusability)
7. [Module Usage](#module-usage)
8. [Team & Project Management](#team--project-management)
9. [Resources](#resources)

## Description

This project implements a configurable maze generator and visual renderer as part of the 42 curriculum. The program creates perfect (with one unique path between entrance and exit) or imperfect mazes, exports them in a hexadecimal per-cell format, and provides visual rendering in both terminal and graphical displays. The maze generator is designed as a reusable module that can be imported and integrated into future projects.

The project demonstrates proficiency in algorithm implementation, data structure design, code modularity, and user interface development through both terminal and graphical rendering options.

## Features

- **Configurable maze generation** with customizable dimensions, entry/exit points, and generation parameters
- **Multiple algorithm support** including recursive backtracking, Prim's, and Kruskal's algorithms
- **Perfect maze generation** ensuring exactly one path between entrance and exit when enabled
- **Perfect maze validation** including wall coherence, corridor width limits, and full connectivity
- **Visual "42" pattern** embedded in generated mazes (when space permits)
- **Dual rendering modes**: Terminal ASCII and graphical (MLX) display
- **Interactive controls** for maze regeneration, path visualization, and customization
- **Hexadecimal output format** with per-cell wall encoding for easy serialization and sharing
- **Reproducible generation** using seed-based random number generation
- **Comprehensive error handling** with graceful failure modes and user-friendly error messages

## Instructions

### Installation and Setup

```bash
# Install dependencies and create virtual environment
make install

# Build the reusable module package
make build
```

### Running the Program

```bash
# Run with default configuration
make run

# Or run directly with a config file
python3 a_maze_ing.py config.txt
```

### Development Commands

```bash
# Run in debug mode (pdb debugger)
make debug

# Check code quality (flake8 and mypy)
make lint

# Clean up cache and temporary files
make clean
```

The program reads the configuration file and generates a maze according to the specified parameters, writing the output to the file specified in the config file (defaults to `maze.txt`).

## Configuration File Format

The configuration file uses a `KEY=VALUE` format with one pair per line. Lines starting with `#` are treated as comments and ignored.

### Mandatory Parameters

```
WIDTH=20              # Maze width in cells (positive integer)
HEIGHT=15             # Maze height in cells (positive integer)
ENTRY=0,0             # Entry point coordinates (x,y)
EXIT=19,14            # Exit point coordinates (x,y)
OUTPUT_FILE=maze.txt  # Output filename for hex maze data
PERFECT=False         # Generate perfect maze (True/False)
```

### Optional Parameters

```
SEED=42               # Random seed for reproducibility (int or string)
ALGORITHM=backtracker # Maze generation algorithm (backtracker, prim, kruskal)
```

### Example Configuration

```
# Default A-Maze-ing Configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=0
```

## Maze Generation Algorithm

### Algorithm Choice: Recursive Backtracking

The primary maze generation algorithm implemented is **Recursive Backtracking**, chosen for its balance of simplicity, visual quality, and ability to generate both perfect and imperfect mazes.

### Why Recursive Backtracking?

1. **Perfect Maze Generation**: Naturally generates perfect mazes (spanning trees) when using a depth-first search approach
2. **Visual Quality**: Produces mazes with long, winding corridors that create aesthetically pleasing and challenging puzzles
3. **Deterministic Reproducibility**: Seed-based randomization ensures consistent results for identical parameters
4. **Memory Efficiency**: Stack-based implementation (with explicit stack) is straightforward and memory-conscious
5. **Educational Value**: Demonstrates core computer science concepts: recursion, depth-first search, graph theory, and backtracking

### Algorithm Implementation

The recursive backtracking algorithm:
1. Marks the starting cell as visited
2. Selects a random unvisited neighbor
3. Removes the wall between current and neighbor cell
4. Recursively visits the neighbor
5. Backtracks when no unvisited neighbors exist
6. Results in a spanning tree with exactly one path between any two points

### Maze Validity Guarantees

Generated mazes satisfy all requirements:
- **Wall Coherence**: Adjacent cells have consistent wall representations
- **Full Connectivity**: All cells are reachable from entry point (no isolated cells except "42" pattern)
- **Corridor Width Limits**: No open areas larger than 2×2 cells
- **Border Walls**: External boundaries are properly sealed
- **Entry/Exit Cells**: Guaranteed different locations within bounds

## Code Reusability

### The mazegen Module

The maze generation logic is packaged as a standalone, reusable Python module called **mazegen**, installable via pip. This allows other projects to easily integrate maze generation functionality without reimplementing the algorithms.

#### Module Installation

```bash
# Install from the packaged wheel
pip install mazegen-1.0.0-py3-none-any.whl
```

#### Module Usage

```python
from mazegen.maze import MazeGenerator

# Create a maze generator with custom parameters
generator = MazeGenerator(
    height=20,
    width=20,
    perfect=True,
    entry=(0, 0),
    exit=(19, 19),
    seed="42"
)

# Generate the maze
generator.generate()

# Access the maze structure (list of dicts with wall data)
maze_data = generator.list_dict

# Write to hexadecimal format
generator.write_hex("my_maze.txt")

# Get the solution path
solution_path = generator.solution
```

#### What's Reusable

- **MazeGenerator class**: Core maze generation and validation logic
- **Algorithm implementations**: Recursive backtracking, Prim's, Kruskal's
- **Wall encoding**: Hexadecimal per-cell wall representation
- **Path solving**: Breadth-first search for finding shortest path
- **Seed-based reproducibility**: Deterministic maze generation

#### What's NOT Included in the Module

- Visual rendering (terminal ASCII or MLX graphics)
- Interactive GUI controls
- Configuration file parsing
- Main application entry point

This separation ensures the module remains lightweight, portable, and focused on core maze generation functionality.

## Module Usage

### Basic Example

```python
from mazegen.maze import MazeGenerator

# Generate a 15x15 perfect maze with reproducible randomness
maze = MazeGenerator(
    height=15,
    width=15,
    perfect=True,
    entry=(0, 0),
    exit=(14, 14),
    seed="custom_seed"
)

# Generate the maze structure
maze.generate()

# Access maze data
for row in maze.list_dict:
    for cell in row:
        walls = cell["walls"]  # 4-bit encoding (N, E, S, W)
        marked = cell["marked"]  # Part of "42" pattern

# Get solution path
path = maze.solution  # String like "EESSWWNNEE"

# Write to file in hex format
maze.write_hex("output.txt")
```

### Accessing Generated Structure

The maze structure is stored in `list_dict` as a 2D list of dictionaries:

```python
cell = maze.list_dict[y][x]
# cell["walls"]: int (0-15) encoding walls as bits [N, E, S, W]
# cell["marked"]: bool (True if part of "42" pattern)
```

### Passing Custom Parameters

All parameters are passed to the constructor:

- `height`, `width`: Maze dimensions (positive integers)
- `perfect`: Boolean for perfect maze generation
- `entry`, `exit`: Tuples (x, y) for start and end points
- `seed`: String or int for reproducible randomization

## Team & Project Management

### Team Members

| Member      | Role                                    |
|-------------|-----------------------------------------|
| jstomps     | Algorithm implementation, core logic    |
| wwiedijk    | Visual rendering, module packaging, integration |

### Project Phases and Evolution

#### Phase 1: Planning & Algorithm Research
- **Planned**: Analyze maze generation algorithms and choose optimal approach
- **Actual**: Selected recursive backtracking after comparing with Prim's and Kruskal's
- **Evolution**: Initial plan to implement all three algorithms; later focused on one well-tested implementation

#### Phase 2: Core Generation Engine
- **Planned**: Implement maze generation with wall encoding
- **Actual**: Completed with hexadecimal per-cell format and seed reproducibility
- **Evolution**: Added comprehensive validation for maze coherence and wall consistency

#### Phase 3: Visual Rendering
- **Planned**: Terminal ASCII and MLX graphical display
- **Actual**: Both rendering modes implemented with interactive controls
- **Evolution**: Initially ASCII-only; MLX support added for richer visual experience

#### Phase 4: Module Packaging
- **Planned**: Package as reusable pip-installable module
- **Actual**: Created `mazegen` package with proper build configuration
- **Evolution**: Separated rendering logic from generation to keep module lightweight

### What Worked Well

1. **Clear separation of concerns**: Generator logic isolated from rendering enables reusability
2. **Comprehensive error handling**: Graceful handling of invalid configurations prevents crashes
3. **Seed-based reproducibility**: Enables consistent testing and debugging
4. **Type hints and validation**: Caught many issues early through static analysis
5. **Modular architecture**: Each component (parsing, generation, rendering) is independently testable

### What Could Be Improved

1. **Algorithm variety**: Currently focused on recursive backtracking; supporting alternative algorithms would add flexibility
2. **Performance optimization**: Large maze generation could benefit from iterative algorithms instead of recursion
3. **Animation framework**: Maze generation visualization during drawing process (planned bonus feature)
4. **Advanced interactions**: More customization options (colors, patterns, animation speed)
5. **Logging and diagnostics**: Better debugging information for maze validation failures

### Tools Used

- **Python 3.10+**: Primary language
- **MiniLibX (MLX)**: Graphical rendering library
- **setuptools/build**: Python package distribution
- **flake8**: Code linting and style enforcement
- **mypy**: Static type checking
- **pytest**: Unit testing framework (development)
- **GitHub**: Version control and collaboration
- **AI Assistance**: Used for code refactoring, documentation generation, and small helper functions; all logic reviewed and validated by project authors

## Resources

### Maze Generation References

- [Maze Generation Algorithms on Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Perfect Mazes and Spanning Trees](https://en.wikipedia.org/wiki/Perfect_maze)
- Recursive Backtracking: A depth-first search approach to maze generation
- Prim's Algorithm: Probability-weighted random spanning tree generation
- Kruskal's Algorithm: Edge-based minimum spanning tree generation

### Visualization and Graphics

- [MiniLibX Documentation](https://github.com/42Paris/minilibx-linux)
- Terminal ASCII art rendering techniques
- Interactive event handling and user input processing

### AI Usage

AI was used for specific, well-defined tasks that were reviewed and validated by project authors:

1. **Documentation Generation**: Creating docstrings and README sections
2. **Type Annotation Support**: Suggesting type hints and mypy configurations


