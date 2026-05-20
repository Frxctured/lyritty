import os
import sys

if len(sys.argv) >= 2:
    path = sys.argv[1]

    if os.path.exists(path):
        with open(path, "r+") as f:
            content = f.read()
            content = content.replace("<", "\n[").replace(">", "]").replace(" ", "")
            f.seek(0)
            f.write(content)
            f.truncate()
    else:
        print("Not a valid path")
else:
    print("You must provide a path")