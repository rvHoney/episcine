import sys
import actions

def main():
    if len(sys.argv) == 1:
        print('No action provided')
        sys.exit()

    action = sys.argv[1]
    if action == 'init':
        actions.init(sys.argv)
    elif action == 'push':
        actions.push(sys.argv)
    else:
        print('Invalid action')
        sys.exit()

if __name__ == '__main__':
    main()