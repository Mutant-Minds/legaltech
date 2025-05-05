#!/bin/bash
set -euo pipefail

COMMAND=$1
EXTRA_ARGUMENTS=("${@:2}")

SERVICES=$(find backend/services -mindepth 1 -maxdepth 1 -type d -printf '%f\n')
for SERVICE in $SERVICES; do
  ENV_PATH="backend/services/$SERVICE/.env"
  if [ ! -f "$ENV_PATH" ]; then
    echo "Creating empty .env for backend/services/$SERVICE"
    touch "$ENV_PATH"
  fi

  ENV_TESTING_PATH="backend/services/$SERVICE/.env.test"
  if [ ! -f "$ENV_TESTING_PATH" ]; then
    echo "Warning: Missing .env.testing in $SERVICE"
  fi
done

for SERVICE in $SERVICES; do
  echo "Running '$COMMAND' for service: $SERVICE"
  docker compose run --rm test "$SERVICE" --run "$COMMAND" "${EXTRA_ARGUMENTS[@]}"
done
