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
        Addition(ADD) routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        res = bin(int(('0'*20 + inst[10:22]), 2) + int(self.gp_registers[rn[-31:]], 2))[2:]

        if len(res) > 32:
            self.gp_registers[rd] = self.gp_registers[rd][:32]+ res[-32:]
        elif len(res) < 32:
            self.gp_registers[rd] = self.gp_registers[rd][:32] + '0'*(32-len(res)) + res
        else
            self.gp_registers[rd] = self.gp_registers[rd][:32] + res


    def add_immediate_64(inst):

        """
        Addition(ADD) routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        res = bin(int(('0'*52 + inst[10:22]), 2) + int(self.gp_registers[rn], 2))[2:]
        if len(res) > 64:
            self.gp_registers[rd] = res[-64:]
        elif len(res) < 64:
            self.gp_registers[rd] = '0'*(64-len(res)) + res
        else
            self.gp_registers[rd] = res

    def adds_immediate_32(inst):

        """
        Addition(ADDS) routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        a, b = int(('0'*20 + inst[10:22]), 2), int(self.gp_registers[rn][-31:], 2)
        res = bin(a+b)[2:]
        
        if int(res, 2) == 0:
            self.flags[Z] = True
        if len(res) > 32:
            self.flags[V] = True
            self.gp_registers[rd] = self.gp_registers[rd][:32] + res[-32:]
        elif len(res) < 32:
            self.gp_registers[rd] = self.gp_registers[rd][:32] + '0'*(32-len(res)) + res
        else
            self.gp_registers[rd] = self.gp_registers[rd][:32] + res
        if self.gp_registers[rd][0] == '1':
            self.flags[N] = True


    def adds_immediate_64(inst):

        """
        Addition(ADDS) routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        res = bin(int(('0'*52 + inst[10:22]), 2) + int(self.gp_registers[rn], 2))[2:]
        if res == 0:
            self.flags[Z] = True
        if len(res) > 64:
            self.flags[V] = True
            self.gp_registers[rd] = res[-64:]
        elif len(res) < 64:
            self.gp_registers[rd] = '0'*(64-len(res)) + res
        else
            self.gp_registers[rd] = res
        if self.gp_registers[rd][0] == '1':
            self.flags[N] = True

    def add_shift_register_32(inst):

        """
        Addition(ADD) routine for shift register addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = ('0'*32) + self.gp_registers[rm][(32+amount):] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*32) + ('0'*amount) + self.gp_registers[rm][32:-amount]
        elif shift == '10':
            rm_new = ('0'*32) + (self.gp_registers[rm][32]*amount + self.gp_registers[rm][32:-amount]

        rm = int(rm_new, 2)
        res = bin(rm + int(self.gp_registers[rn][-32:], 2))[2:]
        
        if len(res) > 32:
            self.gp_registers[rd] = self.gp_registers[rd][:32]+ res[-32:]
        elif len(res) < 32:
            self.gp_registers[rd] = self.gp_registers[rd][:32] + '0'*(32-len(res)) + res
        else
            self.gp_registers[rd] = self.gp_registers[rd][:32] + res

    def add_shift_register_64(inst):

        """
        Addition(ADD) routine for shift register addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = self.gp_registers[rm][amount:] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*amount) + self.gp_registers[rm][:-amount]
        elif shift == '10':
            rm_new = (self.gp_registers[rm][0]*amount + self.gp_registers[rm][:-amount]

        rm = int(rm_new, 2)
        res = bin(rm + int(self.gp_registers[rn], 2))[2:]
        
        if len(res) > 64:
            self.gp_registers[rd] = res[-64:]
        elif len(res) < 64:
            self.gp_registers[rd] = '0'*(64-len(res)) + res
        else
            self.gp_registers[rd] = res

