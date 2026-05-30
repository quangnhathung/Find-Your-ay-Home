# Find Your Way Home - Hill Climbing Pathfinding Visualization

An interactive GUI application built with Pygame that visualizes multiple Hill Climbing algorithm variants for pathfinding on a grid. Users can place start/end points, draw obstacles, configure parameters, and compare algorithm performance through statistical experiments.

---

## Overview

This project demonstrates local search-based pathfinding using Hill Climbing algorithms in a 2D grid environment. Unlike classical pathfinding (A*, Dijkstra), Hill Climbing uses heuristic-guided local decisions to navigate from start to goal.

**Key Objectives:**

- Visually compare 4 Hill Climbing variants in real-time
- Provide an intuitive drag-and-click interface for map creation
- Run batch experiments to statistically measure algorithm success rates
- Serve as an educational tool for AI search algorithm concepts

---

## Features

### Core Features
- **Interactive Grid Editor** — Left-click to place start (blue), end (green), and walls (black); right-click to erase
- **4 Hill Climbing Algorithms** — Simple, Steepest Ascent, Stochastic, Random Restart
- **Real-time Visualization** — Watch the algorithm explore the grid step-by-step with configurable delay
- **Random Map Generator** — Generate obstacle maps with configurable density

### Advanced Features
- **Batch Experiment Runner** — Run 100 trials per algorithm with statistical bar chart output (via Matplotlib)
- **Configurable Parameters** — Adjust matrix size, obstacle density, max restart count, and animation delay via UI
- **Start Screen** — Themed welcome screen with banner background and fade transition
- **Multi-variant Wall Textures** — Random textured wall tiles (grass, trees, rocks, etc.)

### User Features
- **Controls Panel** — Keyboard/mouse instructions displayed in the right panel
- **Settings Panel** — Input fields for Max Restart, Delay, Density, and Matrix size with Apply button
- **Clear Map** — Press `C` to reset the grid

---

## Tech Stack

| Category       | Technology                            |
| -------------- | ------------------------------------- |
| Language       | Python 3.13                           |
| Framework      | Pygame 2.x                            |
| Visualization  | Matplotlib (experiment charts)        |
| Config         | python-dotenv (.env file)             |
| Typing         | Python typing module                  |
| IDE            | Visual Studio Code / PyCharm          |

---

## System Architecture

The application follows a **modular monolith** architecture with clear separation of concerns:

```
┌─────────────────────────────────────┐
│         FindHome.py (Entry)         │
├─────────────────────────────────────┤
│        StartScreen (UI Layer)       │
│        root (Main Game Loop)        │
├──────────────┬──────────────────────┤
│  Algorithms  │   Config & Model     │
│  (internal/) │   (config/, model/)  │
└──────────────┴──────────────────────┘
```

- **Layered Architecture** — UI layer (StartScreen, root loop) → Algorithm layer → Model layer
- **Event-driven Game Loop** — Pygame event loop drives all interactions
- **Strategy Pattern** — Algorithms implement the same interface and are interchangeable
- **Immutable Grid Model** — Grid state is managed by the `Node` class with clear state transitions

---

## Project Structure

```text
game/
├── FindHome.py                    # Entry point — launches start screen then main loop
├── .env                           # Environment configuration (ignored by git)
├── .env_sample                    # Sample environment variables with Vietnamese comments
├── .gitignore
│
├── config/
│   ├── config.py                  # Config class reading .env via python-dotenv
│   ├── constans.py                # Global constants (colors, derived config values)
│   ├── layout.py                  # Window dimensions, Pygame display setup, icon
│   └── utils.py                   # Heuristic function (Manhattan), grid utilities, drawing helpers
│
├── internal/
│   ├── root.py                    # Main game loop, UI rendering, button handling, experiment runner
│   ├── StartScreen.py             # Welcome/start screen with banner and START/EXIT buttons
│   │
│   └── Algorithm/
│       ├── Simple.py              # Simple Hill Climbing — picks first improving neighbor
│       ├── SteepestAscent.py      # Steepest Ascent — picks best neighbor globally
│       ├── Stochastic.py          # Stochastic Hill Climbing — weighted random among improvers
│       ├── SidewaysMoves.py       # Sideways Moves — allows plateau moves up to a limit
│       └── RandomRestart.py       # Random Restart — restarts from random position when stuck
│
├── model/
│   └── model.py                   # Node class (grid cell), asset caching, image scaling
│
└── assets/
    ├── banner.png                 # Start screen background
    ├── logo.png                   # Window icon
    ├── character-bg.png           # Start node sprite
    ├── home.png                   # End node sprite
    ├── wall.png                   # Wall tile
    ├── grass.png                  # Wall variant
    ├── tree.png                   # Wall variant
    ├── rock.jpg                   # Wall variant
    ├── human-angry.png            # Wall variant
    ├── hole.png                   # Wall variant
    ├── mark.png                   # Open node indicator
    ├── foot.png                   # Path node indicator
    ├── flag.png                   # Flag node (Random Restart marker)
    └── EndOfPath.png              # Closed node indicator
```

---

## Business Flow

```
User launches application
    │
    ▼
Start Screen
    │
    ├── [START] ──► Main Game Loop
    └── [EXIT]  ──► Quit
                     │
                     ▼
         ┌──────────────────────────┐
         │       Game Loop          │
         │                          │
         │  1. Set Start & End      │
         │  2. Draw Walls           │
         │  3. Configure Settings   │
         │  4. Click Algorithm      │
         │                          │
         │  ┌──────────────────┐    │
         │  │ Algorithm Runs   │    │
         │  │  → Hill Climbing │    │
         │  │  → Visualize     │    │
         │  │  → Show Result   │    │
         │  └──────────────────┘    │
         │                          │
         │  5. Or "Run Experiments" │
         │     → Batch 100 runs     │
         │     → Show bar chart     │
         └──────────────────────────┘
```

---

## Algorithms

All algorithms use **Manhattan distance** as the heuristic function `h(a, b) = |x1 - x2| + |y1 - y2|`.

| Algorithm     | Selection Strategy                              | Plateau Handling | Restart |
| ------------- | ----------------------------------------------- | ---------------- | ------- |
| Simple        | First neighbor with lower heuristic             | No               | No      |
| Steepest      | Best neighbor (lowest heuristic), random if tie | No               | No      |
| Stochastic    | Weighted random among improving neighbors       | No               | No      |
| SidewaysMoves | Best neighbor, allows equal-heuristic moves     | Limited count    | No      |
| RandomRestart | Best neighbor; marks stuck nodes as flags       | No               | Yes     |

---

## Database Design

Not Detected — This project does not use a database. All state is held in memory via Pygame surfaces and Python data structures.

---

## API Documentation

Not Detected — This is a desktop GUI application. There are no REST, GraphQL, or RPC APIs.

---

## Authentication & Authorization

Not Detected — The application runs locally with no user accounts, authentication, or authorization system.

---

## Environment Variables

| Variable          | Description                                            | Required | Default |
| ----------------- | ------------------------------------------------------ | -------- | ------- |
| `MAX_SIDEWAY_MOVE`| Maximum consecutive sideways moves allowed             | No       | 10      |
| `SCREEN_WIDTH`    | Width of the grid area in pixels                       | No       | 600     |
| `MATRIX`          | Number of rows/columns in the grid                     | No       | 10      |
| `BG_COLOR`        | Background color (hex format)                          | No       | #F5F2EA |
| `DENSITY`         | Obstacle density for random map generation (0.0–1.0)   | No       | 0.3     |
| `MAX_RESTART`     | Maximum restarts for Random Restart algorithm          | No       | 10      |
| `DELAY`           | Animation delay between steps in milliseconds          | No       | 75      |

---

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Clone
```bash
git clone <repository-url>
cd game
```

### Install Dependencies
```bash
pip install pygame python-dotenv matplotlib
```

### Setup Environment
```bash
cp .env_sample .env
# Edit .env to customize parameters (optional)
```

### Run
```bash
python FindHome.py
```

---

## Docker

Not Detected — No Dockerfile or docker-compose.yml is present in the project.

---

## Testing

Not Detected — No test framework, test files, or test scripts are present in the codebase.

---

## CI/CD

Not Detected — No CI/CD configuration files (GitHub Actions, GitLab CI, Jenkins) are present.

---

## Deployment

The application runs as a local desktop GUI. To distribute:

```bash
# Install PyInstaller
pip install pyinstaller

# Package as single executable
pyinstaller --onefile --windowed FindHome.py
```

---

## Security

- **Authentication** — Not applicable (local desktop app)
- **Authorization** — Not applicable
- **Input Validation** — User input from UI fields is validated and clamped (integer parsing with fallbacks, density clamped to `[0, 1]`, matrix size clamped to `[2, 200]`)
- **Encryption** — Not detected
- **Secrets Management** — `.env` file is git-ignored; sensitive configuration stays local

---

## Performance Considerations

- **Caching** — Raw images and scaled images are cached in dictionaries to avoid repeated disk I/O and rescaling
- **Algorithm Complexity** — Each step evaluates `O(k)` neighbors where `k ≤ 4` (up/down/left/right), making per-step cost constant
- **Animation Delay** — Configurable `DELAY` parameter controls visualization speed; setting to `0` runs algorithms at maximum speed during experiments
- **Grid Size** — Matrix up to 200×200 (40,000 nodes) is supported; larger grids may impact UI responsiveness
- **Experiments** — Batch runs use a `silent_draw` no-op to skip Pygame rendering, maximizing throughput

---

## Known Limitations

1. **No Diagonal Movement** — Agents can only move up, down, left, and right
2. **No Weighted/Uneven Terrain** — All non-wall cells have equal traversal cost
3. **No Path Smoothing** — The reconstructed path follows raw algorithm output without post-processing
4. **No Save/Load** — Maps cannot be saved to disk or loaded from files
5. **No Unit Tests** — The codebase lacks automated test coverage
6. **Single Window** — All algorithms run in the same window; no multi-view comparison
7. **Sideways Moves Not on UI** — The `SidewaysMoves` algorithm is imported but not exposed as a button

---

## Future Improvements

1. **Add Diagonal Movement** — Support 8-directional movement for more realistic pathfinding
2. **Weighted Terrain** — Assign different costs to different cell types (e.g., forest, water, road)
3. **Additional Algorithms** — Add A*, Dijkstra, Beam Search, Genetic Algorithm for comparison
4. **Save/Load Maps** — Serialize grid layouts to JSON files
5. **Unit & Integration Tests** — Add pytest coverage for algorithms and utilities
6. **Multi-window Comparison** — Side-by-side visualization of multiple algorithms running simultaneously
7. **Performance Profiling** — Optimize the experiment runner for larger grid sizes
8. **Localization** — Support English language option alongside current Vietnamese UI
9. **SidewaysMoves Button** — Expose the already-implemented algorithm on the UI

---

## Architecture Summary

| Aspect          | Detail                                                    |
| --------------- | --------------------------------------------------------- |
| Pattern         | Modular Monolith with Strategy Pattern                    |
| UI Framework    | Pygame (custom event loop, no widget library)             |
| State Management| In-memory grid of `Node` objects; immutable state machine |
| Extensibility   | Adding a new algorithm requires only one new file         |
| Config          | External `.env` file + UI-based runtime overrides         |

---

## Code Quality Assessment

| Category      | Score | Notes                                                    |
| ------------- | ----- | -------------------------------------------------------- |
| Architecture  | 7/10  | Clean separation but tight coupling between layout/constans |
| Code Quality  | 7/10  | Well-structured algorithms; some duplicate draw logic    |
| Security      | 6/10  | Input validation present but no sandboxing               |
| Testing       | 1/10  | No automated tests                                       |
| Documentation | 6/10  | Vietnamese comments; minimal docstrings                  |

---

## Technical Debt

1. **Circular Imports** — `config/layout.py` imports from `model/model.py`, and `model/model.py` imports from `config/constans.py`, creating a circular dependency that works only because Python's import system handles it at module level
2. **Duplicate Draw Logic** — `Node.draw()` in `model.py` and `root.py` both handle rendering; the `is_path()` method is duplicated (lines 214–220)
3. **Hardcoded Dimensions** — Some layout calculations depend on pixel constants that should be derived from configuration
4. **Mixed Language** — Comments, messages, and variables mix Vietnamese and English inconsistently
5. **Unused Imports** — Several files import modules that are not directly used (e.g., `Node` in `root.py` via wildcard imports)
6. **Wildcard Imports** — Heavy use of `from X import *` makes dependency tracking difficult

---

## Recommendations

1. **Add pytest tests** for each algorithm with known grid configurations
2. **Refactor imports** to use explicit names instead of wildcards
3. **Resolve circular dependencies** by extracting shared types to a dedicated module
4. **Add English localization** or consistently use one language for comments and UI
5. **Expose SidewaysMoves** algorithm on the UI button bar
6. **Add a `pyproject.toml`** with project metadata and dependencies for modern Python packaging
7. **Add type stubs** or switch to a type-checked codebase with mypy

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

Not Detected — No license file is present in the repository.
