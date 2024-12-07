#!/bin/bash

# Check if stash.py exists in the current directory
if [ ! -f "stash.py" ]; then
    echo "Error: stash.py not found in the current directory."
    exit 1
fi

# Step 1: Add a shebang if it doesn't exist
if ! head -n 1 stash.py | grep -q "^#!/usr/bin/env python3"; then
    echo "Adding shebang to stash.py..."
    sed -i '1i#!/usr/bin/env python3' stash.py
fi

# Step 2: Rename stash.py to stash (remove .py extension)
if [ -f "stash" ]; then
    echo "Removing old executable named 'stash'..."
    rm -f stash
fi
mv stash.py stash

# Step 3: Make it executable
chmod +x stash
echo "Made 'stash' executable."

# Step 4: Move to /usr/local/bin
echo "Moving 'stash' to /usr/local/bin (requires sudo)..."
sudo mv stash /usr/local/bin/stash

# Step 5: Verify installation
if [ -f "/usr/local/bin/stash" ]; then
    echo "Installation successful! You can now use 'stash' as a command."
    echo "Example usage:"
    echo "  stash init"
    echo "  stash update"
else
    echo "Error: Installation failed. Check your permissions or try again."
    exit 1
fi

# Step 6: Self-delete the script
echo "Deleting installation script..."
rm -- "$0"

echo "Done!"
