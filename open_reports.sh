#!/bin/bash

for file in reports/*.xlsx; do
    explorer.exe "$(wslpath -w "$file")"
done
