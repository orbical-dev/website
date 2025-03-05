#!/usr/bin/env python3
import configparser
import os
import sys
import multiprocessing
from app import app

def main():
    # Load configuration
    config = configparser.ConfigParser()
    
    # Try to find config.ini in multiple locations
    config_paths = [
        'config.ini',  # Current working directory
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'),  # Script directory
    ]
    
    # If running as PyInstaller bundle, also check executable directory
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        config_paths.append(os.path.join(os.path.dirname(sys.executable), 'config.ini'))
    
    # Find the first config file that exists
    config_path = None
    for path in config_paths:
        if os.path.exists(path):
            config_path = path
            print(f"Using configuration from: {path}")
            break
    
    # Default configuration
    port = 5000
    host = '0.0.0.0'
    use_production_server = False
    workers = multiprocessing.cpu_count() * 2 + 1  # Gunicorn recommended formula
    
    # Try to load configuration
    if config_path:
        try:
            config.read(config_path)
            port = config.getint('server', 'port', fallback=port)
            host = config.get('server', 'host', fallback=host)
            if config.has_section('production'):
                use_production_server = config.getboolean('production', 'use_production_server', fallback=False)
                workers = config.getint('production', 'workers', fallback=workers)
        except Exception as e:
            print(f"Warning: Could not load configuration: {e}")
    else:
        print("Warning: No config.ini found. Using default configuration.")
    
    # Always use Flask development server for simplicity
    print(f"Starting Flask development server on {host}:{port}.")
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    main()
