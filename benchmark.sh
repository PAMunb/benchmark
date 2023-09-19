#!/bin/bash
set -e

cleanup() {
    echo "Cleaning up..."
    docker rm -f dogefuzz_benchmark 2> /dev/null;
    docker compose down 2> /dev/null;
    exit 0
}

trap 'cleanup' SIGTERM
trap 'cleanup' SIGKILL
trap 'cleanup' INT

mkdir -p results

echo "[1] Starting fuzzer and dependencies"
docker compose up -d;

echo "[1.1] Wait for all containers to be healthy"
while true; do
  health_status=$(docker inspect --format='{{.State.Health.Status}}' dogefuzz_api);

  if [ "$health_status" = "healthy" ]; then
    echo "All containers are healthy";
    break;
  fi

  sleep 5;
done

echo "[2] Building benchmark container image"
docker build -t benchmark:1.0.0 --quiet .;

echo "[3] Running benchmark"
docker run \
    --rm \
    --network dogefuzz_benchmark \
    --network-alias benchmark \
    --name dogefuzz_benchmark \
    -p "5000:5000" \
    -v "$PWD/results:/app/results" \
    -v "$PWD/dataset:/app/dataset" \
    benchmark:1.0.0 \
    $@;

echo "[4] Stopping all containers"
cleanup