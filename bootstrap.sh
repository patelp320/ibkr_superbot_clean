#!/bin/bash
set -e
echo "🔧 Bootstrapping IBKR Superbot..."
mkdir -p data logs local_cache
docker compose build --no-cache
docker compose up -d
docker compose logs -f trader
