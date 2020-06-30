#!/bin/bash

set -e

printf "Found files in workspace:\n"
ls

# GITHUB_REPOSITORY is required for actions
if [ -z "${GITHUB_REPOSITORY}" ]; then
    printf "GitHub Repository (GITHUB_REPOSITORY) environment variable is required for generation.\n"
    exit 1
fi

# GITHUB_TOKEN is recommended
if [ -z "${GITHUB_TOKEN}" ]; then
    printf "Warning, you might want to export GITHUB_TOKEN to increase API limits.\n"
else
    export PRIVATE_TOKEN="${GITHUB_TOKEN}"
fi


# Define the log level
export LOG_LEVEL="${INPUT_LOG_LEVEL}"

# Determine if we are running each parser
RUN_ALLCONTRIB="false"
RUN_ZENODO="false"

if [ "${INPUT_PARSERS}" == "all" ]; then
    RUN_ALLCONTRIB="true"
    RUN_ZENODO="true"
elif [[ "${INPUT_PARSERS}" == *"zenodo"* ]]; then
    RUN_ZENODO="true"
elif [[ "${INPUT_PARSERS}" == *"allcontrib"* ]]; then
    RUN_ALLCONTRIB="true"
fi

# Update the user:
printf "Run zenodo: ${RUN_ZENODO}\n"
printf "Run allcontrib: ${RUN_ALLCONTRIB}\n"

# The .all-contributorsrc is required, generate headless if doesn't exist
if [ ! -f "${INPUT_ALLCONTRIB_FILE}" ] && [ "${RUN_ALLCONTRIB}" == "true" ]; then
    printf "Generating ${INPUT_ALLCONTRIB_FILE} for ${GITHUB_REPOSITORY}\n"
    tributors init allcontrib
    cat "${INPUT_ALLCONTRIB_FILE}"
else
    printf "${INPUT_ALLCONTRIB_FILE} already exists.\n"
fi

# If a Zenodo DOI is set, use it to init the repository
if [ ! -z "${INPUT_ZENODO_DOI}" ] && [ "${RUN_ZENODO}" == "true" ]; then
    if [ "$INPUT_FORCE" == "true" ]; then
        tributors init zenodo --doi "${INPUT_ZENODO_DOI}" --zenodo-file "${INPUT_ZENODO_FILE}" --force
    else
        tributors init zenodo --doi "${INPUT_ZENODO_DOI}" --zenodo-file "${INPUT_ZENODO_FILE}"
    fi
fi

# Update all types request
COMMAND="tributors update ${INPUT_PARSERS} --thresh ${INPUT_THRESHOLD}" 
if [ ! -z "${INPUT_ALLCONTRIB_TYPE}" ] && [ "${RUN_ALLCONTRIB}" == "true" ]; then
    COMMAND="${COMMAND} --allcontrib-type ${INPUT_ALLCONTRIB_TYPE}"
fi

echo $COMMAND
$COMMAND

# Finally, run all-contributors generate
if [ "${INPUT_ALLCONTRIB_SKIP_GENERATE}" == "false" ]; then
    printf "Running all-contributors generate\n"
    cli.js generate
fi
