#!/bin/bash

# Find all .py files and convert them to UTF-8 encoding
find . -type f -name "*.py" | while read -r file; do
    # Detect the current encoding of the file
    encoding=$(file -bi "$file" | sed -n 's/.*[ ]charset=\(.*\)$/\1/p')
    
    # If the encoding is not UTF-8, convert the file
    if [ "$encoding" != "utf-8" ]; then
        echo "Converting $file from $encoding to utf-8"
        iconv -f "$encoding" -t utf-8 "$file" -o "$file.utf8" && mv "$file.utf8" "$file"
    else
        echo "$file is already utf-8"
    fi
done