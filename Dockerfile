FROM python:3.10-slim

# Setup user for Hugging Face Spaces (UID 1000)
RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HF_HOME=/home/user/app/hf_cache

WORKDIR $HOME/app

# Install Python dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (Frontend is ignored via .dockerignore)
COPY --chown=user . .

EXPOSE 7860

# Start FastAPI and Gradio app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
