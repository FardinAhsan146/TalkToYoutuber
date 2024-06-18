# This script helps me during development to just nuke the two databases and start from scratch 

# Remove the chroma directory
Remove-Item -Recurse -Force .\chroma\

# Remove the talk_to_youtuber_db.sqlite file
Remove-Item -Force .\database_utils\talk_to_youtuber_db.sqlite