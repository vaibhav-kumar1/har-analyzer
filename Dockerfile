# Stage 2: Setup backend
FROM python:3.12-slim
WORKDIR /app

# Copy backend files
COPY backend/ ./backend

# Copy frontend build output
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Install Python dependencies including gunicorn
RUN pip install --no-cache-dir flask flask-cors gunicorn

# Environment variables
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
EXPOSE 5000
ENV PORT 5000

# Run backend with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]