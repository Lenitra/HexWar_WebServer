#!/bin/bash

# Définir les variables de base
UNITY_PATH="/home/taumah/Unity/Hub/Editor/6000.0.28f1/Editor/Unity"
PROJECT_PATH="HexWar"
OUTPUT_PATH="Builds"
BUILD_METHOD="BuildAutomation.BuildAllPlatforms"
LOG_FILE="build_log.txt"
DATE=$(date +%Y_%m_%d)
FILE_NAME="HexWar_$DATE"

# Vérifier si les dossiers de sortie existent
if [ ! -d "$OUTPUT_PATH" ]; then
    mkdir -p "$OUTPUT_PATH"
fi

# Étape 1 : Exécuter Unity pour compiler le projet
echo "Building the project..."
"$UNITY_PATH" -batchmode -nographics -quit -projectPath "$PROJECT_PATH" -executeMethod "$BUILD_METHOD" -logFile "$LOG_FILE"
if [ $? -ne 0 ]; then
    echo "Build failed! Check $LOG_FILE for details."
    exit 1
fi

echo "Build completed successfully."



exit 0
