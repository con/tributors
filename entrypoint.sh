#!/bin/bash

set -e

printf "Found files in workspace:\n"
ls

# GITHUB_REPOSITORY is required
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

# The .all-contributorsrc is required, generate headless if doesn't exist
if [ ! -f ".all-contributorsrc" ]; then   
    printf "Generating .all-contributorsrc for ${GITHUB_REPOSITORY}\n"
    a2z init "${GITHUB_REPOSITORY}"
    cat .all-contributorsrc
else
    printf ".all-contributorsrc already exists.\n"
fi

# IF a Zenodo DOI is set, use it to init the repository
if [ ! -z "${INPUT_ZENODO_DOI}" ]; then
    if [ "$INPUT_FORCE" == "true" ]; then
        a2z init --zenodo "${INPUT_ZENODO_DOI}" --zenodo-file "${INPUT_ZENODO_FILE}" --force
    else
        a2z init --zenodo "${INPUT_ZENODO_DOI}" --zenodo-file "${INPUT_ZENODO_FILE}"
    fi
fi

# Update all contributors file
a2z update all --ctype "${INPUT_CTYPE}"

# Finally, run all-contributors generate
if [ "${INPUT_SKIP_GENERATE}" == "false" ]; then
    printf "Running all-contributors generate\n"
    cli.js generate
fi
