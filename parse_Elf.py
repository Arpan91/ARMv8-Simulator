import elftools.elf.elffile as ELF
import sys

def parse_elf(elf_binary):

    """
    Function to parse ELF file of the ARMv8 architecture and obtain corresponding section data.

    Input
    -----
    ELF Binary of the ARMv8 architecture as parameter.

    Output
    ------
    Corresponding section data of the ELF Binary.
    """

    file_stream = open(elf_binary, "rb")
    elf_object = ELF.ELFFile(file_stream)
    text_section_object = elf_object.get_section_by_name(".text")
    data = text_section_object.data()
    return data
