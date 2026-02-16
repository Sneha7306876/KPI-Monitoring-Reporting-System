# Deployment Guide

## Production Deployment

### Security Considerations

1. **Debug Mode**: The application defaults to running with debug mode disabled. To enable debug mode (development only), set the environment variable:
   ```bash
   export FLASK_DEBUG=true
   python app.py
   ```

2. **User Isolation**: The current implementation uses in-memory storage for uploaded files. For production use, implement:
   - User authentication and session management
   - Database storage for file metadata
   - User-specific data isolation

3. **File Storage**: Consider using a dedicated storage service (e.g., AWS S3, Azure Blob Storage) instead of local file system storage in production.

4. **HTTPS**: Always deploy with HTTPS enabled to protect data in transit.

### Environment Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set production environment variables:
   ```bash
   export FLASK_DEBUG=false
   export FLASK_ENV=production
   ```

3. Run with a production WSGI server (e.g., Gunicorn):
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Resource Requirements

- Python 3.8+
- 1GB RAM minimum (2GB recommended for larger datasets)
- 500MB disk space for application and uploaded files

### Monitoring

Monitor the following:
- Upload folder disk usage
- Memory usage (especially the data_store dictionary)
- Request response times
- Error rates

## Development

For local development:
```bash
export FLASK_DEBUG=true
python app.py
```

The application will be available at http://localhost:5000
