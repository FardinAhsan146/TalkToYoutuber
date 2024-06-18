# This script helps me during development to just nuke the two databases and start from scratch 
# .\clean_databases.ps1

# Remove the chroma directory
Remove-Item -Recurse -Force .\chroma\

# Remove the talk_to_youtuber_db.sqlite file
cd database
rm talk_to_youtuber_db.sqlite