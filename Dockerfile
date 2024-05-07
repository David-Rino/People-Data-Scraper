# Slim version of Python
FROM python:3.8.12-slim

# Download Package Information
RUN apt-get update -y

# Install necessary packages for Tkinter, Xvfb, and PostgreSQL client libraries
RUN apt-get install -y tk xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic \
                       postgresql-client libpq-dev

# Install additional utilities
RUN apt-get install -y xorg

# Create necessary X11 directories with appropriate permissions
RUN mkdir /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos "" appuser

# Set the working directory
WORKDIR /app

# Copy the application files and requirements file into the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change owner of the /app directory to the new user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Configure the ENTRYPOINT to start Xvfb and run the Python application using the virtual display
ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 1280x720x24 -ac & export DISPLAY=:99 && exec python3 /app/Main.py"]
