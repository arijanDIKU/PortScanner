import argparse
import queue
from colorama import Fore, Back, Style
import threading
import socket
import time


q = queue.Queue()
print_lock = threading.Lock()


def port_scan(port):
    global targethost
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((targethost, port))
        with print_lock:
            try: 
                protocol = socket.getservbyport(port)
                print(f'{Fore.GREEN}{port} Open {protocol}')
            except:
                print(f'{Fore.GREEN}{port} Open Unknown')
        s.close()
    except:
        with print_lock:
            print(f'{Fore.RED}{port} Closed')


def threader():
    global q
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()



def scan_ports(ports, threads):
    global q
    for t in range(threads):
        t = threading.Thread(target=threader, daemon=True)
        t.start()

    for worker in ports:
        q.put(worker)
    q.join()


parser = argparse.ArgumentParser(description="Port scanner")
parser.add_argument("targethost", help="Host to scan")
parser.add_argument("--ports", "-p", default="1-65535", help="Range of ports to scan")
parser.add_argument("--threads", type=int, default=150, help="set number of threads")
parser.add_argument("--time", help="record time taken", action="store_true")
args = parser.parse_args()
targethost, port_range, threads = args.targethost, args.ports, args.threads

port_begin, port_end = port_range.split('-')
port_begin, port_end = int(port_begin), int(port_end)
ports = [p for p in range(port_begin, port_end+1)]
print(ports[0], ports[-1])


print("Port Status Protocol")
start = time.time()
scan_ports(ports, threads)


if args.time:
    print(f"Time passed : {(time.time()-start) / 1000}ms") 
