from minips.memory import Memory
from time import time


class Mipstatics:
    def __init__(self) -> None:
        self.statistics = {
            'I': 0,
            'R': 0,
            'J': 0,
            'FR': 0,
            'FI': 0,
            'timelapse_0': 0,
            'timelapse_f': 0,
            "memory_access": 0,
            "l1i_access": 0,
            "l1d_access": 0,
            "l2_access": 0,
            "cycles": 0
        }

    def start(self):
        self.__set_statistic('timelapse_0', time())

    def finish(self):
        self.__set_statistic('timelapse_f', time())

    def __set_statistic(self, key, value):
        self.statistics[key] = value

    def increase_statistic(self, instruction):
        instruction_mapper = {
            0: 'I',
            1: 'R',
            2: 'J',
            3: 'FI',
            4: 'FR'
        }
        self.statistics[instruction_mapper[instruction.instruction_type]] += 1
        self.statistics["cycles"] += 1
    
    def memory_statistics(self, memory: Memory):
        cycles = 0
        memory_access = memory.access_count[3]
        cycles += memory_access * 100
        self.statistics["cycles"] += cycles
        self.statistics["memory_access"] += memory_access

    def show_statistics(self):
        print("\n------------------------------------------")
        print("Instruction count:")
        total = 0
        elapsed_time = self.statistics['timelapse_f'] - \
            self.statistics['timelapse_0']
        for instruction_type in ['R', 'I', 'J', 'FR', 'FI']:
            v = self.statistics[instruction_type]
            total += v
            print(f"{instruction_type}: {v}", end=' ')
        print(f"\nTotal: {total}")
        print(f"Simulation time: {elapsed_time} sec")
        print(f"Average IPS: {total/elapsed_time}")
        print("------------------------------------------\n")

        print(f"Cycles {self.statistics['cycles']}")
        print(f"Memory Access: {self.statistics['memory_access']} | Latency per access: 100")
        print(f"Cache L2 Access: {self.statistics['l2_access']} | Latency per access: 10")
        print(f"Cache L1D Access: {self.statistics['l1d_access']} | Latency per access: 1")
