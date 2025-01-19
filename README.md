# TinyLab AI Text Summarizer

A Flask-based web application that leverages Google Cloud Vertex AI (Gemini Pro) for text summarization.

## Features

- Text summarization using Google's Gemini Pro model
- Simple and intuitive web interface
- Containerized deployment with Docker
- Cloud Run deployment support
- Custom domain configuration

## Prerequisites

- Google Cloud Account with billing enabled
- Docker installed
- gcloud CLI installed and configured
- Domain name (optional, for custom domain setup)

## Project Structure

```
summarizer/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
├── static/              # Static assets
│   └── logo.png        # Application logo
└── templates/           # HTML templates
    └── index.html      # Main application template
```

## Quick Start

### 1. Google Cloud Setup

```bash
# Login to Google Cloud
gcloud auth login

# Set project ID
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com
```

### 2. Create Artifact Registry Repository

```bash
gcloud artifacts repositories create summarizer-image \
    --repository-format=docker \
    --location=YOUR_REGION
```

### 3. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up local authentication for Vertex AI
gcloud auth application-default login

# Run locally
python app.py
```

### 4. Docker Build and Deploy

```bash
# Build Docker image
docker build -t summarizer-image .

# Tag for Artifact Registry
docker tag summarizer-image \
    YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_ID/summarizer-image/summarizer:latest

# Configure Docker authentication
gcloud auth configure-docker YOUR_REGION-docker.pkg.dev

# Push to Artifact Registry
docker push \
    YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_ID/summarizer-image/summarizer:latest

# Deploy to Cloud Run
gcloud run deploy summarizer \
    --image YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_ID/summarizer-image/summarizer:latest \
    --platform managed \
    --region YOUR_REGION \
    --memory 512Mi \
    --allow-unauthenticated
```

## Custom Domain Configuration

### Region Support Check

```bash
gcloud beta run domain-mappings create \
    --service summarizer \
    --domain your-domain.com \
    --region your-region \
    --platform managed
```

Note: If you receive a 501 error, the region doesn't support domain mappings. Consider using an alternative region (e.g., asia-southeast1 for Asia-Pacific).

### DNS Configuration Steps

1. Verify domain ownership:
```bash
gcloud domains verify your-domain.com
```

2. Add CNAME record in your DNS settings:
   - Name/Host: app (for app.your-domain.com)
   - Type: CNAME
   - Value: ghs.googlehosted.com
   - TTL: 3600

3. Create domain mapping:
```bash
gcloud beta run domain-mappings create \
    --service summarizer \
    --domain app.your-domain.com \
    --region YOUR_REGION \
    --platform managed
```

### Domain Mapping Status

Monitor the status:
```bash
gcloud beta run domain-mappings describe \
    --domain app.your-domain.com \
    --region YOUR_REGION
```

Expected status conditions:
- Ready: True
- CertificateProvisioned: True
- DomainRoutable: True

## Monitoring

```bash
# View application logs
gcloud run services logs read summarizer --region YOUR_REGION

# Check service status
gcloud run services describe summarizer --region YOUR_REGION

# List domain mappings
gcloud beta run domain-mappings list --region YOUR_REGION
```

## Dependencies

Key dependencies are specified in `requirements.txt`:
```
Flask==2.0.1
Werkzeug==2.0.1
gunicorn==23.0.0
google-cloud-aiplatform>=1.35.0
vertexai>=1.0.0
```

## Development Workflow

1. Make local changes
2. Test locally with `python app.py`
3. Build and deploy:
```bash
docker build -t summarizer-image .
docker tag summarizer-image YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_ID/summarizer-image/summarizer:latest
docker push YOUR_REGION-docker.pkg.dev/YOUR_PROJECT_ID/summarizer-image/summarizer:latest
```

## License

[MIT License](LICENSE)
