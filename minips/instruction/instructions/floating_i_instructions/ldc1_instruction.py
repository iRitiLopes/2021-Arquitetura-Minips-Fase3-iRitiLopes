from helpers.bin2float import Bin2Float
from helpers.bin2int import Bin2Int
from helpers.float2bin import Float2Bits
from helpers.int2bin import Int2Bits
from minips.coprocessor import COProcessor
from minips.instruction.instructions.floating_i_instructions import \
    Floating_I_BaseFunction
from minips.memory import Memory
from minips.registers import Registers
from helpers.int2hex import Int2Hex

class LDC1Instruction(Floating_I_BaseFunction):
    instruction_name = "LDC1"
    funct_code = '110101'

    def __init__(self, word) -> None:
        super().__init__(word)

    def decode(self, registers: Registers, coprocessor: COProcessor, *args, **kwargs) -> str:
        ft_name = coprocessor.registers.get_register_name(self.ft_number)
        rs_number = Bin2Int.convert(self.base)
        rs_name = registers.get_register_name(rs_number)
        offset = Bin2Int.convert(self.offset)

        return f"{self.instruction_name} {ft_name}, {offset}({rs_name})"

    def execute(self,
                registers: Registers,
                coprocessor: COProcessor,
                program_counter,
                memory: Memory,
                *args,
                **kwargs):
        local_co_registers = coprocessor.registers
        local_registers = registers

        rs_number = Bin2Int.convert(self.base)
        rs_register = local_registers.get_register(rs_number)
        rs_address = rs_register.to_unsigned_int()
        offset = Bin2Int.convert(self.offset)

        word1 = memory.load(rs_address + offset).data
        word2 = memory.load(rs_address + offset + 4).data

        kwargs['logger'].trace(f"R {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(rs_address + offset)})")
        kwargs['logger'].trace(f"R {Int2Hex.convert(program_counter)} (line# {Int2Hex.convert(rs_address + offset + 4)})")

        local_co_registers.set_register_value(self.ft_number, word1)
        local_co_registers.set_register_value(self.ft_number + 1, word2)

        return local_registers, program_counter + 4, memory, local_co_registers
