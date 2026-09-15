#!/bin/bash
# Construye la imagen y la sube a Amazon ECR.
# Se ejecuta en AWS CloudShell, desde la carpeta donde están app.py y el Dockerfile.
# Uso:  bash subir_imagen.sh v1      (o v2, v3... para las versiones siguientes)
set -e

VERSION="${1:-v1}"
REGION="us-east-1"
REPO="demo-fargate"
CUENTA=$(aws sts get-caller-identity --query Account --output text)
REGISTRO="$CUENTA.dkr.ecr.$REGION.amazonaws.com"

echo "== 1. Crear el repositorio en ECR (si ya existe, sigue) =="
aws ecr describe-repositories --repository-names "$REPO" --region "$REGION" >/dev/null 2>&1 \
  || aws ecr create-repository --repository-name "$REPO" --region "$REGION" >/dev/null
echo "   repositorio: $REGISTRO/$REPO"

echo "== 2. Iniciar sesión de Docker en ECR =="
aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$REGISTRO"

echo "== 3. Construir la imagen para x86_64 (la arquitectura de la definición de tarea) =="
docker build --platform linux/amd64 -t "$REPO:$VERSION" .

echo "== 4. Etiquetarla con la dirección de ECR =="
docker tag "$REPO:$VERSION" "$REGISTRO/$REPO:$VERSION"

echo "== 5. Subirla =="
docker push "$REGISTRO/$REPO:$VERSION"

echo
echo "LISTO. Copia esta dirección en el campo «URI de la imagen» de la definición de tarea:"
echo "   $REGISTRO/$REPO:$VERSION"
