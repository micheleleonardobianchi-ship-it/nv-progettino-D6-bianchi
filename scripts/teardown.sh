#!/bin/bash

# Sposta l'esecuzione nella root del progetto
cd "$(dirname "$0")/.."

echo "--- Spegnimento e rimozione container/volumi ---"
docker compose down -v --remove-orphans

echo "--- Pulizia completata ---"
