#!/bin/bash

# Define the current directory as the source directory (the folder where the script is being executed)
SOURCE_DIR="$(pwd)"

# Check if the current directory contains any folders
if [ ! "$(ls -A "$SOURCE_DIR")" ]; then
  echo "Error: Source directory '$SOURCE_DIR' is empty."
  exit 1
fi

# Loop through all subdirectories in the current directory (dotfiles folder)
for folder in "$SOURCE_DIR"/*/; do
  # Check if it is a directory
  if [ -d "$folder" ]; then
    # Get the directory name (basename removes the path)
    folder_name=$(basename "$folder")

    # Check if the symlink already exists and points to the correct directory
    if [ -L "$HOME/.config/$folder_name" ] && [ "$(readlink "$HOME/.config/$folder_name")" == "$SOURCE_DIR/$folder_name" ]; then
      echo "Symlink for '$folder_name' already exists and is correct. Skipping."
    else
      # Remove existing symlink if it exists and create a new one
      rm -rf "$HOME/.config/$folder_name"
      ln -sf "$SOURCE_DIR/$folder_name" "$HOME/.config/$folder_name"
      echo "Symlinked '$folder_name' to ~/.config/$folder_name"
    fi
  else
    echo "'$folder' is not a directory. Skipping."
  fi
done
