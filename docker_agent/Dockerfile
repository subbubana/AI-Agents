# Use official Python base image
FROM python:3.13

# Install nodejs (needed for npx)
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy your app code (assuming main.py is in current folder)
COPY . /app

# Install Python dependencies (add your requirements if any)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install python-dotenv openai-agents

# Ensure npx is available and install MCP filesystem server (optional pre-install to speed startup)
RUN npm install -g @modelcontextprotocol/server-filesystem

# Expose port (if needed, your app currently CLI based)
# EXPOSE 8080

# Default command to start your app
CMD ["python", "main.py"]
