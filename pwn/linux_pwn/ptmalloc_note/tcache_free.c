
maybe_init_tcache(){
    /*
    struct tcache_perthread_struct
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

tcache_put(mchunkptr chunk,size_t tc_idx){
    check tc_idx                 // 可以说没有检查
    put_into_tcache()
}


#define max_address top+top->size
#define min_address max_address-av->system_mem
#define minsize 32
#define FASTBIN_CONSOLIDATION_THRESHOLD 0x10000

__libc_free(){

    maybe_init_tcache()

    _int_free(){
            check(){
                addr valid
                addr align
                p->size > minsize
            }

            check_inuse_chunk(){                
                p >= min_address
                p+p->size <=top
                
                if(prv_freed){
                    check(){
                        //只有prv->size>=minsize才需要瞒住下面五个条件
                        //否则只需要prv->size==8
                        prv->prev_inuse==1
                        prv->size align
                        prv addr align
                        prv->next_chunk->prev_size==prv->size
                        prv->next_chunk == top || inuse(prv->next_chunk)
                        /*
                        prv >= min_address
                        prv + prv->size <= top
                        */
                    }
                }
                if(next==top){
                    check(){
                        next->prev_inuse == 1
                        next->size >= minsize
                    }
                }
                else if(next freed){
                    check(){
                        //下面五个检查只有next->size < minsize才需要
                        //否则只需要 next->size==8
                        next->size align
                        next->prev_inuse == 1
                        next align
                        next->next_chunk->prevsize == next->size
                        next->next_chunk == top || inuse(next->next_chunk)
                        /*
                        next >= minsize
                        next + next->size <= top
                        */
                    }
                }
            }
            
            #if USE_TCACHE
                tc_idx=csize2tidx(size); // size = chunksize(p)
                if(tcache
                    && tc_idx < tcache_bins
                    && tcache->counts[tc_idx] < max ){
                    tcache_put(p)
                    return
                }
            #endif

            // free fastchunk
            free_fast(){
                check(){
                    p->size
                    next->size
                    double_free // just check bin head
                    not_free_top
                    check idx (correspond size)
                }
            }

            else if free_mmap(){
                munmap_chunk(p)
            }

            // free normal chunk
            else free_nonmmap(){
                check(){
                    not_free_top
                    next->size
                    next->prev_inuse==1
                    next <=top+top->size // max_address
                }
                //free_perturb (chunk2mem(p), size - 2 * SIZE_SZ);

                if(p->prev_inuse==0){
                    /* 
                        merge(){
                            prevsize=p->prev_size
                            size+=prevsize
                            p=p-prev_size
                        }
                    */
                    unlink(prv) 
                }

                if(next != top){

                    if( next_free ){
                        unlink(next)
                        /*
                            merge(){
                                size += next->size
                            }
                        */
                    }
                    else{
                        clear_next_inuse_bit()
                    }

                    /* 这个check也很重要
                        unsortedbin_check(){
                            unsortedbin->fd->bk == unsortedbin
                        }
                    */
                    link_in_unsortedbin(){
                            p->fd=bin->fd
                            p->bk=bin
                            /*如果是free largechunk的话还需要设置nextsize链为空
                                if(p_is_largebin){
                                    set_p_nextsize_null()
                                }
                            */
                    }

                    set_head(p)          // also set p->prev_inuse bit
                    set_foot(p)          //set next->prev_size

                    check_free_chunk(){
                        check(){
                            //下面五个检查只有new_next->size >= minsize才会进行
                            //否则只需要new_next->size==8即可
                            p->size align
                            p addr align

                            new_next->next_chunk->prev_size==new_next->size
                            new_next->prev_inuse==1
                            new_next->next_chunk == topchunk || inuse(new_next->next_chunk)
                            /*
                            new_next >= min_address
                            new_next + new_next->size <=top
                            */
                        }

                    }
                }
                
                // next is top
                else{                    
                    size += next->size
                    set_head(p)       // also set p->prev_inuse bit
                    top = p
                    check(){
                        p->size >= minsize
                        p->prev_inuse==1
                    }
                }
            }

            // free p->size >=0x10000 (FASTBIN_CONSOLIDATION_THRESHOLD)
            // maybe return space to system
            if(free_size >= 0x10000){

                if(have_fastbin){
                    malloc_consolidate()
                }

                return_space_to_system(){
                    if(top->size > 0x20000){
                        systrim()      // 返回空间给系统
                    }
                }
            }
        }
    }
}