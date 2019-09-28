from pwn import *
from collections import OrderedDict

# elf arch Error
class elfArchError(Exception):
    pass

class streamLenError(Exception):
    pass


class shellcodeLenError(Exception):
    pass

# global var context.arch Error
class contextArchError(Exception):
    pass

# function argument arror
class argError(Exception):
    pass

elf_fp=0
symbol_num = 0
symbol_dynsym_sz = 0
symbol_got_plt_sz = 0
symbol_rel_plt_sz = 0
offset = 1
arch = ''
symbol_dynsym_index_list = []
section_got_plt_addr = 0

def ret_list_base_len(string_stream, once_len):
    string_len = len(string_stream)
    circle_index = string_len/once_len
    try:
        if string_len % once_len != 0:
            raise streamLenError("\n\nError: string_len/once_len == 0\n\n")
    except streamLenError as except1:
        print(except1)
        quit()
    ret_list = []
    left_idx = 0
    for i in range(circle_index):
        ret_list.append(string_stream[left_idx:left_idx+once_len])
        left_idx += once_len
    return ret_list


def init_gloVar(fpath, arg_offset=1):
    global elf_fp
    global symbol_num
    global symbol_dynsym_sz
    global symbol_got_plt_sz
    global symbol_rel_plt_sz
    global arch
    global offset
    global section_got_plt_addr
    elf_fp = ELF(fpath)
    section_got_plt_addr = elf_fp.get_section_by_name(
        '.got.plt').header.sh_addr
    try:
        if elf_fp.arch == 'i386':
            symbol_dynsym_sz = 0x10
            symbol_got_plt_sz = 0x4
            symbol_rel_plt_sz = 0x8
            arch = 'i386'
        elif elf_fp.arch == 'amd64':
            symbol_dynsym_sz = 0x18
            symbol_got_plt_sz = 0x8
            symbol_rel_plt_sz = 0x18
            arch = 'amd64'
        else:
            raise elfArchError(
                '\n\nError: ELF arch neither i386 nor amd64\n\n')
    except elfArchError as except0:
        print(except0)
        quit()
    symbol_num = len((elf_fp.get_section_by_name('.plt').data()))/0x10-1
    offset = arg_offset % (symbol_num)


def ret_section_plt_got_plt_addr_dict():

    section_plt_obj = elf_fp.get_section_by_name('.plt')
    section_plt_addr = section_plt_obj.header.sh_addr
    symbol_plt_addr_list = []

    section_got_plt_obj = elf_fp.get_section_by_name('.got.plt')
    section_got_plt_addr = section_got_plt_obj.header.sh_addr
    symbol_got_plt_addr_list = []

    for i in range(symbol_num):
        symbol_plt_addr_list.append(section_plt_addr+(i+1)*0x10)
        symbol_got_plt_addr_list.append(
            section_got_plt_addr+(i+3)*symbol_got_plt_sz)
    return OrderedDict(zip(symbol_plt_addr_list, symbol_got_plt_addr_list))


def set_symbol_dynsym_index_list():
    global symbol_dynsym_index_list
    if arch == 'i386':
        section_rel_plt_obj = elf_fp.get_section_by_name('.rel.plt')
    else:
        section_rel_plt_obj = elf_fp.get_section_by_name('.rela.plt')

    section_rel_plt_addr = section_rel_plt_obj.header.sh_addr
    section_rel_plt_data = section_rel_plt_obj.data()
    symbol_rel_plt_list = ret_list_base_len(
        section_rel_plt_data, symbol_rel_plt_sz)

    if arch == 'i386':
        for i in range(symbol_num):
            symbol_dynsym_index = u32((symbol_rel_plt_list[i])[4:8]) >> 8
            symbol_dynsym_index_list.append(symbol_dynsym_index)
    else:
        for i in range(symbol_num):
            symbol_dynsym_index = u64((symbol_rel_plt_list[i])[8:16]) >> 32
            symbol_dynsym_index_list.append(symbol_dynsym_index)


def ret_symbol_dynsym_dict():
    section_dynsym_obj = elf_fp.get_section_by_name('.dynsym')
    section_dynsym_addr = section_dynsym_obj.header.sh_addr
    section_dynsym_data = section_dynsym_obj.data()
    section_dynsym_data_list = ret_list_base_len(
        section_dynsym_data, symbol_dynsym_sz)

    symbol_dynsym_addr_list = []
    symbol_dynsym_data_list = []

    for i in range(symbol_num):
        symbol_dynsym_index = symbol_dynsym_index_list[i]
        symbol_dynsym_addr = section_dynsym_addr+symbol_dynsym_index*symbol_dynsym_sz
        symbol_dynsym_data = section_dynsym_data_list[symbol_dynsym_index]

        symbol_dynsym_addr_list.append(symbol_dynsym_addr)
        symbol_dynsym_data_list.append(symbol_dynsym_data)

    return OrderedDict(zip(symbol_dynsym_addr_list, symbol_dynsym_data_list))


def ret_symbol_gnu_version_dict():
    section_gnu_version_obj = elf_fp.get_section_by_name('.gnu.version')
    section_gnu_version_addr = section_gnu_version_obj.header.sh_addr
    section_gnu_version_data = section_gnu_version_obj.data()
    section_gnu_version_data_list = ret_list_base_len(
        section_gnu_version_data, 2)

    symbol_gnu_version_addr_list = []
    symbol_gnu_version_data_list = []

    for i in range(symbol_num):
        symbol_gnu_version_index = symbol_dynsym_index_list[i]
        symbol_gnu_version_addr = section_gnu_version_addr+symbol_gnu_version_index*2
        symbol_gnu_version_data = section_gnu_version_data_list[symbol_gnu_version_index]

        symbol_gnu_version_addr_list.append(symbol_gnu_version_addr)
        symbol_gnu_version_data_list.append(symbol_gnu_version_data)

    return OrderedDict(zip(symbol_gnu_version_addr_list, symbol_gnu_version_data_list))


def ret_jmp_machine_code(src_addr, target_addr):
    if arch == 'amd64':
        jmp_machine_code = '\xff\x25{}'.format(p32(target_addr-(src_addr+6)))
        return jmp_machine_code
    else:
        if elf_fp.pie:
            jmp_machine_code = '\xff\xa3{}'.format(
                p32(target_addr-section_got_plt_addr))
            return jmp_machine_code
        else:
            jmp_machine_code = '\xff\x25{}'.format(p32(target_addr))
            return jmp_machine_code


def exchange_plt():
    section_plt_got_plt_addr_dict = ret_section_plt_got_plt_addr_dict()
    symbol_plt_addr_list = section_plt_got_plt_addr_dict.keys()
    symbol_got_plt_addr_list = section_plt_got_plt_addr_dict.values()
    symbol_got_plt_addr_list = symbol_got_plt_addr_list[offset:] + \
        symbol_got_plt_addr_list[:offset]
    for i in range(symbol_num):
        src_addr = symbol_plt_addr_list[i]
        target_addr = symbol_got_plt_addr_list[i]
        jmp_machine_code = ret_jmp_machine_code(src_addr, target_addr)
        elf_fp.write(src_addr, jmp_machine_code)


def list_move_right(arg_list):
    new_list = ['']*len(arg_list)
    for i in range(symbol_num):
        target_index = (i+offset) % symbol_num
        new_list[target_index] = arg_list[i]
    return new_list


def exchange_dynsym():

    set_symbol_dynsym_index_list()

    section_dynsym_dict = ret_symbol_dynsym_dict()
    symbol_dynsym_addr_list = section_dynsym_dict.keys()
    symbol_dynsym_data_list = section_dynsym_dict.values()
    symbol_dynsym_data_list = list_move_right(symbol_dynsym_data_list)

    for i in range(symbol_num):
        elf_fp.write(symbol_dynsym_addr_list[i], symbol_dynsym_data_list[i])


def exchange_gnu_version():
    section_gnu_version_dict = ret_symbol_gnu_version_dict()
    symbol_gnu_version_addr_list = section_gnu_version_dict.keys()
    symbol_gnu_version_data_list = section_gnu_version_dict.values()
    symbol_gnu_version_data_list = list_move_right(
        symbol_gnu_version_data_list)

    for i in range(symbol_num):
        elf_fp.write(
            symbol_gnu_version_addr_list[i], symbol_gnu_version_data_list[i])


def exchangeGot(fpath, arg_offset=1):
    init_gloVar(fpath, arg_offset)
    exchange_plt()
    exchange_dynsym()
    exchange_gnu_version()
    elf_fp.save('./after_exchangeGot')
