import parse_Elf

def get_instructions(elf_binary):

    """
    Function to fetch instructions from the contents of .text section of ELF binary.

    Input
    -----

    Stream of the ELF Binary file of the ARMv8 architecture passed as parameter.

    Output
    ------

    String containing the instructions one after the other in the Big-Endian manner.
    (MSB at the left)
    """

    data = parse_Elf.parse_elf(elf_binary)

    data = ''.join(ch.encode('hex') for ch in data)

    if parse_Elf.is_Little_Endian(elf_binary):
        data = format_instruction(data)

    return data


def format_instruction(LE_instructions):

    """
    Function to format each Little-Endian 32-bit instructions to the Big-Endian manner.

    Input
    -----

    The Little Endian instruction in String format.

    Output
    ------

    The properly formatted instruction in String format.
    """

    instructions = [LE_instructions[i:i+8] for i in range(0, len(LE_instructions), 8)]
    BE_instructions = [i[6:8]+i[4:6]+i[2:4]+i[:2] for i in instructions]
    formatted_instruction = ''.join(BE_instructions)
    return formatted_instruction
