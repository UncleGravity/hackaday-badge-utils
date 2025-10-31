#!/usr/bin/env python3
"""
File Manager for Supercon 2025 Badge
Upload, download, and manage files on the badge filesystem
Uses mpremote (official MicroPython tool) for reliable file operations
"""
import sys
import os
import subprocess

SERIAL_PORT = "/dev/cu.usbmodem2101"

def mpremote_cmd(*args):
    """Run an mpremote command without resetting the device"""
    # Use 'connect' + 'resume' to connect without soft-reset that turns off display
    cmd = ['mpremote', 'connect', SERIAL_PORT, 'resume'] + list(args)
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0

def list_files(path='/'):
    """List files in a directory on the badge"""
    print(f"Listing files in: {path}")
    # mpremote automatically formats output nicely
    mpremote_cmd('fs', 'ls', f':{path}')
    return True

def read_file(filepath):
    """Read and display a file from the badge"""
    print(f"Reading file: {filepath}")
    print("-" * 60)
    # Use mpremote to cat the file
    mpremote_cmd('fs', 'cat', f':{filepath}')
    return True

def upload_file(local_path, remote_path):
    """Upload a file to the badge"""
    if not os.path.exists(local_path):
        print(f"Error: Local file '{local_path}' not found")
        return False
    
    print(f"Uploading: {local_path} -> {remote_path}")
    success = mpremote_cmd('fs', 'cp', local_path, f':{remote_path}')
    
    if success:
        print("✓ Upload successful!")
    else:
        print("✗ Upload failed!")
    
    return success

def download_file(remote_path, local_path):
    """Download a file from the badge"""
    print(f"Downloading: {remote_path} -> {local_path}")
    success = mpremote_cmd('fs', 'cp', f':{remote_path}', local_path)
    
    if success:
        # Show file info
        if os.path.exists(local_path):
            size = os.path.getsize(local_path)
            with open(local_path, 'r') as f:
                lines = len(f.readlines())
            print(f"✓ Download successful! {size} bytes ({lines} lines) saved to: {local_path}")
        else:
            print("✓ Download completed")
    else:
        print("✗ Download failed!")
    
    return success

def delete_file(filepath):
    """Delete a file from the badge"""
    print(f"Deleting: {filepath}")
    success = mpremote_cmd('fs', 'rm', f':{filepath}')
    
    if success:
        print("✓ File deleted successfully!")
    else:
        print("✗ Delete failed!")
    
    return success

def main():
    if len(sys.argv) < 2:
        print("Badge File Manager for Supercon 2025")
        print("Powered by mpremote (official MicroPython tool)")
        print("\nUsage:")
        print(f"  {sys.argv[0]} ls [path]                - List files")
        print(f"  {sys.argv[0]} cat <file>               - Read file")
        print(f"  {sys.argv[0]} download <remote> <local> - Download file")
        print(f"  {sys.argv[0]} upload <local> <remote>  - Upload file")
        print(f"  {sys.argv[0]} rm <file>                - Delete file")
        return 1
    
    command = sys.argv[1]
    
    try:
        if command == 'ls':
            path = sys.argv[2] if len(sys.argv) > 2 else '/'
            list_files(path)
            
        elif command == 'cat':
            if len(sys.argv) < 3:
                print("Error: No file specified")
                return 1
            read_file(sys.argv[2])
            
        elif command == 'download':
            if len(sys.argv) < 4:
                print("Error: Need remote and local paths")
                return 1
            success = download_file(sys.argv[2], sys.argv[3])
            return 0 if success else 1
            
        elif command == 'upload':
            if len(sys.argv) < 4:
                print("Error: Need local and remote paths")
                return 1
            success = upload_file(sys.argv[2], sys.argv[3])
            return 0 if success else 1
            
        elif command == 'rm':
            if len(sys.argv) < 3:
                print("Error: No file specified")
                return 1
            success = delete_file(sys.argv[2])
            return 0 if success else 1
            
        else:
            print(f"Unknown command: {command}")
            return 1
        
    except KeyboardInterrupt:
        print("\nInterrupted")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
