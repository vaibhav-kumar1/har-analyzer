# Stage 1: Build frontend
FROM node:18 as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Setup backend
FROM python:3.12-slim
WORKDIR /app
COPY backend/ ./backend
COPY --from=frontend-build /app/frontend/build ./frontend/build
RUN pip install --no-cache-dir flask flask-cors

# Serve frontend via Flask static
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
EXPOSE 5000

CMD ["python", "backend/app.py"]