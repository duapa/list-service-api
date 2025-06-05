FROM python:3.10.12-alpine
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

ENV PORT=8080
WORKDIR /app

ENV PYTHONPATH=/app

# Copy and install requirements
COPY ../requirements.txt requirements.txt

# Create venv
RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir --upgrade pip

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/app ./app/

# Copy boot.sh and enable excecution
COPY boot.sh boot.sh
RUN chmod +x boot.sh

RUN chmod +x /opt/extensions/lambda-adapter

EXPOSE ${PORT}
ENTRYPOINT ["./boot.sh"]