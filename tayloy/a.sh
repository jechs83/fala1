#!/bin/bash




if [ "$1" == "1" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/tayloy/as.py 0"'  "$2"

elif [ "$1" == "2" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/falabella/as.py 100"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/falabella/as.py 200"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/falabella/as.py 300"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/falabella/as.py 400"' "$2"

elif [ "$1" == "3" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 100"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 111"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 112"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 113"' "$2"


elif [ "$1" == "4" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 100"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 111"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 112"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 113"' "$2"


elif [ "$1" == "5" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 114"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 115"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/ripley/as.py 116"' "$2"

elif [ "$1" == "6" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/curacao/as.py 1"'  "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/curacao/as.py 2"'  "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/curacao/as.py 3"'  "$2" 
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/curacao/as.py 4"'  "$2"

elif [ "$1" == "7" ]; then
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/promart/as.py 1"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/promart/as.py 2"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/promart/as.py 3"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/promart/as.py 4"' "$2"
    osascript -e 'tell app "Terminal" to do script "python3 /Users/javier/GIT/fala/promart/as.py 5"' "$2"


else
  echo "Invalid argument: $1"
fi