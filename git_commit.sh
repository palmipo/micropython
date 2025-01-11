find ./ -type f  -name "*.py" -exec git add {} \;
find ./ -type f  -name "*.json" -exec git add {} \;
git commit
git push
