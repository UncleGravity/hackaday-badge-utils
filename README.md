# Supercon 2025 Badge Tools

Python scripts for interacting with the Hackaday Supercon 2025 Badge (ESP32-S3 with MicroPython).

## Setup

Install dependencies with uv:
```bash
uv sync
```

## Quick Start (Unified Tool)

The easiest way to use these tools is with the unified `badge.py` script:

```bash
# Show device information
uv run badge.py info

# Monitor real-time output
uv run badge.py monitor

# Interactive REPL
uv run badge.py repl

# Execute a quick command
uv run badge.py exec 'import gc; gc.mem_free()'

# List files
uv run badge.py ls /apps

# Read a file
uv run badge.py cat /main.py

# Get help
uv run badge.py help
```

## Individual Scripts

### 1. badge_info.py - Device Information
Gathers system information, memory stats, and filesystem details.

```bash
uv run badge_info.py
```

**Output includes:**
- MicroPython version
- CPU frequency
- Memory usage
- Flash size
- Directory listings
- WiFi status

### 2. badge_monitor.py - Real-time Monitor
Monitors serial output with timestamps and optional logging.

```bash
# Monitor only
uv run badge_monitor.py

# Monitor and log to file
uv run badge_monitor.py badge_log.txt
```

### 3. badge_repl.py - Interactive REPL
Provides an interactive MicroPython REPL session.

```bash
uv run badge_repl.py
```

**Features:**
- Automatically enters REPL mode
- Interactive Python shell
- Direct access to badge hardware

### 4. badge_file_manager.py - File Management
Upload, download, and manage files on the badge.

```bash
# List files in root
uv run badge_file_manager.py ls

# List files in specific directory
uv run badge_file_manager.py ls /apps

# Read a file
uv run badge_file_manager.py cat /main.py

# Upload a file
uv run badge_file_manager.py upload local_file.py /remote_file.py

# Delete a file
uv run badge_file_manager.py rm /path/to/file.py
```

### 5. badge_exec.py - Quick Command Executor
Execute a single Python command and see the output.

```bash
# Check free memory
uv run badge_exec.py 'import gc; gc.mem_free()'

# Get CPU frequency
uv run badge_exec.py 'import machine; machine.freq()'

# List directory
uv run badge_exec.py 'import os; os.listdir("/")'
```

### 6. badge.py - Unified Tool
All-in-one interface combining all tools above. See "Quick Start" section.

## Badge Information

**Hardware:**
- ESP32-S3 with Octal SPIRAM
- 240 MHz CPU
- MicroPython 1.25.0
- LVGL 9.3.0 GUI

**Serial Port:** `/dev/cu.usbmodem2101` @ 115200 baud

**Apps on Badge:**
- chat.py - Chat application
- talks.py - Conference talks viewer
- badgeshark.py - Badge interaction tool
- nametag.py - Name tag display
- net_tools.py - Network utilities
- And more in `/apps` directory

## Common Tasks

```bash
# Check memory usage
uv run badge.py exec 'import gc; print(f"Free: {gc.mem_free()}, Used: {gc.mem_alloc()}")'

# See what apps are available
uv run badge.py ls /apps

# Read the main.py file
uv run badge.py cat /main.py

# Create a custom app
# 1. Write your app locally as myapp.py
# 2. Upload it: uv run badge.py upload myapp.py /apps/userA.py
# 3. Restart the badge (Ctrl+D in REPL)

# Monitor badge activity with logging
uv run badge.py monitor badge_activity.log
```

## Tips

- Press Ctrl+C in the REPL to interrupt running programs
- Press Ctrl+D to soft reset the badge
- The badge runs multiple apps that can be switched via the menu
- Check memory with `import gc; gc.mem_free()`
