import elftools.elf.elffile as ELF

def parse_elf(elf_binary):

    """
    Function to parse ELF file of the ARMv8 architecture and obtain corresponding section data.

    Input
    -----
    ELF Binary of the ARMv8 architecture passed as parameter.

    Output
    ------
    Corresponding section data of the ELF Binary.

    Return type: Object of sections class
    """

    file_stream = open(elf_binary, "rb")
    elf_object = ELF.ELFFile(file_stream)
    text_section_object = elf_object.get_section_by_name(".text")
    data = text_section_object.data()
    file_stream.close()
    return data

def is_Little_Endian(elf_binary):

    """
    Function to specify whether the ELF binary input is encoded in Little Endian manner or Big Endian Manner

    Input
    -----
    ELF Binary of the ARMv8 architecture passed as parameter.

    Output
    ------
    Corresponding architecture encoding for the ELF binary.

    Return type: bool

    For Little Endian: Return True
    For Big Endian: Return False
    """

    file_stream = open(elf_binary, "rb")
    elf_object = ELF.ELFFile(file_stream)
    return elf_object.little_endian
