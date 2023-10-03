#!/bin/bash

# This file comments or uncomments based on the mode specificed and if the operation has already been performed
# bash comment.sh [boolean]

# -----

filePath="/etc/" # Replace with the path to your file
commenting=$1        # Set to true for adding mode, false for removing mode

# Start marker and end marker
startMarker="start"
endMarker="end"

#  ------

# Temporary file to store the modified content
tempFile=$(mktemp)
markerFound=false

while IFS= read -r line; do
  # Check if we found the start marker
  if [[ $line == *"$startMarker"* ]]; then
    markerFound=true
  fi

  # Check if we found the end marker
  if $markerFound && [[ $line == *"$endMarker"* ]]; then
    markerFound=false
  fi

  # Edit lines between the markers
  if $markerFound; then
    if $commenting && [[ "${line:0:1}" != "#" ]] && [[ $line != *"$startMarker"* ]]; then
      line="#$line"
    elif ! $commenting && [[ "${line:0:1}" == "#" ]] && [[ $line != *"$startMarker"* ]]; then
      line="${line:1}" # Remove the '#' character
    fi
  fi

  echo "$line" >> "$tempFile"
done < "$filePath"

# Replace the original file with the modified content
mv "$tempFile" "$filePath"

echo "Operation completed successfully."