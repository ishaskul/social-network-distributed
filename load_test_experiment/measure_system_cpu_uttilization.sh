if [ -z "$1" ]; then
  echo "Please provide output folder path as a command line argument"
  exit 1
fi

HOSTNAME=$(hostname)
OUTPUT_DIR=$1
OUTPUT_FILE="$OUTPUT_DIR/cpu_usage_output_${HOSTNAME}_$(date +'%Y%m%d_%H%M%S').txt"
mkdir -p "$OUTPUT_DIR"

# output cpu util every 15 seconds until 8 minutes
sar -u 15 42 > "$OUTPUT_FILE"

echo "CPU UTILIZATION OUTPUT SAVED TO: $OUTPUT_FILE"