FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create contact.txt with appropriate permissions
RUN touch contact.txt && chmod 666 contact.txt

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
