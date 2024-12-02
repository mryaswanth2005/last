#!/bin/bash

# This script will build your project for deployment

# Step 1: Clean up old build files (if any)
echo "Cleaning up old build files..."
rm -rf build/

# Step 2: Copy necessary files for the build
echo "Copying files to the build folder..."
mkdir build
cp -r * build/

# Step 3: Optionally, minify or optimize files if required
echo "Minifying JavaScript and CSS files..."
# You can add minification commands here if necessary
# For example: uglifyjs app.js -o build/app.min.js

# Step 4: Commit and push the changes to GitHub Pages branch
echo "Committing changes..."
git add .
git commit -m "Build and deploy to GitHub Pages"
git push origin gh-pages

echo "Build process completed successfully!"
