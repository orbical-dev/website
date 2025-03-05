# Orbical Website

A Flask-based website that can be deployed using Docker for easy deployment on any server or cloud platform.

## Development

To run the website in development mode:

```bash
python app.py
```

This will start the Flask development server on http://localhost:5000. The development server is not suitable for production use, but it's perfect for testing and debugging.

## Docker Deployment

This project can be easily deployed using Docker and Docker Compose.

### Local Development with Docker

1. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```

2. Access the website at http://localhost:5000

### Production Deployment

#### Using Docker Compose

1. Clone the repository on your server:
   ```bash
   git clone https://github.com/orbical-dev/orbical-website.git
   cd orbical-website
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Set up a reverse proxy with Nginx (optional but recommended).

#### Using GitHub Container Registry

The Docker image is automatically built and published to GitHub Container Registry (ghcr.io) when changes are pushed to the main branch.

1. Pull the latest image:
   ```bash
   docker pull ghcr.io/orbical-dev/orbical-website:latest
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 -v $(pwd)/contact.txt:/app/contact.txt ghcr.io/orbical-dev/orbical-website:latest
   ```

## Configuration

The application is configured to run on port 5000 by default. You can modify the port in the `app.py` file or by setting environment variables in the `docker-compose.yaml` file.

When using Docker, you can mount volumes to persist data, such as the contact form submissions stored in `contact.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
