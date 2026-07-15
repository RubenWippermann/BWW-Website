#!/bin/zsh
cd "$(dirname "$0")"
git remote set-url origin https://github.com/RubenWippermann/BWW-Website.git 2>/dev/null || git remote add origin https://github.com/RubenWippermann/BWW-Website.git
git branch -M main
git push -u origin main
echo
echo "Fertig. Du kannst dieses Fenster schließen."
read -k 1 "?Taste drücken zum Schließen ..."
