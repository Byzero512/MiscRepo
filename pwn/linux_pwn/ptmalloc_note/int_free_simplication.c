int_free()
{
    check_align:
        ptr;
        lock;
        size;
    check_inuse_chunk();

    if(fastchunk (&& next!=topchunk))           //TRIM
        check next->size;
        check double_free;
        check idx;

    else if(other nchunk)
        check not_top_chunk;
        check next_chunk < av->top+topchunk->size;
        check next->prev_inuse==1;                      //p inused
        check next->size;                               

        if(prv freed)
            merge;
            unlink;            

        if(next not top_chunk)
            if(next freed)
                unlink;
                merge;
            else
                clear_inuse_bit_at_offset(nextchunk,0);

            check unsortedbin->fd->bk==unsortedbin;
            link;
            do_check_free_chunk();

        else  //next is top chunk
            merge;
            do_check_chunk();
            malloc_consolidate(); 

        if(free_size>=0x10000 && have fastbin)   //这里经常会被忽略吧
            malloc_consolidate();               //这里对fastbin中的chunk是没有检查的，基本来是0x80的chunk改成0xfffffffffffffff1也是可以的
                                                //并且还会帮忙设置next->prevsize
}
//set_head 设置p的size
//set_foot 设置next的prevsize
// link-->set something-->check()-->ret