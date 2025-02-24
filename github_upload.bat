@echo off
echo Creating README.md...
echo # moonscrapesearch >> README.md

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Committing changes...
git commit -m "Initial commit - full codebase"

echo Renaming branch to main...
git branch -M main

echo Adding remote origin...
git remote add origin https://github.com/TheManiacalCoder/moonscrapesearch.git

echo Pushing to remote repository...
git push -u origin main

echo Done!
pause 