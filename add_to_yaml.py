import os
import time

import yaml
import os



os.popen('cd ~/git/metalink_static')
pasteboard = os.popen('pbpaste').read().replace("'","").replace("\n","").split('&t=')[0]

def add_to_yaml(URL=pasteboard):
    with open('video_list.yaml', 'r') as yamlfile:
        cur_yaml = yaml.safe_load(yamlfile)  # Note the safe_load
        cur_yaml['videos'].append(URL)

    if cur_yaml:
        with open('video_list.yaml', 'w') as yamlfile:
            yaml.safe_dump(cur_yaml, yamlfile)  # Also note the safe_dump

if __name__ == '__main__':
    add_to_yaml()