#!/bin/bash

# Load environment variables
source .env

trap 'echo -e "\nMonitoring stopped."; exit 0' INT

nohup bash -c '
CONTAINER="'${CONTAINER_NAME}'"
RESTART_MODEL="'${RESTART_MODEL}'"
pid=$$
echo "Monitor script started with PID: $pid" > monitor.log

while true; do
    output=$(docker exec $CONTAINER nvidia-smi 2>&1)
    
    if [[ $output == *"Failed to initialize NVML: Unknown Error"* ]]; then
        echo "$(date): NVML error detected, restarting $CONTAINER..." >> monitor.log
        docker restart $CONTAINER
        
        if [ ! -z "$RESTART_MODEL" ]; then
            sleep 5
            docker exec $CONTAINER ollama run $RESTART_MODEL --keepalive -1h
        fi
        
        echo "$(date): Container restarted" >> monitor.log
    fi
    
    sleep 60
done' >> monitor.log 2>&1 &

echo "Monitoring started in background (PID: $!)"
echo "Check monitor.log for output"
