#!/usr/bin/env python3
"""
Sales Forge - Combined Startup Script
Starts both FastAPI backend and React frontend simultaneously
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

# Colors for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    RESET = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.RESET}")

def print_header():
    """Print application header"""
    print_colored("🚀 Sales Forge - AI Sales Intelligence Platform", Colors.PURPLE)
    print_colored("=" * 50, Colors.PURPLE)
    print_colored("Starting both Backend (FastAPI) and Frontend (React + Tailwind)...", Colors.BLUE)
    print()

def check_dependencies():
    """Check if required dependencies are available"""
    print_colored("🔍 Checking dependencies...", Colors.YELLOW)
    
    # Check Python dependencies
    try:
        import fastapi, uvicorn, pydantic
        print_colored("   ✅ Python dependencies: OK", Colors.GREEN)
    except ImportError:
        print_colored("   ❌ Python dependencies missing. Installing...", Colors.RED)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_colored("   ✅ Python dependencies: Installed", Colors.GREEN)
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_colored(f"   ✅ Node.js: {result.stdout.strip()}", Colors.GREEN)
        else:
            print_colored("   ❌ Node.js not found", Colors.RED)
            return False
    except FileNotFoundError:
        print_colored("   ❌ Node.js not found", Colors.RED)
        return False
    
    print()
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print_colored("🔧 Starting Backend (FastAPI)...", Colors.GREEN)
    print_colored("   📍 Location: http://localhost:8000", Colors.CYAN)
    print_colored("   📚 API Docs: http://localhost:8000/api/docs", Colors.CYAN)
    print()
    
    # Run backend from project root to maintain proper import paths
    process = subprocess.Popen(
        [sys.executable, 'backend/application.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    return process

def start_frontend():
    """Start the React frontend server"""
    print_colored("🎨 Starting Frontend (React + Tailwind)...", Colors.GREEN)
    print_colored("   📍 Location: http://localhost:3000", Colors.CYAN)
    print()
    
    os.chdir('frontend')
    
    # Install dependencies if needed
    if not os.path.exists('node_modules'):
        print_colored("   📦 Installing npm dependencies...", Colors.YELLOW)
        subprocess.run(['npm', 'install'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    process = subprocess.Popen(
        ['npm', 'start'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    os.chdir('..')
    return process

def monitor_process(process, name, color):
    """Monitor a process and print its output"""
    for line in process.stdout:
        if line.strip():
            print_colored(f"[{name}] {line.strip()}", color)

def main():
    """Main function to start both services"""
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print_header()
    
    # Check dependencies
    if not check_dependencies():
        print_colored("❌ Dependencies check failed. Please install Node.js and try again.", Colors.RED)
        return 1
    
    processes = []
    threads = []
    
    try:
        # Start backend
        backend_process = start_backend()
        processes.append(('Backend', backend_process))
        
        # Wait for backend to start
        time.sleep(2)
        
        # Start frontend
        frontend_process = start_frontend()
        processes.append(('Frontend', frontend_process))
        
        # Wait for frontend to start
        time.sleep(3)
        
        print_colored("🎉 Sales Forge is now running!", Colors.PURPLE)
        print_colored("=" * 30, Colors.PURPLE)
        print_colored("✅ Backend:  http://localhost:8000 (API + Documentation)", Colors.GREEN)
        print_colored("✅ Frontend: http://localhost:3000 (Main Application)", Colors.GREEN)
        print()
        print_colored("📋 Usage:", Colors.YELLOW)
        print_colored("   1. Open http://localhost:3000 in your browser", Colors.WHITE)
        print_colored("   2. Navigate between tabs: Advance-Agents, Crew Agents, IBM Agents", Colors.WHITE)
        print_colored("   3. In Advance-Agents tab, select a workflow and analyze leads", Colors.WHITE)
        print_colored("   4. View comprehensive AI intelligence results", Colors.WHITE)
        print()
        print_colored("🛑 To stop: Press Ctrl+C in this terminal", Colors.YELLOW)
        print()
        print_colored("🔍 Server logs:", Colors.BLUE)
        print_colored("=" * 20, Colors.BLUE)
        
        # Start monitoring threads
        backend_thread = threading.Thread(
            target=monitor_process, 
            args=(backend_process, 'Backend', Colors.BLUE)
        )
        frontend_thread = threading.Thread(
            target=monitor_process, 
            args=(frontend_process, 'Frontend', Colors.GREEN)
        )
        
        backend_thread.daemon = True
        frontend_thread.daemon = True
        
        backend_thread.start()
        frontend_thread.start()
        
        threads.extend([backend_thread, frontend_thread])
        
        # Wait for processes
        for name, process in processes:
            process.wait()
            
    except KeyboardInterrupt:
        print_colored("\n🛑 Shutting down Sales Forge...", Colors.YELLOW)
        
    except Exception as e:
        print_colored(f"❌ Error: {e}", Colors.RED)
        
    finally:
        # Clean up processes
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print_colored(f"✅ {name} stopped", Colors.GREEN)
            except subprocess.TimeoutExpired:
                process.kill()
                print_colored(f"🔪 {name} killed", Colors.YELLOW)
            except Exception:
                pass
        
        print_colored("✅ All services stopped", Colors.GREEN)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())