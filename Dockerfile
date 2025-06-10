FROM python:3.10-slim as base


# Install Gradio and copy local files
WORKDIR /app

ARG FILES_DIR=/app/files
ENV FILES_DIR=$FILES_DIR

ENV ALLOW_EDITING=true

RUN pip install --no-cache-dir gradio[mcp]
COPY . .


WORKDIR /app

RUN useradd -m -u 1000 user

RUN chown -R user:user /app
USER user

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]

FROM base as main

USER root
RUN apt-get update && apt-get install -y git

ENV ALLOW_EDITING=false
WORKDIR /motion-canvas
ENV MC_DIR=/motion-canvas/motion-canvas

RUN git clone https://github.com/motion-canvas/motion-canvas /motion-canvas/motion-canvas

ENV MC_DOCS_DIR=/motion-canvas/motion-canvas/packages/docs/docs
ENV MC_SRC_DIR=/motion-canvas/motion-canvas/packages/core/src

RUN cp -r $MC_DOCS_DIR $FILES_DIR/docs
RUN cp -r $MC_SRC_DIR $FILES_DIR/src

WORKDIR /app
USER user