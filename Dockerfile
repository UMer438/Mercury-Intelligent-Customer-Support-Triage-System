# Build Stage for Frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
# This will generate the static files in /app/frontend/out
RUN npm run build 

# Runtime Stage
FROM python:3.10-slim

WORKDIR /app

# Copy Backend Code
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

# Copy Built Frontend Assets explicitly to 'static' directory in backend workdir
COPY --from=frontend-builder /app/frontend/out /app/static

# Create a user to run the application (Hugging Face Spaces requirement for security, usually recommended)
# But strictly, direct execution works too. 
# Explicitly set port to 7860
ENV PORT=7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
