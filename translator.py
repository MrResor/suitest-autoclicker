from parser import parser
from collections import deque
import json
import numpy as np
from tqdm import tqdm

class translator():

    def __init__(self):
        self._args = parser.parse_args()
        self.read_keyboard_setup()
        self.input_prep()
        self.prep_commands()
        self.to_clipboard()

    def read_keyboard_setup(self):
        with open(self._args.platform + ".json") as f:
            keyboard = f.readlines()
        self._keyboard = json.loads(''.join(keyboard))

    def input_prep(self):
        text = list(self._args.string)
        if self._keyboard['type'] > 0:
            flag = False
            for i, v in reversed(list(enumerate(text))):
                if v.isupper() and not flag:
                    text[i] = v.lower()
                    for _ in range(self._keyboard['type']):
                        text.insert(i+1, "CAPS")
                    flag = True
                    continue
                if v.isupper() and flag:
                    text[i] = v.lower()
                    continue
                if not v.isupper() and flag:
                    for _ in range(self._keyboard['type']):
                        text.insert(i+1, "CAPS")
                    flag = False
            flag = False
            for i, v in reversed(list(enumerate(text))):
                if v in self._keyboard['special'] and not flag:
                    text.insert(i+1, "SPECIAL")
                    flag = True
                    continue
                if v not in self._keyboard['special'] and flag:
                    text.insert(i+1, "SPECIAL")
                    flag = False
        self.text = text

    def prep_commands(self):
        text = self.text
        path = [(self._keyboard['begin'], text[0])] + list(zip(text, np.roll(text, -1)))[:-1]
        commands = []
        special = False
        for i in tqdm(path):
            commands.append(f'{{"type":"comment","excluded":false,"fatal":false,"screenshot":false,"val":"{i[1]}"}}')
            path_order = []
            key = 'arcs' if special else 'edges'
            path = self.bfs(self._keyboard[key], i[0], i[1])
            for j in list(zip(path, np.roll(path, -1)))[:-1]:
                path_order.append(self._keyboard[key][j[0]][j[1]])
            if path_order:
                last = path_order[0]
                count = 1
                for j in path_order[1:]:
                    if last == j:
                        count += 1
                    else:
                        commands.append(f'{{"type":"button","excluded":false,"fatal":false,"screenshot":false,"count":{count},"delay":"<%del%>","ids":["{last}"]}}')
                        last = j
                        count = 1
                commands.append(f'{{"type":"button","excluded":false,"fatal":false,"screenshot":false,"count":{count},"delay":"<%del%>","ids":["{last}"]}}')
            commands.append(f'{{"type":"button","excluded":false,"fatal":false,"screenshot":false,"count":1,"delay":"<%del%>","ids":["ENTER"]}}')
            special = not special if i[1] == "SPECIAL" else special
                
        self._commands = '[' + ','.join(commands) + ']'

    def bfs(self, graph, S, D):

        visited = {}
        # Queue to store the nodes in the order they are visited
        q = deque()
        # Push the source node to the queue
        q.append(S)

        visited[S] = None

        # Iterate until the queue is not empty
        while q:
            # Pop the node at the front of the queue
            node = q.popleft()
            # Explore all the neighbors of the current node
            if node == D:
                path = []
                while node:
                    path.append(node)
                    node = visited[node]
                return path [::-1]

            for neighbour in graph[node]:
                # Check if the neighboring node is not visited
                if neighbour not in visited:
                    visited[neighbour] = node
                    q.append(neighbour)    

    def to_clipboard(self):
        from sys import platform
        if platform == "linux" or platform == "linux2":
            self.handle_win_and_linux_output()
        elif platform == "darwin":
            import subprocess 
            data = "hello world"
            subprocess.run("pbcopy", text=True, input=self._commands)
        elif platform == "win32":
            self.handle_win_and_linux_output()

        a = {1: self.read_keyboard_setup, 2: self.handle_win_and_linux_output}
        func = a[1]
        func()
    
    def handle_win_and_linux_output(self):
        print("platform not supported for copying to clipboard, please copy manualy from below:")
        print(self._commands)
        