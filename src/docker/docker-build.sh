#!/bin/bash

echo "Ensure we are running in the proper folder"
if !([[ -d "./src/docker" ]] && [[ -f "./src/TODO:SomeFile" ]]); then 
    echo "This script must be run from the repository root folder"
    exit 1
fi

echo "Building Docker Image"
docker build --file src/docker/Dockerfile --tag ghcr.io/agile-learning-institute/mentorhub-<<TODO:domaion>>-<<TODO:component>>:latest .
if [ $? -ne 0 ]; then
    echo "Docker build failed"
    exit 1
fi

# Run the containers
mh up TODO:package
