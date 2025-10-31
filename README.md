# Supercon 2025 Badge Tools

Python utilities for interacting with the Hackaday Supercon 2025 Badge (ESP32-S3 with MicroPython).

Built with `mpremote` for reliable file operations that won't disrupt your badge display.

## Setup

Install dependencies with uv:
```bash
uv sync
```

Or install dependencies manually:
```bash
pip install pyserial mpremote
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
Upload, download, and manage files on the badge using mpremote (official MicroPython tool).

**Features:**
- Uses `mpremote` for reliable file operations
- Won't reset the device or turn off the display
- **Supports glob patterns** for batch downloads (`*`, `?` wildcards)
- **Supports recursive directory operations** with `-r` flag
- Automatic directory creation for downloads

```bash
# List files in root
uv run badge_file_manager.py ls

# List files in specific directory
uv run badge_file_manager.py ls /apps

# Read a file
uv run badge_file_manager.py cat /main.py

# Download a single file from badge
uv run badge_file_manager.py download /apps/chat.py chat.py

# Download multiple files using glob patterns
uv run badge_file_manager.py download '/apps/*.py' ./files/
uv run badge_file_manager.py download '/apps/user?.py' ./files/

# Download entire directory recursively
uv run badge_file_manager.py download -r /apps ./local_apps/

# Upload a file to badge
uv run badge_file_manager.py upload local_file.py /remote_file.py

# Upload entire directory recursively
uv run badge_file_manager.py upload -r ./my_app /apps/my_app/

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

# Backup all apps from the badge
uv run badge.py download -r /apps ./backup/

# Download all Python files using glob patterns
uv run badge.py download '/apps/*.py' ./files/

# Download specific user apps only
uv run badge.py download '/apps/user?.py' ./files/

# Create a custom app
# 1. Write your app locally as myapp.py
# 2. Upload it: uv run badge.py upload myapp.py /apps/userA.py
# 3. Restart the badge (Ctrl+D in REPL)

# Deploy a complete application directory
uv run badge.py upload -r ./my_badge_app /apps/my_badge_app/

# Monitor badge activity with logging
uv run badge.py monitor badge_activity.log
```

## Tips

- Press Ctrl+C in the REPL to interrupt running programs
- Press Ctrl+D to soft reset the badge
- The badge runs multiple apps that can be switched via the menu
- Check memory with `import gc; gc.mem_free()`
