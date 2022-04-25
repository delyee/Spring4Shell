'''
$ masscan 10.0.0.0/8 -Pn -p80,443,8080,8000,5000 --open-only --output-format list --output-filename mda.txt --rate 70000
...

#masscan
open tcp 8080 10.1.1.2 1650872280
open tcp 80 10.1.1.3 1650872280
'''

from sys import argv

if len(argv) < 2:
    print("python3 masscan_list_converter.py masscan_list_output.txt")
    exit()


with open(argv[1]) as f:
    urls = []
    for line in f.readlines():
        _ = line.split()
        if len(_) != 5:
            continue
        urls.append(f"http://{_[3]}:{_[2]}\n")


with open("urls.txt", "w") as f:
    f.writelines(urls)