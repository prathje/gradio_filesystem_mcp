FROM python:3.10-slim as base


# Install Gradio and copy local files
WORKDIR /app

ARG FILES_DIR=/app/files
ENV FILES_DIR=$FILES_DIR

ENV ALLOW_EDITING=true

RUN pip install --no-cache-dir gradio[mcp]
COPY . .

RUN useradd -m -u 1000 user

RUN chown -R user:user /app
USER user

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]