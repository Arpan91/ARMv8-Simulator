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

    def f_adder(a, b, c):

       if a=='0':
           if b == '0':
               if c == '0':
                   return '0', '0'
               else:
                   return '1', '0'

           else:
               if c == '0':
                   return '1', '0'
               else:
                   return '0', '1'

        else:
           if b == '0':
               if c == '0':
                   return '1', '0'
               else:
                   return '0', '1'

           else:
               if c == '0':
                   return '0', '1'
               else:
                   return '1', '1'

    def bin_add(reg1, reg2, mode):

        aux = ['0']*65
        res = ['0']*64

        if mode == 0:
            for i in range(1:33):
                res[-i], aux[-(i+1)] = f_adder(reg1[-i], reg2[-i], aux[-i])
            res = ''.join(res)
            if aux[-33] == '1':
                return res, 1
            else:
                return res, 0

        else:
            for i in range(1:65):
                res[-i], aux[-(i+1)] = f_adder(reg1[-i], reg2[-i], aux[-i])
            res = ''.join(res)
            if aux[-65] == '1':
                return res, 1
            else:
                return res, 0
        
    def f_subtractor(a, b, c):

       if a=='0':
           if b == '0':
               if c == '0':
                   return '0', '0'
               else:
                   return '1', '1'

           else:
               if c == '0':
                   return '1', '1'
               else:
                   return '0', '1'

        else:
           if b == '0':
               if c == '0':
                   return '1', '0'
               else:
                   return '0', '0'

           else:
               if c == '0':
                   return '0', '0'
               else:
                   return '1', '1'

    def bin_sub(reg1, reg2, mode):

        aux = ['0']*65
        res = ['0']*64

        if mode == 0:
            for i in range(1:33):
                res[-i], aux[-(i+1)] = f_subtractor(reg1[-i], reg2[-i], aux[-i])
            res = ''.join(res)
            if aux[-33] == '1':
                return res, 1
            else:
                return res, 0

        else:
            for i in range(1:65):
                res[-i], aux[-(i+1)] = f_subtractor(reg1[-i], reg2[-i], aux[-i])
            res = ''.join(res)
            if aux[-65] == '1':
                return res, 1
            else:
                return res, 0
    
    def add_immediate_32(inst):

        """
        Addition(ADD) routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:32] + imm_temp[44:] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_add(imm, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

    def add_immediate_64(inst):

        """
        Addition(ADD) routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:12] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_add(imm, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

    def adds_immediate_32(inst):

        """
        Addition(ADDS) routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:32] + imm_temp[44:] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_add(imm, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-32] == '1':
            self.flags[N] == True

        if self.gp_registers[rn][-32] == imm[-32]:
            if res[-32] != imm[-32]:
                self.flags[V] = True

    def adds_immediate_64(inst):

        """
        Addition(ADDS) routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:12] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_add(imm, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-64] == '1':
            self.flags[N] == True
        if self.gp_registers[rn][-64] == imm[-64]:
            if res[-64] != imm[-64]:
                self.flags[V] = True

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
            rm_new = ('0'*32) + self.gp_registers[rm][(32+amount-1):] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*32) + ('0'*amount) + self.gp_registers[rm][32:-amount]
        elif shift == '10':
            rm_new = ('0'*32) + (self.gp_registers[rm][32]*amount + self.gp_registers[rm][32:-amount]

        res, carry = bin_add(rm_new, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

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
            rm_new = self.gp_registers[rm][amount-1:] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*amount) + self.gp_registers[rm][:-amount]
        elif shift == '10':
            rm_new = (self.gp_registers[rm][0]*amount + self.gp_registers[rm][:-amount]

        res, carry = bin_add(rm_new, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

    def adds_shift_register_32(inst):

        """
        Addition(ADDS) routine for shift register addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = ('0'*32) + self.gp_registers[rm][(32+amount-1):] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*32) + ('0'*amount) + self.gp_registers[rm][32:-amount]
        elif shift == '10':
            rm_new = ('0'*32) + (self.gp_registers[rm][32]*amount + self.gp_registers[rm][32:-amount]

        res, carry = bin_add(rm_new, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-32] == '1':
            self.flags[N] == True
        if self.gp_registers[rn][-32] == rm_new[-32]:
            if res[-32] != rm_new[-32]:
                self.flags[V] = True

    def adds_shift_register_64(inst):

        """
        Addition(ADD) routine for shift register addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = self.gp_registers[rm][amount-1:] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*amount) + self.gp_registers[rm][:-amount]
        elif shift == '10':
            rm_new = (self.gp_registers[rm][0]*amount + self.gp_registers[rm][:-amount]

        res, carry = bin_add(rm_new, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-64] == '1':
            self.flags[N] == True
        if self.gp_registers[rn][-64] == imm[-64]:
            if res[-64] != imm[-64]:
                self.flags[V] = True

        def sub_immediate_32(inst):

        """
        Subtraction(SUB) routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:32] + imm_temp[44:] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_sub(imm, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

    def sub_immediate_64(inst):

        """
        Subtraction(SUB) routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:12] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_sub(imm, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

    def subs_immediate_32(inst):

        """
        Subtraction(SUBS) routine for immediate addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:32] + imm_temp[44:] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_sub(imm, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-32] == '1':
            self.flags[N] == True

        if self.gp_registers[rn][-32] == imm[-32]:
            if res[-32] != imm[-32]:
                self.flags[V] = True

    def subs_immediate_64(inst):

        """
        Subtraction(SUBS) routine for immediate addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        shift = inst[-23:-21]
        imm_temp = '0'*52 + inst[10:22]
        if shift == '01':
            imm = (imm_temp[:12] + '0'*12)
        else:
            imm = imm_temp
        res, carry = bin_sub(imm, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-64] == '1':
            self.flags[N] == True
        if self.gp_registers[rn][-64] == imm[-64]:
            if res[-64] != imm[-64]:
                self.flags[V] = True

    def sub_shift_register_32(inst):

        """
        Subtraction(SUB) routine for shift register addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = ('0'*32) + self.gp_registers[rm][(32+amount-1):] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*32) + ('0'*amount) + self.gp_registers[rm][32:-amount]
        elif shift == '10':
            rm_new = ('0'*32) + (self.gp_registers[rm][32]*amount + self.gp_registers[rm][32:-amount]

        res, carry = bin_sub(rm_new, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

    def sub_shift_register_64(inst):

        """
        Subtraction(SUB) routine for shift register addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = self.gp_registers[rm][amount-1:] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*amount) + self.gp_registers[rm][:-amount]
        elif shift == '10':
            rm_new = (self.gp_registers[rm][0]*amount + self.gp_registers[rm][:-amount]

        res, carry = bin_sub(rm_new, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

    def subs_shift_register_32(inst):

        """
        Subtraction(SUBS) routine for shift register addressing mode(32 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = ('0'*32) + self.gp_registers[rm][(32+amount-1):] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*32) + ('0'*amount) + self.gp_registers[rm][32:-amount]
        elif shift == '10':
            rm_new = ('0'*32) + (self.gp_registers[rm][32]*amount + self.gp_registers[rm][32:-amount]

        res, carry = bin_sub(rm_new, self.gp_registers[rn], 0)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-32] == '1':
            self.flags[N] == True
        if self.gp_registers[rn][-32] == rm_new[-32]:
            if res[-32] != rm_new[-32]:
                self.flags[V] = True

    def subs_shift_register_64(inst):

        """
        Subtraction(SUBS) routine for shift register addressing mode(64 bit mode).
        """

        rd = int(inst[27:], 2)
        rn = int(inst[-10:-5], 2)
        amount = int(inst[-16:-10], 2)
        rm = int(inst[-21:-16], 2)
        shift = inst[-24:-22]

        if shift == '00':
            rm_new = self.gp_registers[rm][amount-1:] + ('0'*amount)
        elif shift == '01':
            rm_new = ('0'*amount) + self.gp_registers[rm][:-amount]
        elif shift == '10':
            rm_new = (self.gp_registers[rm][0]*amount + self.gp_registers[rm][:-amount]

        res, carry = bin_sub(rm_new, self.gp_registers[rn], 1)
        self.gp_rgisters[rd] = res

        if int(res, 2) == 0:
            self.flags[Z] == True
        if carry == 1:
            self.flags[C] == True
        if res[-64] == '1':
            self.flags[N] == True
        if self.gp_registers[rn][-64] == imm[-64]:
            if res[-64] != imm[-64]:
                self.flags[V] = True
