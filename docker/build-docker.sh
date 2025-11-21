#!/bin/bash

# This script builds a Docker image for the application.


docker build -t ste93/congestion-coverage-plan:latest . --build-arg BRANCH=fix/library