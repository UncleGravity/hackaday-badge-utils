#!/usr/bin/env python3
"""
Real-time Badge Monitor for Supercon 2025 Badge
Monitors serial output with timestamps and optional logging
"""
import serial
import sys
import time
from datetime import datetime

SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 115200

def main():
    log_file = None
    
    # Parse arguments
    if len(sys.argv) > 1:
        log_filename = sys.argv[1]
        log_file = open(log_filename, 'a')
        print(f"Logging to: {log_filename}")
    
    print("Supercon 2025 Badge Monitor")
    print("=" * 60)
    print(f"Port: {SERIAL_PORT} @ {BAUD_RATE} baud")
    print("Press Ctrl+C to exit")
    print("=" * 60)
    
    ser = None
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        
        while True:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                
                # Print to console
                for line in data.splitlines():
                    if line.strip():
                        output = f"[{timestamp}] {line}"
                        print(output)
                        
                        # Write to log file if specified
                        if log_file:
                            log_file.write(output + '\n')
                            log_file.flush()
            else:
                time.sleep(0.1)
                
    except serial.SerialException as e:
        print(f"\nError: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
    finally:
        if ser is not None:
            ser.close()
        if log_file is not None:
            log_file.close()
            print(f"Log saved to: {log_file.name}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
