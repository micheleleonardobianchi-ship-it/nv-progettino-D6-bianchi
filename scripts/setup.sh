#!/bin/bash

set -e

# Vai nella root del progetto
cd "$(dirname "$0")/.."

echo ""
echo "--- Avvio dei container e build immagini ---"

docker compose up -d --build

echo ""
echo "--- Attesa completamento container load ---"

echo ""
echo "--- Risultato del conteggio dati ---"

docker compose exec db \
  psql -U user -d mydatabase \
  -c "SELECT * FROM tdata LIMIT 10;"

echo ""
echo "--- Pipeline completata ---"

