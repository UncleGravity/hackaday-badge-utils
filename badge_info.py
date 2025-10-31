#!/usr/bin/env python3
"""
Badge Information Gatherer for Supercon 2025 Badge
Collects system info, memory stats, and filesystem details
"""
import serial
import time
import sys

SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 115200

def send_command(ser, cmd, wait=0.5):
    """Send a command and return the response"""
    # Clear input buffer
    ser.reset_input_buffer()
    
    # Send command
    ser.write((cmd + '\r\n').encode('utf-8'))
    time.sleep(wait)
    
    # Read response
    response = ""
    while ser.in_waiting:
        response += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
        time.sleep(0.1)
    
    return response

def main():
    print("Supercon 2025 Badge Information Gatherer")
    print("=" * 60)
    
    ser = None
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}\n")
        
        # Send Ctrl+C to enter REPL
        ser.write(b'\x03')
        time.sleep(1)
        ser.reset_input_buffer()
        
        commands = [
            ("System Implementation", "import sys; sys.implementation"),
            ("MicroPython Version", "sys.version"),
            ("CPU Frequency", "import machine; machine.freq()"),
            ("Unique ID", "import ubinascii; ubinascii.hexlify(machine.unique_id())"),
            ("Flash Size", "import esp; esp.flash_size()"),
            ("Free Memory", "import gc; gc.mem_free()"),
            ("Allocated Memory", "gc.mem_alloc()"),
            ("Root Directory", "import os; os.listdir('/')"),
            ("Apps Directory", "os.listdir('/apps')"),
            ("WiFi Status", "import network; sta = network.WLAN(network.STA_IF); sta.active()"),
        ]
        
        for title, cmd in commands:
            print(f"\n{title}:")
            print("-" * 40)
            response = send_command(ser, cmd, wait=0.5)
            # Extract the relevant part (skip echo and >>> prompt)
            lines = response.strip().split('\n')
            for line in lines:
                if line.strip() and not line.startswith('>>>'):
                    clean_line = line.replace('>>>', '').strip()
                    if clean_line and clean_line != cmd:
                        print(f"  {clean_line}")
        
        print("\n" + "=" * 60)
        print("Information gathering complete!")
        
        # Soft reset the badge
        print("\nResetting badge...")
        ser.write(b'\x04')  # Ctrl+D
        time.sleep(1)
        
    except serial.SerialException as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 1
    finally:
        if ser is not None:
            ser.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
