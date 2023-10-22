#!/usr/bin/env bash

poetry cache clear pypi --all -q &>/dev/null
poetry add schedule-service-client@latest &>/dev/null
poetry cache clear pypi --all -q
poetry add schedule-service-client@latest
poetry update
