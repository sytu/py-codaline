#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import argparse


def getLinesNumStr(file):
    cmd_single = 'sloccount {0} | grep "Lines" | cut -c61-'.format(file)
    strArr = os.popen(cmd_single).read().split('\n')
    return strArr[0]


# def Print(result, repeat=False):
#     if repeat == False:
#         print("---Codaline---\n\n" + result)
#     else:
#         print(result)


def saveLines(file, env_name, outfile):
    lines = getLinesNumStr(file)
    outfile.write("export {0}={1};\n".format(env_name, lines))
    result = """Target: {0}

Saved the number of lines of code: < {1} > to environ[{2}]. 

Tip: Then source and use --diff to count the lines of code you have added.
    """.format(os.path.join(os.getcwd(), file), lines, env_name)
    print(result)
    # os.popen('source '+ os.path.expanduser("~/.zshrc"))


def countLines(file, env_name, outfile, last_lines):
    lines = getLinesNumStr(file)
    diff = int(lines) - int(last_lines)
    result = "Target: {0}\n\n".format(os.path.join(os.getcwd(), file)) + \
    ("You haven't added any line of code yet.\n" if diff == 0 else "Lines of code had been added: \t\t\t< {0} >\n".format(diff))
    print(result)


# delete the environ in zshrc
def reset(xxrc, lns, env_name):
    result = ''
    with open(xxrc,"w",encoding="utf-8") as outfile_w:
        for line in lns:
            if env_name in line:
                result = 'Found line contains environ:[{0}] and delete successfully.\n'.format(env_name)
                print(result)
                continue
            outfile_w.write(line)
    if result == '':
        print('Not found environ:[{0}]. \nCleaning process failed.\n'.format(env_name))

def main():
    print("---Codaline---\n")

    env_name = os.getcwd().replace('-', '/').replace('/', '_')
    xxrc = os.path.expanduser("~/.zshrc")

    descStr = """
    This program counts the number of code you added into a directory or a file. 
    Usage: 
    1. --save .
    2. source ~/.xxrc
    3. programming
    4. --diff .
    """
    parser = argparse.ArgumentParser(description=descStr)
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--save', '-s', dest='pSaveLines', required=False)
    group.add_argument('--diff', '-d', dest='pCountDiffLines', required=False)
    # --clean不需要参数
    group.add_argument('--clean', '-c', action="store_true", default=False)

    args = parser.parse_args()
    # print(args)

    with open(xxrc, "a") as outfile_a:
        # save the num of lines to the environ
        if args.pSaveLines:
            saveLines(args.pSaveLines, env_name, outfile_a)
        # count the lines
        elif args.pCountDiffLines:
            try: 
                last_lines = int(os.environ[env_name])
            except KeyError as e:
                # print('Not found environ: ', e)
                raise KeyError("Unfound environ: {0}. Please --save and source before --diff!".format(e))
            countLines(args.pCountDiffLines, env_name, outfile_a, last_lines)
        # clean up the environ
        # @now
        elif args.clean:
            with open(xxrc, "r") as outfile_r:
                lns = outfile_r.readlines()
            reset(xxrc, lns, env_name)
        else:
            print('Error Option.')


if __name__ == "__main__":
    main()
