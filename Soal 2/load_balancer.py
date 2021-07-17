import os.path
from datetime import datetime
from urllib.parse import unquote
import re


class LoadBalancer:
    def __init__(self):
        self.server_list = []
        self.server_list.append(("localhost", 8000))
        # self.server_list.append(("localhost", 8001))
        # self.server_list.append(("localhost", 8002))
        # self.server_list.append(("localhost", 8003))
        # self.server_list.append(("localhost", 9004))
        self.counter = 0

    def get_server(self):
        server = self.server_list[self.counter]
        self.counter += 1
        if self.counter >= len(self.server_list):
            self.counter = 0
        return server


if __name__ == "__main__":
    load_balancer = LoadBalancer()
    for x in range(0, 100):
        y = load_balancer.get_server()
        print(y)
