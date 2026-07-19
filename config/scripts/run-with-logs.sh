#!/bin/sh
set -eu

common_log=$1
service_log=$2
shift 2

mkdir -p "$(dirname "$common_log")" "$(dirname "$service_log")"
touch "$common_log" "$service_log"
"$@" 2>&1 | tee -a "$common_log" "$service_log"

