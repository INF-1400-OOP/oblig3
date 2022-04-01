#!/usr/bin/env python3

from argparse import ArgumentParser
from server import Server
from main import Main
from _thread import start_new_thread, allocate_lock

def get_args():

    parser = ArgumentParser(description="Run Mayhem clone game as eiter a server or connecting client.")

    parser.add_argument("-s", "--server", action="store_true", help="Run Mayhem clone as a server.")

    parser.add_argument("-c", "--client", action="store_true", help="Run Mayhem clone as a client.")

    parser.add_argument("-p", "--port", metavar="PORT", type=int, action="append", help="Port to run or connect to Mayhem clone server on.")

    parser.add_argument("-a", "--address", metavar="ADDRESS", type=str, action="append", help="Address to run or connect to Mayhem clone server on.")

    args = parser.parse_args()

    return (args.server, args.client, args.port, args.address)

def run_server(port:int, addr:str):
    
    server = Server(addr, port, Main.spawn_player)

    start_new_thread(server.start_server, ())

    game = Main(port, addr, 2048*64)

    while True:
        game.new()
        game.run()


# def server_runner():
#     server = Server(addr, port)
#     server.start_server()

def run_client(port:int, addr:str):

    game = Main(port, addr, 2048*64)
    while True:
        game.new()
        game.run()


if __name__ == '__main__':
    server, client, port, addr = get_args()

    port = port[0] if port else None
    addr = addr[0] if addr else None

    if server:
        print("Running Mayhem clone as a server.")
    elif client:
        print("Running Mayhem clone as a client.")
    else:
        print("No arguments given. Running Mayhem clone as a server.")
        server = True

    print("Port    : " + str(port))
    print("Address : " + str(addr))

    # print(port, type(port), addr, type(addr))

    # exit()

    if server:
        print("Running Mayhem clone as a server.")
        run_server(port, addr)
    elif client:
        print("Running Mayhem clone as a client.")
        run_client(port, addr)
    else:
        print("No arguments given. Running Mayhem clone as a server.")
        run_server(port, addr)