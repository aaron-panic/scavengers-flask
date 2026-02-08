FROM python:3.12-slim

WORKDIR /app

# Install dependencies
# We copy this separately to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We don't COPY the app code here because the Compose volume 
# will overwrite it. This keeps the image build fast.

# Default command
CMD ["flask", "run", "--host=0.0.0.0"]
