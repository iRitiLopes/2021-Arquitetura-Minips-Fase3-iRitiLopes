from minips.cache.policy.random_access import RandomAccess
from minips.cache.mapping.direct import DirectMapping
from minips.word import Word
from minips.cache.controller import CacheController

class L1ICache:
    def __init__(self, size=512, line_size=32, mode=DirectMapping(), policy=RandomAccess()) -> None:
        super().__init__(size=size)
        self.mode = mode
        self.policy = policy
        self.size = size
        self.line_size = line_size
        self.num_blocks = self.size // self.line_size
        self.cache = {x: Word("".zfill(32)) for x in range(self.num_blocks)}
        self.cache_control = {x: CacheController() for x in range(self.num_blocks)}
    
    def hit(self, address):
        pass
    
    def load(self, address):
        block = self.block_index(address)
        if not self.cache_control[block].compare_tag(address):
            raise Exception("Invalid")
        return self.cache[block]
    
    def store(self, address, data):
        block = self.block_index(address)
        self.cache_control[block].valid_this()
        self.cache_control[block].clean_this()
        self.cache_control[block].set_tag(address)
        self.cache[block] = Word(data)

    def block_index(self, address):
        return (address // (self.line_size // 8) % self.num_blocks)