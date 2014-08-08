import process_instructions as pi

class ARMv8(object):
    """
    Simulator for the ARMv8 architecture
    """

    def __init__(self, stream):
        self.instructions = pi.get_instructions(stream)
        self.gp_registers = ['0'*64 for i in range(31)]
        self.sp = ['0'*64]
        self.pc = ['0'*64]
        self.flags = {N: False, Z: False, C: False, V: False}
        self.exception_mask = {D: False, A: False, I: False, F: False}
        
    def add_immediate_32(inst):

        """
        Addition routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        res = bin(int(('0'*20 + inst[10:22]), 2) + int(self.gp_registers[rn[-31:]], 2))[2:]
        if len(res) > 32:
            self.flags[C] = True
            self.gp_registers[rd] = '0'*32 + res[-32:]
        elif len(res) < 32:
            self.gp_registers[rd] = '0'*32 + '0'*(32-len(res)) + res
        else
            self.gp_registers[rd] = '0'*32 + res


    def add_immediate_64(inst):

        """
        Addition routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        res = bin(int(('0'*52 + inst[10:22]), 2) + int(self.gp_registers[rn], 2))[2:]
        if len(res) > 64:
            self.flags[C] = True
            self.gp_registers[rd] = res[-64:]
        elif len(res) < 64:
            self.gp_registers[rd] = '0'*(64-len(res)) + res
        else
            self.gp_registers[rd] = res
