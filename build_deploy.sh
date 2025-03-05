#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create config.ini file first (this will be included in the binary)
cat > config.ini << EOF
[server]
port = 5000
host = 0.0.0.0

[production]
use_production_server = false
workers = 4
EOF

# Build the binary using PyInstaller as a static binary
pyinstaller --clean orbical.spec

# Create a deployment package
mkdir -p deploy
cp dist/orbical deploy/
chmod +x deploy/orbical
cp -r deploy_config/* deploy/ 2>/dev/null || :

# Create a production-ready systemd service file
mkdir -p deploy/systemd
cat > deploy/systemd/orbical.service << EOF
[Unit]
Description=Orbical Website
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/orbical
ExecStart=/opt/orbical/orbical
Environment="PATH=/usr/bin:/usr/local/bin"
Restart=always
RestartSec=5
TimeoutStartSec=30
TimeoutStopSec=30

# Security enhancements
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
EOF

# Create deployment instructions
cat > deploy/README.md << EOF
# Orbical Website Deployment

This package contains a standalone binary for the Orbical website.

## Deployment Instructions

1. Copy the contents of this directory to your VPS (e.g., using scp or rsync):
   \`\`\`
   rsync -avz --progress ./deploy/ user@your-vps:/tmp/orbical/
   \`\`\`

2. SSH into your VPS and run the following commands:
   \`\`\`
   sudo mkdir -p /opt/orbical
   sudo cp -r /tmp/orbical/* /opt/orbical/
   sudo chmod +x /opt/orbical/orbical
   sudo cp /opt/orbical/systemd/orbical.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable orbical
   sudo systemctl start orbical
   \`\`\`

3. Configure your web server (nginx/apache) as a reverse proxy (optional):
   
   Example nginx configuration:
   \`\`\`
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host \$host;
           proxy_set_header X-Real-IP \$remote_addr;
       }
   }
   \`\`\`

4. Set up SSL with Let's Encrypt (recommended):
   \`\`\`
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   \`\`\`
EOF

# Create a deployment config directory
mkdir -p deploy_config

# Create a production configuration file
cat > deploy_config/config.ini << EOF
[server]
port = 5000
host = 0.0.0.0

[production]
use_production_server = false
workers = 4
EOF

echo "Production configuration set with use_production_server = false"

# Create a development configuration file for reference
cat > config.ini << EOF
[server]
port = 5000
host = 0.0.0.0

[production]
use_production_server = false
workers = 4
EOF

echo "Build complete! Deployment package created in the 'deploy' directory."
echo "Run './build_deploy.sh' to build the binary and create a deployment package."
