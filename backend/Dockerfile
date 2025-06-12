# docker/Dockerfile

FROM python:3.11-slim

ENV USER=uv-example-user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

# Install required packages and dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /bin/bash $USER

# Set the working directory
ENV APP_DIR=/home/$USER/src
WORKDIR $APP_DIR

# Copy application files
COPY . $APP_DIR

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Python path
ENV PYTHONPATH=$APP_DIR

# Change ownership of the application directory
RUN chown -R "$USER":"$USER" $APP_DIR
USER $USER

# Command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]