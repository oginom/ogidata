import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../helper"))

import push

if __name__ == "__main__":
    print(push.push("sample_project", "debug", "sample message", img_path="runrun.png"))
