# ------------------------------
# Stage 1: Build frontend
# ------------------------------
FROM node:18 AS frontend-build
WORKDIR /app/frontend

# Copy package.json and install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend code and build
COPY frontend/ ./
RUN npm run build

# ------------------------------
# Stage 2: Setup backend
# ------------------------------
FROM python:3.12-slim
WORKDIR /app

# Copy backend files
COPY backend/ ./backend

# Copy frontend build output from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Install Python dependencies including gunicorn
RUN pip install --no-cache-dir flask flask-cors gunicorn

# Environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Expose the port
EXPOSE 5000

# Run backend with gunicorn for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]