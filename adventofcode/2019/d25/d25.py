import os
import sys
from collections import defaultdict, deque

with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    program = [int(x) for x in f.read().split(",")]


class VM:
    def __init__(self, program):
        self.pointer = 0
        self.program = defaultdict(int, enumerate(program))
        self.input = []
        self.output = []
        self.done = False
        self.base = 0

        self.op_params = {
            1: 3, 2: 3, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 1
        }

    def add_input(self, input):
        self.input.append(input)
        self.run()

    def run(self):
        while True:
            opcode = self.program[self.pointer]
            code = opcode % 100
            if code == 99:
                self.done = True
                return
            if code == 3 and len(self.input) == 0:
                return

            num_params = self.op_params[code]
            modes = [(opcode // 10**i) %
                     10 for i in range(2, 2+num_params)]
            args = [self.program[self.pointer+x]
                    for x in range(1, 1+num_params)]
            reads = [(self.program[a], a, self.program[a+self.base])[m]
                     for a, m in zip(args, modes)]
            writes = [(a, None, a+self.base)[m]
                      for a, m in zip(args, modes)]

            self.pointer += num_params + 1
            if code == 1:
                self.program[writes[2]] = reads[0] + reads[1]
            elif code == 2:
                self.program[writes[2]] = reads[0] * reads[1]
            elif code == 3:
                self.program[writes[0]] = self.input.pop(0)
            elif code == 4:
                self.output.append(reads[0])
            elif code == 5:
                if reads[0] != 0:
                    self.pointer = reads[1]
            elif code == 6:
                if reads[0] == 0:
                    self.pointer = reads[1]
            elif code == 7:
                self.program[writes[2]] = int(reads[0] < reads[1])
            elif code == 8:
                self.program[writes[2]] = int(reads[0] == reads[1])
            elif code == 9:
                self.base += reads[0]


vm = VM(program)
vm.run()

cmds = [
    "south",
    "take whirled peas",
    "south",
    "south",
    "south",
    "take festive hat",
    "north",
    "north",
    "north",
    "north",
    "west",
    "take pointer",
    "east",
    "north",
    "take coin",
    "north",
    "take astronaut ice cream",
    "north",
    "west",
    "take dark matter",
    "south",
    "take klein bottle",
    "west",
    "take mutex",
    "west",
    "south",
]

items = ['mutex', 'dark matter', 'astronaut ice cream',
         'festive hat', 'whirled peas', 'coin', 'klein bottle', 'pointer']

for cmd in cmds:
    for ch in cmd:
        vm.add_input(ord(ch))
    vm.add_input(10)

# items
for item in items:
    for ch in f"drop {item}\n":
        vm.add_input(ord(ch))

for a in range(2**len(items)):
    iset = set()
    for i in range(len(items)):
        if ((a >> i) & 1) == 1:
            iset.add(items[i])
    for item in iset:
        for ch in f"take {item}\n":
            vm.add_input(ord(ch))
    for ch in f"east\n":
        vm.add_input(ord(ch))
    for item in iset:
        for ch in f"drop {item}\n":
            vm.add_input(ord(ch))

out = vm.output
vm.output = []
for ch in out:
    print(chr(ch), end='')