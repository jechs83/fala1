#!/bin/bash



osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/juntoz/as.py 1"' "$2"
osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/juntoz/as.py 2"' "$2"
osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/juntoz/as.py 3"' "$2"



sleep 600

osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/juntoz/as.py 4"' "$2"
osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/juntoz/as.py 5"' "$2"
osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/juntoz/as.py 6"' "$2"




