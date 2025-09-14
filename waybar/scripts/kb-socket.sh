#!/bin/bash

# Function to get current layout
get_layout() {
    current_layout=$(hyprctl devices -j | jq -r '.keyboards[] | select(.name == "at-translated-set-2-keyboard") | .active_keymap')
    case "$current_layout" in
        *"English"* | *"US"*) echo '{"text": " US", "class": "us"}' ;;
        *"Swedish"* | *"SE"*) echo '{"text": " SE", "class": "se"}' ;;
        *) echo '{"text": " '$current_layout'", "class": "unknown"}' ;;
    esac
}

# Output initial state
get_layout

# Listen to Hyprland socket for events
socat -u UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock - | while read -r line; do
    # Listen for keyboard layout events
    if [[ $line == *"activelayout"* ]]; then
        get_layout
    fi
done
