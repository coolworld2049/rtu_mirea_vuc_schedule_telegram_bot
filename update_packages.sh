#!/usr/bin/env bash

poetry cache clear pypi --all -q &>/dev/null
poetry add rtu-mirea-vuc-schedule-client@latest &>/dev/null
poetry cache clear pypi --all -q
poetry add rtu-mirea-vuc-schedule-client@latest
poetry lock --no-update
