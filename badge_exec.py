#!/usr/bin/env python3
"""
Quick Command Executor for Supercon 2025 Badge
Execute a single Python command on the badge and show the result
"""
import serial
import time
import sys

SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 115200

def execute_command(ser, command):
    """Execute a command and return clean output"""
    # Enter REPL
    ser.write(b'\x03')
    time.sleep(0.5)
    ser.reset_input_buffer()
    
    # Send command
    ser.write((command + '\r\n').encode('utf-8'))
    time.sleep(0.5)
    
    # Read response
    response = ""
    while ser.in_waiting:
        response += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
        time.sleep(0.1)
    
    # Extract output (skip echo and prompts)
    lines = response.split('\n')
    output_lines = []
    skip_next = False
    
    for line in lines:
        clean = line.strip()
        if skip_next or not clean or clean.startswith('>>>') or clean == command:
            skip_next = False
            continue
        output_lines.append(clean)
    
    return '\n'.join(output_lines)

def main():
    if len(sys.argv) < 2:
        print("Badge Quick Command Executor")
        print("\nUsage:")
        print(f"  {sys.argv[0]} '<python_command>'")
        print("\nExamples:")
        print(f"  {sys.argv[0]} 'import gc; print(gc.mem_free())'")
        print(f"  {sys.argv[0]} 'import machine; print(machine.freq())'")
        print(f"  {sys.argv[0]} 'import os; print(os.listdir(\"/\"))'")
        return 1
    
    command = ' '.join(sys.argv[1:])
    ser = None
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        result = execute_command(ser, command)
        
        if result:
            print(result)
        
        # Reset
        ser.write(b'\x04')
        time.sleep(0.5)
        
    except serial.SerialException as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 1
    finally:
        if ser is not None:
            ser.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
