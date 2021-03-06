#!/usr/bin/env python3

import sys, getopt
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import multiprocessing as mp
from gcs.server import *
from utils.system_killer import Killer


def runServer(HOST, PORT, utm, input_parent_conn, output_child_conn, name, utmUpdate, verbose):
    queenB = Server(HOST, PORT, utm, input_parent_conn, output_child_conn, name, utmUpdate, verbose)
    queenB.listen()

def main():

    #store JWT into 'token'
    with open("mwalton.token", "r") as toke:
        token = toke.read()

    #Get the IP and Port of server from the localIP py file

    HOST = "192.168.254.11"
    PORT = 65432

    #These two pipes send data from the UI to the clientHandler server loop
    input_parent_conn, input_child_conn = mp.Pipe()
    output_parent_conn, output_child_conn = mp.Pipe()

    #create api interface with onesky
    utm = OneSkyAPI(token)

    kill = Killer()

    #instantiate the UI with the pipes
    ui = UI(input_child_conn, output_parent_conn, kill)
    #instantiate the server
    
    p_server = mp.Process(target= runServer, args=(HOST, PORT, utm, input_parent_conn, output_child_conn,  "castle", True, True))
    p_server.daemon = True
    p_server.start()

    ui.start()    
    p_server.join()    
    sys.exit(0)


if __name__=="__main__":

    main()

    
    

    