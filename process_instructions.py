import parse_ELF

def get_instructions(elf_binary):

    """
    Function to fetch instructions from the contents of .text section of ELF binary

    Input
    -----

    Name of the ELF Binary of the ARMv8 architecture passed as parameter.

    Output
    ------

    String containing the instructions one after the other in the Big-Endian manner
    (MSB at the left)
    """

    data = parse_Elf.parse_elf(elf_binary)

    if (parse_Elf.is_Little_Endian(elf_binary):
        data = format_instruction(data)

    return data
