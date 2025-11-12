#!/bin/bash
set -euo pipefail

echo "Etape 1: Lancement migration..."
docker compose run --rm migration

echo "Etape 2: Lancement service Mongo et Backup..."
docker compose up -d mongo mongo-backup

echo "Etape 3: Lancement tests..."
docker compose --profile run-tests up --build --abort-on-container-exit

echo "Etape 4: Nettoyage migration et tests..."

# Remove all containers with names containing "-migration" or "-test"
CONTAINERS_TO_REMOVE=$(docker ps -a --format '{{.Names}}' | grep -E '\-migration|\-test' || true)
if [ -n "$CONTAINERS_TO_REMOVE" ]; then
  echo "Removing containers:"
  echo "$CONTAINERS_TO_REMOVE"
  docker rm -f $CONTAINERS_TO_REMOVE || true
else
  echo "Aucun container Test ou migration à supprimer."
fi

# Remove all images with names containing "-migration" or "-test"
IMAGES_TO_REMOVE=$(docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' | grep -E '\-migration|\-test' || true)
if [ -n "$IMAGES_TO_REMOVE" ]; then
  echo "Removing images:"
  echo "$IMAGES_TO_REMOVE" | awk '{print $2}' | xargs -r docker rmi || true
else
  echo "Aucune image Test ou migration à supprimer."
fi

echo "Etape 5: Ouverture Mongo Shell..."

# Trouver automatiquement le container mongo en cours
MONGO_CONTAINER=$(docker ps --filter "name=mongo" --format '{{.Names}}' | head -n 1)

if [ -n "$MONGO_CONTAINER" ]; then
  echo "Connexion a Mongo via le container : $MONGO_CONTAINER"
  docker exec -it "$MONGO_CONTAINER" mongosh
else
  echo "Le container Mongo n'est pas lance."
fi