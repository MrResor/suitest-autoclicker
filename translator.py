from collections import deque
from sys import platform
import json

import numpy as np
from tqdm import tqdm

from parser import parser

class Translator():
    """ Class that translates string input to list of instructions for remote that need to be clicked to type
        in that string on designated device.\n

        Attributes:\n
        _args                           -- dictionary with arguments parsed by argparse.\n
        _format                         -- format of tqdm bar.\n
        _keyboard                       -- disctionary holding keyboard layouts and additional informations
        needed by a program to run the BFS calculations.\n
        _text                           -- string given by the user, the same variable is used to perform all
        the necessary transformations.\n
        _commands                       -- string created using the list of commands that need to be used in
        order to input the string on the deivce, it is either printed to console or coppied into clipboard
        and it has to be coppied into test in suite.st.\n

        Methods:\n
        _read_keyboard_setup            -- reads respecitve keyboard file and parses it into dictionary to
        be used by other functions of this program.\n
        _input_prep                     -- converts string to symbols that can be found on the keybord ([A]
        is changed into [SHIFT, a], any special symbols are prefixed with SPECIAL symbol).\n
        run                             -- runs the main algorithm of the program using the previously
        prepaired text input and producing the final output of the program.\n
        _prep_commands                  -- 
        _bfs                            -- implementation of Breadth First Search algorithm, finds the
        shortest path between two nodes in the graph.\n
        _to_clipboard                   -- coppies result to clipboard or prints it to the console based on
        the system the program was used on.\n
        _handle_win_and_linux_output    -- handles the printing of the result on windows and linux platforms.
    """

    def __init__(self) -> None:
        """ Sets up translator and constants that are used later on. Calls for initial parsing of the input
            string.
        """
        self._args = parser.parse_args()
        self._format = "{desc:<25}: {percentage:3.0f}%|{bar:100}{r_bar}{bar:-10b}"
        self._read_keyboard_setup()
        self._input_prep()

    def _read_keyboard_setup(self) -> None:
        """ Read keyboard .json file and parse it into JSON / dictionary.
        """
        with open("keyboards/" + self._args.platform + ".json") as f:
            self._keyboard = json.loads("".join(f.readlines()))

    def _input_prep(self) -> None:
        """ Parses the input string based on the keyboard type so it can be typed in using given keyboard.
            For example, for keyboards of type 1 and 2 any capital letter needs to be changed into normal
            letter with SHIFT preeceding it or with CAPS encasing it.
        """
        text = list(self._args.string)
        if self._keyboard['type'] > 0:
            flag = False
            inverse = reversed(list(enumerate(text)))
            iter = tqdm(list(inverse), desc="Processing input", bar_format=self._format)
            # passes are done from end to start to make indexing and insterting  easier
            # first pass, for capital letters
            for i, v in iter:
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
            if flag:
                text.insert(0, "CAPS")
            flag = False
            inverse = reversed(list(enumerate(text)))
            iter = tqdm(list(inverse), desc="Processing input", bar_format=self._format)
            # second pass, for special characters
            for i, v in iter:
                if v in self._keyboard['special'] and not flag:
                    text.insert(i+1, "SPECIAL")
                    flag = True
                    continue
                if v not in self._keyboard['special'] and flag:
                    text.insert(i+1, "SPECIAL")
                    flag = False
            if flag:
                text.insert(0, "SPECIAL")
        self._text = text

    def run(self) -> None:
        """ Prepaires the commands to be used by suitest and puts them into clipboard.
        """
        self._prep_commands()
        self._to_clipboard()

    def _prep_commands(self) -> None:
        """ Prepaires the commands that should be send to suitest to type in given string. It paires the
            letters in the string (for example 'ABC' is converted into pairs 'AB' and 'BC') and then finds
            the shortest paths using BFS which then is translated to remote clicks.
        """
        text = self._text
        path = [(self._keyboard['begin'], text[0])] + list(zip(text, np.roll(text, -1)))[:-1]
        commands = []
        commands.append(f'{{"type":"comment","excluded":false,"fatal":false,"screenshot":false,"val":"{self._args.platform}"}}')
        commands.append(f'{{"type":"comment","excluded":false,"fatal":false,"screenshot":false,"val":"{self._args.string}"}}')
        commands.append(f'{{"type":"comment","excluded":false,"fatal":false,"screenshot":false,"val":"----------"}}')
        special = False
        for i in tqdm(path, desc="Generating key sequence", bar_format=self._format):
            commands.append(f'{{"type":"comment","excluded":false,"fatal":false,"screenshot":false,"val":"{i[1]}"}}')
            path_order = []
            key = 'arcs' if special else 'edges'
            path = self._bfs(self._keyboard[key], i[0], i[1])
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

    def _bfs(self, graph:dict, S:str, D:str) -> None:
        """ Implementation of Breadth First Search algorithm for finding shortest path in the graph. Takes
            in graph description, starting and destination nodes as parameters and returns a list of nodes
            that needs to be visited in given order to reach destination node from the starting node.
        """

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

    def _to_clipboard(self) -> None:
        """ Copies prepared instructions to clipboard, and if copying is not possible it will call a function
            that handles that.
        """
        if platform == "linux" or platform == "linux2":
            self._handle_win_and_linux_output()
        elif platform == "darwin":
            import subprocess 
            subprocess.run("pbcopy", text=True, input=self._commands)
            print("Coppied to clibpoard.")
        elif platform == "win32":
            self._handle_win_and_linux_output()
    
    def _handle_win_and_linux_output(self) -> None:
        """ Informs that copying to clipboard is not possible and prints to console.
        """
        print("Platform not supported for copying to clipboard, please copy manualy from below:")
        print(self._commands)
        