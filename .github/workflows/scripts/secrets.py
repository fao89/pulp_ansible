import json
import os
import sys

secrets = json.loads(sys.argv[1])
with open("fao.json", "w") as fao:
    fao.write(sys.argv[1])
for key, value in secrets.items():
    if key != "AUTOMATION_HUB_TOKEN_AUTH":
        continue
    print(f"Setting {key} ...")
    lines = len(value.split("\n"))
    if lines > 1:
        print("MULTI")
        os.system(f"echo '{key}<<EOF' >> $GITHUB_ENV")
        os.system(f"echo '{value}' >> $GITHUB_ENV")
        os.system("echo 'EOF' >> $GITHUB_ENV")
    else:
        os.system(f"echo '{key}={value}' >> $GITHUB_ENV")
