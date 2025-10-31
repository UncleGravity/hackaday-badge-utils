#!/usr/bin/env python3
"""
Unified Badge Tool for Supercon 2025 Badge
All-in-one interface for badge interaction
"""
import sys
import subprocess

def show_help():
    print("""
Supercon 2025 Badge Tool
========================

Usage: uv run badge.py <command> [args...]

Commands:
  info                     - Show badge system information
  monitor [logfile]        - Monitor real-time output
  repl                     - Interactive Python REPL
  exec '<code>'            - Execute Python code
  
  ls [path]                - List files
  cat <file>               - Read file contents
  download <remote> <local> - Download file from badge
  upload <local> <remote>  - Upload file to badge
  rm <file>                - Delete file
  
  help                     - Show this help

Examples:
  uv run badge.py info
  uv run badge.py monitor
  uv run badge.py repl
  uv run badge.py exec 'import gc; gc.mem_free()'
  uv run badge.py ls /apps
  uv run badge.py cat /main.py
  uv run badge.py download /apps/chat.py chat.py
  uv run badge.py download '/apps/*.py' ./files/
  uv run badge.py upload myapp.py /apps/userA.py

Quick Info:
  Device: ESP32-S3 @ 240MHz
  Port: /dev/cu.usbmodem2101
  MicroPython: 1.25.0
  File operations powered by mpremote (won't reset display)
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return 1
    
    command = sys.argv[1]
    
    if command == 'help' or command == '--help' or command == '-h':
        show_help()
        return 0
    
    # Map commands to scripts
    script_map = {
        'info': ['badge_info.py'],
        'monitor': ['badge_monitor.py'] + sys.argv[2:],
        'repl': ['badge_repl.py'],
        'exec': ['badge_exec.py'] + sys.argv[2:],
        'ls': ['badge_file_manager.py', 'ls'] + sys.argv[2:],
        'cat': ['badge_file_manager.py', 'cat'] + sys.argv[2:],
        'download': ['badge_file_manager.py', 'download'] + sys.argv[2:],
        'upload': ['badge_file_manager.py', 'upload'] + sys.argv[2:],
        'rm': ['badge_file_manager.py', 'rm'] + sys.argv[2:],
    }
    
    if command not in script_map:
        print(f"Unknown command: {command}")
        print("Run 'uv run badge.py help' for usage.")
        return 1
    
    # Run the appropriate script
    try:
        result = subprocess.run(['uv', 'run'] + script_map[command])
        return result.returncode
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
