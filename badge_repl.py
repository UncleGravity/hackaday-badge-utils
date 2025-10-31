#!/usr/bin/env python3
"""
Interactive REPL for Supercon 2025 Badge
Connects to the MicroPython REPL on the badge and provides interactive terminal
"""
import serial
import sys
import threading
import time

SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 115200

def read_serial(ser):
    """Continuously read from serial port and print to stdout"""
    while True:
        try:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                sys.stdout.write(data.decode('utf-8', errors='ignore'))
                sys.stdout.flush()
        except Exception as e:
            print(f"\nError reading: {e}")
            break

def main():
    print(f"Connecting to badge on {SERIAL_PORT}...")
    ser = None
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print("Connected! Press Ctrl+C to enter REPL, Ctrl+D to exit.")
        print("=" * 60)
        
        # Start reader thread
        reader = threading.Thread(target=read_serial, args=(ser,), daemon=True)
        reader.start()
        
        # Send Ctrl+C to interrupt and enter REPL
        time.sleep(0.5)
        ser.write(b'\x03')  # Ctrl+C
        time.sleep(0.5)
        
        # Interactive loop
        while True:
            try:
                user_input = input()
                ser.write((user_input + '\r\n').encode('utf-8'))
            except EOFError:
                break
            except KeyboardInterrupt:
                print("\nSending interrupt...")
                ser.write(b'\x03')  # Ctrl+C
                
    except serial.SerialException as e:
        print(f"Error: {e}")
        print("Make sure the badge is connected and not in use by another program.")
        return 1
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if ser is not None:
            ser.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
