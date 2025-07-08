FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc curl \
    libpq-dev \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements requirements
RUN pip install --upgrade pip
RUN pip install -r requirements

RUN mkdir -p /models

RUN python -c "import os; \
    from transformers import AutoModelForCausalLM, AutoTokenizer; \
    print('Downloading Qwen2.5-0.5B-Instruct model...'); \
    model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct'); \
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct'); \
    print('Saving model to local directory...'); \
    model.save_pretrained('/models/qwen2.5-0.5b-instruct'); \
    tokenizer.save_pretrained('/models/qwen2.5-0.5b-instruct'); \
    print('Model saved successfully!')"

ENV MODEL_PATH=/models/qwen2.5-0.5b-instruct

RUN ls -la /models/qwen2.5-0.5b-instruct/
