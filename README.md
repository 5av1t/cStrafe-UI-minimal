 cStrafe UI — Forked with Direction Logging

> Forked from [CS2Kitchen/cStrafe-UI](https://github.com/CS2Kitchen/cStrafe-UI). Original project by CS2Kitchen.

A lightweight training tool to help players practice counterstrafing mechanics in CS2. It listens to your movement keys (W, A, S and D) and the left mouse button to decide whether you fired while coming to a full stop, started moving the other way or were still overlapping directions.

**What this fork adds:** per-direction tracking and session logging so you can see whether your A→D or D→A counterstrafes are better, review your session stats mid-game, and analyze CSV logs over time.

![UI Preview](images/strafe_ui_2.gif)


## Installation

1. Make sure you have a recent Python installed. (Install 3.13 from Microsoft Store if you get into issues)
2. Install the required dependency:

   ```bash
   pip install pynput tkinter
   ```

   The Tkinter library (`tkinter`) is included with most standard Python installations on Windows and macOS.

3. Download or clone this repository, then run the program from the project directory:

   ```bash
   python main.py
   ```

## Usage

When the application is running, an overlay appears on top of your game window. It updates whenever you fire the left mouse button. You can drag it to any part of the screen. Make sure to run your game in fullscreen windowed (won't work in fullscreen). You can control the overlay with a few simple keys:

| Key | Action |
|-----|--------|
| **F6** | Hide or show the overlay without quitting. |
| **F7** | Show session stats breakdown (per-direction CS rate, averages). Press again or shoot to return to normal mode. |
| **F8** | Exit the program. |
| **=** | Increase the size of the overlay text. |
| **-** | Decrease the size of the overlay text. |

## Classification Labels

After each shot the tool displays one of three labels along with timing information (when applicable):

| Label | Description |
|-------|-------------|
| **Counter‑strafe** | You released one movement key and quickly pressed the opposite key before shooting. A valid counterstrafe should be followed by a shot within a short delay. The overlay shows the time between the key release and the opposite key press (*CS time*) and the delay between pressing the opposite key and firing (*Shot delay*). |
| **Overlap** | Both opposing movement keys were held at the same time. This indicates overlapping movement, which should be avoided for accurate shooting. The overlay shows how long the keys overlapped before the shot. |
| **Bad** | No valid counterstrafe pattern was detected before the shot. This can mean you shot without changing direction, your movement timing was too slow or you were moving in only one direction. |

## Direction Tracking

Each shot now also displays the strafe direction — for example `A→D` (left-to-right) or `D→A` (right-to-left). This helps you identify which side your mechanics are weaker on.

Press **F7** during a session to see a summary like:

```
Session: 47 shots
CS: 62%  OL: 12  Bad: 6

A→D: 71% CS (24) [avg 38ms]
D→A: 52% CS (23) [avg 52ms, OL avg 142ms]
```

This tells you at a glance that your right-to-left counterstrafes need more work.

## Session Logs

Every session is automatically saved to a CSV file in the `logs/` folder with a timestamped filename (e.g. `logs/session_20260317_214530.csv`). Each row records:

| Column | Description |
|--------|-------------|
| `timestamp` | Time of the shot (HH:MM:SS.ms) |
| `direction` | Strafe direction (e.g. `A→D`, `D→A`, `W→S`, `S→W`) |
| `classification` | Counter‑strafe, Overlap, or Bad |
| `cs_time_ms` | Milliseconds between key release and opposite key press |
| `shot_delay_ms` | Milliseconds between opposite key press and shot |
| `overlap_ms` | Milliseconds of key overlap (for Overlap classifications) |

You can open these in Excel or any spreadsheet tool to track your progress over multiple sessions.

## Project Structure

```
├── main.py              # Entry point
├── movement_keys.py     # Key bindings (change here if not using WASD)
├── input_events.py      # Keyboard and mouse input handling
├── classifier.py        # Movement classification logic
├── overlay.py           # Tkinter overlay UI
├── shot_logger.py       # Session logging and per-direction stats (new)
└── logs/                # Auto-created folder for session CSVs (new)
```

## Credits

Original project by [CS2Kitchen](https://github.com/CS2Kitchen). Direction logging and session stats added in this fork.

Keep your movements crisp and have fun — hope this helps you :D
