import process_instructions as pi

class ARMv8(object):
    """
    Simulator for the ARMv8 architecture
    """

    def __init__(self, stream):
        self.instructions = pi.get_instructions(stream)
        self.gp_registers = [[0]*64 for i in range(31)]
        self.sp = [0]*64
        self.pc = [0]*64
        self.flags = {N: False, Z: False, C: False, V: False}
        self.exception_mask = {D: False, A: False, I: False, F: False}

