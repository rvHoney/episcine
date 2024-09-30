import sys
import os
import json
import colorama

def init(args):
    if len(args) < 4:
        print(f'{colorama.Fore.RED}Invalid number of arguments{colorama.Style.RESET_ALL}')
        sys.exit()

    tag = args[2]

    if not tag.endswith('-*'):
        print(f'{colorama.Fore.RED}Invalid tag format (must end with -*){colorama.Style.RESET_ALL}')
        sys.exit()

    if os.path.exists('.episcine'):
        print(f'{colorama.Fore.RED}Episcine already initialized{colorama.Style.RESET_ALL}')
        sys.exit()

    print(f'{colorama.Fore.GREEN}Registering tag {tag}{colorama.Style.RESET_ALL}')

    print(f'{colorama.Fore.GREEN}Adding files...{colorama.Style.RESET_ALL}')
    files = []
    for i in range(3, len(args)):
        files.append(args[i])
        print(f'{colorama.Fore.GREEN}Added file {args[i]}{colorama.Style.RESET_ALL}')

    print(f'{colorama.Fore.GREEN}Creating .episcine file{colorama.Style.RESET_ALL}')

    with open('.episcine', 'w') as f:
        json.dump({
            'tag': tag,
            'files': files,
            'current_ver': 0
        }, f)

    print(f'{colorama.Fore.GREEN}Episcine initialized{colorama.Style.RESET_ALL}')

def push(args):
    if not os.path.exists('.episcine'):
        print(f'{colorama.Fore.RED}Episcine not initialized{colorama.Style.RESET_ALL}')
        sys.exit()

    if os.system('git rev-parse --is-inside-work-tree > /dev/null 2>&1') != 0:
        print(f'{colorama.Fore.RED}No Git repository found{colorama.Style.RESET_ALL}')
        sys.exit()

    with open('.episcine', 'r') as f:
        data = json.load(f)

    if 'tag' not in data or 'files' not in data or 'current_ver' not in data:
        print(f'{colorama.Fore.RED}Invalid .episcine file{colorama.Style.RESET_ALL}')
        sys.exit()

    tag = data['tag']
    files = data['files']
    current_ver = data['current_ver']

    if not tag.endswith('-*'):
        print(f'{colorama.Fore.RED}Invalid tag format (must end with -*){colorama.Style.RESET_ALL}')
        sys.exit()

    for file in files:
        if not os.path.exists(file):
            print(f'{colorama.Fore.RED}File {file} does not exist{colorama.Style.RESET_ALL}')
            sys.exit()

    if type(current_ver) != int and current_ver < 0:
        print(f'{colorama.Fore.RED}Invalid version{colorama.Style.RESET_ALL}')
        sys.exit()

    tag_to_push = tag.replace('*', str(current_ver))

    print(f'{colorama.Fore.GREEN}Pushing changes with tag {tag_to_push}{colorama.Style.RESET_ALL}')

    for file in files:
        os.system(f'git add {file}')

    if os.system('git diff-index --quiet HEAD --') == 0:
        print(f'{colorama.Fore.RED}No changes to push{colorama.Style.RESET_ALL}')
        sys.exit()
    os.system(f'git commit -m "{tag_to_push}"')
    

    os.system(f'git tag -a {tag_to_push} -m "{tag_to_push}"')
    os.system('git push --follow-tags')

    print(f'{colorama.Fore.GREEN}Changes pushed{colorama.Style.RESET_ALL}')

    data['current_ver'] += 1

    with open('.episcine', 'w') as f:
        json.dump(data, f)
        
