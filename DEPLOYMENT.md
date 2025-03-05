# Orbical Website Deployment Guide

This guide provides instructions for deploying the Orbical website in a production environment.

## Deployment Options

The Orbical website can be deployed in two ways:

1. **Using the pre-built binary**: A simple approach that requires minimal setup.
2. **Using Gunicorn with the source code**: A more flexible approach that allows for better performance and configuration.

## Option 1: Using the Pre-built Binary

### Prerequisites
- Linux server (the binary is built for Linux)
- A user account with appropriate permissions (preferably not root)

### Deployment Steps

1. **Copy the deployment package to your server**:
   ```bash
   scp -r deploy/* user@your-server:/path/to/deployment/
   ```

2. **Set up the binary to run on system startup**:
   Create a systemd service file at `/etc/systemd/system/orbical.service`:
   ```
   [Unit]
   Description=Orbical Website
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/deployment
   ExecStart=/path/to/deployment/orbical
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service**:
   ```bash
   sudo systemctl enable orbical
   sudo systemctl start orbical
   ```

4. **Set up a reverse proxy (recommended)**:
   For better security and performance, set up Nginx or Apache as a reverse proxy:

   **Nginx example**:
   ```
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Option 2: Using Gunicorn with Source Code

### Prerequisites
- Python 3.8 or higher
- pip package manager
- virtualenv (recommended)

### Deployment Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/orbical-website.git
   cd orbical-website
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a production configuration**:
   Create a `config.ini` file with the following content:
   ```ini
   [server]
   port = 5000
   host = 0.0.0.0

   [production]
   use_production_server = true
   workers = 4
   ```

5. **Set up a systemd service**:
   Create a systemd service file at `/etc/systemd/system/orbical.service`:
   ```
   [Unit]
   Description=Orbical Website
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/path/to/orbical-website
   ExecStart=/path/to/orbical-website/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 'app:app'
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

6. **Enable and start the service**:
   ```bash
   sudo systemctl enable orbical
   sudo systemctl start orbical
   ```

7. **Set up a reverse proxy** (same as in Option 1)

## Monitoring and Maintenance

- **Check service status**:
  ```bash
  sudo systemctl status orbical
  ```

- **View logs**:
  ```bash
  sudo journalctl -u orbical
  ```

- **Restart the service after updates**:
  ```bash
  sudo systemctl restart orbical
  ```

## Security Considerations

1. **Run as a non-root user**: The service should run as a dedicated user (e.g., www-data).
2. **Use HTTPS**: Set up SSL certificates with Let's Encrypt.
3. **Firewall**: Configure your firewall to only allow necessary ports.
4. **Regular updates**: Keep the system and all dependencies up to date.

## Troubleshooting

- If the service fails to start, check the logs with `journalctl -u orbical`.
- Ensure the binary or script has execute permissions.
- Verify that the port is not already in use by another service.
