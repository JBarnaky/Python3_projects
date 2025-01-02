import subprocess
import datetime
import re
from concurrent.futures import ThreadPoolExecutor

import argparse

def write_result(filename, ping_results):
    with open(filename, "w") as f:
        f.write(f"Start time {datetime.datetime.now()}\n")
        for result in ping_results:
            f.write(result)
        f.write(f"\nEnd time {datetime.datetime.now()}")

def ping_address(address):
    try:
        output = subprocess.run(["ping", "-c", "1", address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return output.stdout
    except subprocess.CalledProcessError as e:
        return f"Failed to ping {address}: {e.stderr}"

def ping_subnet(subnet):
    with ThreadPoolExecutor(max_workers=16) as executor:
        addresses = [f"{subnet}.{i}" for i in range(1, 255)]
        results = list(executor.map(ping_address, addresses))
    return results

def main(subnet, filename):
    write_result(filename, ping_subnet(subnet))

def parse_arguments():
    parser = argparse.ArgumentParser(usage='%(prog)s [options] <subnet>',
                                     description='IP checker',
                                     epilog="python ipscanner.py 192.168.1 -f somefile.txt")
    parser.add_argument('subnet', type=str, help='The subnet you want to ping')
    parser.add_argument('-f', '--filename', type=str, help='The filename for output')
    
    args = parser.parse_args()

    if not re.match(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.0)", args.subnet):
        parser.error("This is not a valid subnet")

    if " " in args.filename:
        parser.error("There cannot be whitespaces in the filename")

    return args.subnet, args.filename

if __name__ == '__main__':
    main(*parse_arguments())
