#!/bin/bash
set -euo pipefail

COMMAND=$1

SERVICES=$(find backend/services -mindepth 1 -maxdepth 1 -type d -printf '%f\n')
for SERVICE in $SERVICES; do
  ENV_PATH="backend/services/$SERVICE/.env"
  if [ ! -f "$ENV_PATH" ]; then
    echo "Creating empty .env for backend/services/$SERVICE"
    touch "$ENV_PATH"
  fi

  echo "Running '$COMMAND' for service: $SERVICE"
  docker compose run --rm test "$SERVICE" --run "$COMMAND"
done
