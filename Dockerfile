# ------------------------------
# Stage 1: Build frontend
# ------------------------------
FROM node:18 as frontend-build
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

# Copy frontend build output into backend static folder
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-cors

# Environment variables for Flask
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production

# Expose a port (Railway will override with dynamic $PORT)
EXPOSE 5000

# Start backend with production-ready settings
CMD ["python", "backend/app.py"]