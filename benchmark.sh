#!/bin/bash


project_name="$(date +"%Y%m%d%H%M%S")-$(hostname | tr '[:upper:]' '[:lower:]')"



cleanup() {
    echo "Cleaning up..."
    docker rm -f dogefuzz_benchmark_$project_name &>/dev/null
    docker compose -p $project_name down &>/dev/null
    exit 0
}

trap 'cleanup' SIGTERM SIGKILL INT

mkdir -p results

echo "[1] Starting fuzzer and dependencies"

docker compose -p $project_name up -d;

echo "[1.1] Wait for all containers to be healthy"
while true; do
  dogefuzz_id=$(docker ps --filter "name=$project_name-dogefuzz" -q)
  health_status=$(docker inspect --format='{{.State.Health.Status}}' $dogefuzz_id);

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
    --network ${project_name}_default \
    --network-alias benchmark \
    --name dogefuzz_benchmark_$project_name \
    --init \
    -it \
    -p "5000" \
    -v "$PWD/results:/app/results" \
    -v "$PWD/dataset:/app/dataset" \
    benchmark:1.0.0 \
    $@;

echo "[4] Stopping all containers"
cleanup
