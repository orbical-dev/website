# Orbical Website

A Flask-based website that can be compiled into a static binary for easy deployment on VPS servers.

## Development

To run the website in development mode:

```bash
python launcher.py
```

This will start the Flask development server on http://localhost:5000. The development server is not suitable for production use, but it's perfect for testing and debugging.

## Building a Static Binary

This project uses PyInstaller to create a standalone binary that includes all dependencies.

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   ./build_deploy.sh
   ```

3. The binary and deployment files will be created in the `deploy` directory.

## Deployment

The build script creates a complete deployment package in the `deploy` directory. Follow the instructions in `deploy/README.md` to deploy the application to your VPS.

### Quick Deployment Steps

1. Copy the deployment package to your VPS:
   ```bash
   rsync -avz --progress ./deploy/ user@your-vps:/tmp/orbical/
   ```

2. SSH into your VPS and install the application:
   ```bash
   sudo mkdir -p /opt/orbical
   sudo cp -r /tmp/orbical/* /opt/orbical/
   sudo chmod +x /opt/orbical/orbical
   sudo cp /opt/orbical/systemd/orbical.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable orbical
   sudo systemctl start orbical
   ```

3. Set up a reverse proxy with Nginx (optional but recommended).

## Configuration

The application can be configured using the `config.ini` file. The following options are available:

```ini
[server]
port = 5000
host = 0.0.0.0

[production]
use_production_server = false
workers = 4
```

The `use_production_server` option is currently set to `false` to use the Flask development server. This is suitable for development and testing purposes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
