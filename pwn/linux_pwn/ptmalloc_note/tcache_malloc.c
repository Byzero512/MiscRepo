maybe_init_tcache(){
    /*struct tcache_perthread_struct
    {
        char counts[TCACHE_MAX_BINS];
        tcache_entry *entries[TCACHE_MAX_BINS]; // tcache_bin 头部
    } tcache_perthread_struct;
    */
    malloc(sizeof(tcache_perthread_struct)) // 分配一个结构体用来管理tcache
}

tcache_get(size_t tc_idx){
    check tidx // no check size and align and other
    return victim
}
tcache_put(mchunkptr p,size_t tc_idx){
    check tc_idx                 // 可以说没有检查
    e=chunk2mem(p)               // tcache中的指针是指向用户空间的
    put_into_tcache(e)
}

#define MAX_ITERS 10000          // 遍历unsortedbin的最大次数

__libc_malloc(){

    /*
    check __malloc_hook
    */
    #if USE_TCACHE
        maybe_init_tcache();
        if(tc_idx < tcache_bins
            && tcache
            && !tcache->counts[tc_idx] !=null ){
            return tcache_get();
        }
    #endif

    _int_malloc(){
        /*
            if no usable arenas:
            sysmalloc  to get a chunk from mmap
        */

        //exact fit in fastbin
        if(fast_req){
               
            check(){
                size_corr_idx   // ***Exp: no check addr align
            }
            victim=REMOVE_FB() 
                
            #if USE_TCACHE
                while(tcache_count < max && have_fastbin)
                    {
                        tcache_p=REMOVE_FB()
                        check tc_idx  // 这里的tc_idx是根据req_size得到的, 也就是说即使是 fastbin上大小不合法的 chunk 也可以进入tcache
                        tcache_put(tcache_p) 
                    }
            #endif

            p=change_victim_to_p()
            return p
        }

        // exact fit in small bin
        if(small_req) {
 
            check(){
                victim=find_victim()
                bck->fd=victim
            }

            set_next_prev_inuse_bit()
            REMOVE_SB(victim)
            /*
            check:
                arena  // arena 和 arena_for_chunk (p) 得到的相对应
                        // 一般不用管
            */
           // ================== 这里的size只要求align, 对大小没要求.            这个trick可以玩一下.
            check_malloced_chunk(){
                check(){
                    victim->addr align
                    victim->size align // also mean that victim->size > minsize
                    victim->prev_inuse==1
                    /*
                    p >= min_address
                    p + p->size <= top
                    */
                }
                if ( next == top ){
                    check(){
                        next->prev_inuse==1
                        next->size>=minsize
                    }
                }

                if ( next freed ){
                    //只有next是freed才需要check
                    check(){
                        next->size >= minsize // 如果这个不大于的话, 下面的五个check都不用进行
                                //只要next->size==8 ????????? 不知道这里有什么用
                        next->prev_inuse==1
                        next->size align
                        next->addr align
                        next->next_chunk->prev_size==next->size
                        next->next_chunk == topchunk || inuse(next->next_chunk)
                        /*范围检查
                        next >= min_address
                        next + next->size <=top
                        */
                    }
                }
            }
            
            #if USE_TCACHE
                while(tcache_count < max && have_smallbin)
                    {
                        set_next_prev_inuse_bit()

                        tcache_p=REMOVE_SB()
                        check tc_idx  // 这里的tc_idx是根据req_size得到的
                        tcache_put(tcache_p) 
                    }
            #endif

            p=change_victim_to_p()
            return p
        }

        if(large_req){
            malloc_consolidate()
        }

// 定义一个和tcache机制有关的结构体
// 用于大循环中unsortedbin的遍历
#if USE_TCACHE
  INTERNAL_SIZE_T tcache_nb = 0;
  size_t tc_idx = csize2tidx (nb);
  if (tcache && tc_idx < mp_.tcache_bins)
    tcache_nb = nb;
  int return_cached = 0;
  tcache_unsorted_count = 0;
#endif

        for(;;){
            
            // 遍历 unsortedbin
            // unsortedbin 不为空
            while ((unsorted_chunks(av)->bk) != unsorted_chunks(av)) {
                victim = unsorted_chunks(av)->bk;
                bck = victim->bk;
                check(){
                    victim->size
                    /*
                        chunksize_nomask (victim) > 2 * SIZE_SZ, 0)
                        && chunksize_nomask (victim) <= system_mem
                    */
                }

                if( small_req && use last_remainder){
                    //fit
                    split
                    check_malloced_chunk(){
                        check(){
                            addr align
                            size align
                            prev_inuse==1
                            /*
                            p >= min_address
                            p + p->size <= top
                            */
                        }
                        if ( next == top ){
                            check:
                                next->prev_inuse==1
                                next->size>=minsize
                        }

                        if ( next freed ){
                            check(){
                                next->size >= minsize // 如果这个不大于的话, 下面的五个check都不用进行
                                //只要next->size==8 (用于next为split remainder剩下的那个chunk)
                                next->prev_inuse==1
                                next->size align
                                next->addr align                            
                                next->next_chunk->prev_size==next->size
                                next->next_chunk == topchunk || inuse(next->next_chunk)

                                /*范围检查
                                next >= min_address
                                next + next->size <=top
                                */
                            }
                        }
                    }
                    return p;
                }

                victim=REMOVE_UB(){
                    unsorted_chunks(av)->bk = bck;
                    bck->fd = unsorted_chunks(av);  
                }

                // all request exact fit
                all_req(){
                        set_next_prev_inuse_bit()
                        #if USE_TCACHE
                            if(tcache_count < max ){
                                tcache_put(victim)        // 将和req相同大小的放到tcache, 不同大小的放到 smallbin 或者 largebin
                                return_cached=1
                                continue    // 进行下一次的unsortedbin遍历
                            }
                            else{
                        #endif
                                check_malloced_chunk() {
                                    check() {
                                        addr align 
                                        size align // 
                                        prev_inuse == 1
                                        /*
                                            p >= min_address
                                            p + p->size <= top
                                        */
                                    }
                                    if (next == top) {
                                        check() {
                                            next->prev_inuse ==1 
                                            next->size >= minsize
                                        }
                                    }

                                    if (next freed) {
                                        //只有next是freed才需要check
                                        check() {
                                            next->size >=minsize  // 如果这个不大于的话,
                                                                 // 下面的五个check都不用进行
                                                                     //只要next->size==8
                                                                     //(用于next为split
                                                                     //remainder剩下的那个chunk)
                                            next->prev_inuse ==1 
                                            next->size align
                                            next->addr align
                                            next->next_chunk->prev_size ==next->size 
                                            next->next_chunk ==topchunk ||inuse(next->next_chunk)

                                            /*范围检查
                                            next >= min_address
                                            next + next->size <=top
                                            */
                                        }
                                    }
                                }
                                p=change_victim_to_p()
                                return p
                        #if USE_TCACHE
                            }
                        #endif
                }

                // if size not exact fit, place it into its bin
                /*这里的link都是没有检查的, 可以进行利用
                    largebin可以进行利用
                */
                place_chunk_in_bin(){
                    if( put_into_smallbin ){
                        put_smallbin(){
                            bck=smallbin_ptr;
                            fwd=bck->fd;
                        }      
                    }
                    else{
                        put_largebin(){      // 这里可以用来 leak heap

                            /* 这里注意一下
                                fwd指向victim要插入的位置的fd指向的地方
                                bck指向victim要插入的位置的bk指向的地方
                            */
                            bck=largebin_ptr;
                            fwd=bck->fd;//= first_chunk_ptr

                            // largebin 不是空的
                            if(fwd!=bck){
                                /*
                                    assert (chunk_main_arena (bck->fd));
                                */
                                // 如果小于最小chunk(意味着唯一大小),
                                // 直接挂到list上
                                if(victim->size<largebin_ptr->bk->size){
                                    link_in(){

                                        fwd = bck;// =largebin_ptr         
                                        bck = bck->bk; //=old_last_chunk_ptr   
                                        victim->fd_nextsize = fwd->fd;//=first_chunk_ptr
                                        victim->bk_nextsize =fwd->fd->bk_nextsize;//=old_last_chunk_ptr
                                        // first_chunk_ptr->bk_nextsize=old_last_chunk_ptr->fd_nextsize=victim
                                        fwd->fd->bk_nextsize =victim->bk_nextsize->fd_nextsize=victim;
                                        /*
                                            victim->fd_nextsize=first_chunk_ptr
                                            victim->bk_nextsize=first_chunk_ptr->bk_nextsize
                                            (first_chunk_ptr->bk_nextsize)->fd_nextsize=victim           这里可以改变一个位置
                                            first_chunk_ptr->bk_nextsize=victim
                                        */
                                    }
                                }
                                else{
                                    // 从前往后找, 找到第一个不大于victim的chunk
                                    // 然后插在它的前面或者其fd指向的地方

                                    /*
                                        assert (chunk_main_arena (fwd));
                                    */
                                    while(victim->size<fwd->size){
                                        fwd=fwd->fd_nextsize;
                                        /*
                                            assert (chunk_main_arena (fwd));
                                        */
                                    }
                                    // 不唯一, 挂在第二个
                                    if(victim->size==fwd->size){
                                        fwd=fwd->fd;
                                    }
                                    // 唯一
                                    // fwd 指向之前存在的 chunk
                                    else{
                                        victim->fd_nextsize = fwd;
                                        victim->bk_nextsize = fwd->bk_nextsize;
                                        fwd->bk_nextsize = victim; 
                                        // (old_fwd->bk_nextsize)->fd_nextsize=victim;
                                        victim->bk_nextsize->fd_nextsize =victim; 
                                    }
                                    bck = fwd->bk;      
                                }
                            }
                            // largebin 是空的
                            else{
                                // 将fd_nextsize指向自身, 可以用来leak heap
                                victim->fd_nextsize = victim->bk_nextsize=victim;
                            }
                        } 
                    }
                    /*  用于next fit分配使用
                        mark_bin(av) 
                    */
                    set_rest_link(){
                        victim->bk = bck;
                        victim->fd = fwd;
                        fwd->bk = victim;                
                        bck->fd = victim;     //     
                    }
                }

                // return chunk from tcache
                #if USE_TCACHE
                    ++tcache_unsorted_count
                    if(return_cached && tcache_unsorted_limit >0 && tcache_unsorted_count > tcache_unsorted_limit)
                     //tcache_unsorted_limit default is 0
                        return tcache_get()
                #endif
                
                // unsortedbin 的遍历次数上限是10000次
                // #define MAX_ITERS       10000
                     if (++iters >= MAX_ITERS)
                        break;
            }

            // return chunk from tcache
            #if USE_TCACHE
                if(return_cached){
                    return tcache_get()
                }
            #endif

            // largebin nextfit in the same largebin
            // for large request
            if(large_req){

                victim = find_victim(){
                    // 先比较最大的chunk是否比需要的大, 如果是, 从nextsize链的最后那个开始
                    // 遍历, 知道找到一个不小于需要的大小的chunk. 
                }   
                unlink(victim)

                set_next_previnuse_bit()
                
                set_head(victim) // also set victim prev_inuse bit
                set_head(remainder) // also set remainder prev_inuse bit
                set_foot(remainder)

                check_malloced_chunk(){
                    check(){
                        addr align
                        size align
                        prev_inuse==1
                        /*
                            p >= min_address
                            p + p->size <= top
                        */
                    }
                    if ( next == top ){
                        check(){
                            next->prev_inuse==1
                            next->size>=minsize
                        }
                    }

                    if ( next freed ){
                        //只有next是freed才需要check
                        check(){
                            next->size >= minsize // 如果这个不大于的话, 下面的五个check都不用进行
                            //只要next->size==8 (用于next为split remainder剩下的那个chunk)
                            next->prev_inuse==1
                            next->size align
                            next->addr align                            
                            next->next_chunk->prev_size==next->size
                            next->next_chunk == topchunk || inuse(next->next_chunk)

                            /*范围检查
                            next >= min_address
                            next + next->size <=top
                            */
                        }
                    }
                }
                p=change_victim_to_p()
                return p
            }

            // next fit for all request 
            next_fit_all_req(){

                victim=find_victim()
                unlink(victim)
                split()

                set_head(victim) // also set victim prev_inuse bit 
                set_head(remainder) // also set remainder prev_inuse bit
                set_foot(remainder)

                check_malloced_chunk(victim){
                    check(){
                        addr align
                        size align
                        prev_inuse==1
                        /*
                        p >= min_address
                        p + p->size <= top
                        */
                    }
                    if ( next == top ){
                        check(){
                            next->prev_inuse==1
                            next->size>=minsize
                        }
                    }

                    if ( next freed ){
                        //只有next是freed才需要check
                        check(){
                            next->size >= minsize // 如果这个不大于的话, 下面的五个check都不用进行
                            //只要next->size==8 (用于next为split remainder剩下的那个chunk)
                            next->prev_inuse==1
                            next->size align
                            next->addr align                            
                            next->next_chunk->prev_size==next->size
                            next->next_chunk == topchunk || inuse(next->next_chunk)

                            /*范围检查
                            next >= min_address
                            next + next->size <=top
                            */
                        }
                        
                    }
                }
                return p
            }

            // use top or other
            use_top(){
                if(topchunk fit){
                    spilt()
                    set_head(victim)  // also set victim ->prev_inuse bit
                    set_head(top)     // also set top->prev_inuse bit
                    check_malloced_chunk(victim){
                        check(){
                            addr align
                            size align
                            prev_inuse==1
                            /*
                            p >= min_address
                            p + p->size <= top
                            */
                        }
                        if ( next == top ){
                            check:
                                next->prev_inuse==1
                                next->size>=minsize
                        }

                        if ( next freed ){
                            //只有next是freed才需要check
                            check:
                                next->size >= minsize // 如果这个不大于的话, 下面的五个check都不用进行
                                //只要next->size==8 (用于next为split remainder剩下的那个chunk)
                                next->prev_inuse==1
                                next->size align
                                next->addr align                            
                                next->next_chunk->prev_size==next->size
                                next->next_chunk == topchunk || inuse(next->next_chunk)

                                /*范围检查
                                next >= min_address
                                next + next->size <=top
                                */
                            
                        }
                    }

                    p=change_victim_to_p()
                    return p
                }
                else if(have_fastbin){
                    malloc_consolidate()
                }
                else{
                    p=sysmalloc()
                    return p
                }
            }            
        }           
    }
}



check tcache:
    assert (tc_idx < TCACHE_MAX_BINS);
//===================
REMOVE_SB()
    bin->bk = bck;
    bck->fd = bin;

