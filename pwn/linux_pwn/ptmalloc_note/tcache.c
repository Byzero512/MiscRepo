
tache_1: //use in __libc_malloc() before __int_malloc()
        #if USE_TCACHE
            size_t tbytes = request2size (bytes);
            size_t tc_idx = csize2tidx (tbytes);
            MAYBE_INIT_TCACHE ();

            DIAG_PUSH_NEEDS_COMMENT;
            if (tc_idx < mp_.tcache_bins
                /*&& tc_idx < TCACHE_MAX_BINS*/ /* to appease gcc */
                && tcache
                && tcache->entries[tc_idx] != NULL)
                {
                    return tcache_get (tc_idx);
                }
            DIAG_POP_NEEDS_COMMENT;
            
        #endif

tcache_2: //use in __int_malloc() after remove the victim in fastbin

        #if USE_TCACHE
            /* While we're here, if we see other chunks of the same size,
                stash them in the tcache.  */
            size_t tc_idx = csize2tidx (nb);
            if (tcache && tc_idx < mp_.tcache_bins)
            {
                mchunkptr tc_victim;

                /* While bin not empty and tcache not full, copy chunks over.  */
                while (tcache->counts[tc_idx] < mp_.tcache_count
                    && (pp = *fb) != NULL)
                {
                    REMOVE_FB (fb, tc_victim, pp);
                    if (tc_victim != 0)
                    {
                        tcache_put (tc_victim, tc_idx);
                    }
                }
            }
        #endif

tcache_3: //use in __int_malloc() when use smallbin
        #if USE_TCACHE
            /* While we're here, if we see other chunks of the same size,
                stash them in the tcache.  */
            size_t tc_idx = csize2tidx (nb);
            if (tcache && tc_idx < mp_.tcache_bins)
            {
                mchunkptr tc_victim;

                /* While bin not empty and tcache not full, copy chunks over.  */
                while (tcache->counts[tc_idx] < mp_.tcache_count
                    && (tc_victim = last (bin)) != bin)
                {
                    if (tc_victim != 0)
                    {
                        bck = tc_victim->bk;
                        set_inuse_bit_at_offset (tc_victim, nb);
                        if (av != &main_arena)
                        set_non_main_arena (tc_victim);
                        bin->bk = bck;
                        bck->fd = bin;
                        tcache_put (tc_victim, tc_idx);
                    }
                }
            }
        #endif

tcache_4: // use in __int_malloc() when traverse the unsortedbin
        #if USE_TCACHE                        
                /* Fill cache first, return to user only if cache fills.
                We may return one of these chunks later.  */
                if (tcache_nb
                && tcache->counts[tc_idx] < mp_.tcache_count)
                {
                    tcache_put (victim, tc_idx);
                    return_cached = 1;
                    continue;             //这里很特别
                }
                else                                                       
                {
        #endif
                    check_malloced_chunk (av, victim, nb);                  //check.
                    void *p = chunk2mem (victim);
                    alloc_perturb (p, bytes);
                    return p;
        #if USE_TCACHE
                }
        #endif

tcache_5: // use in __int_malloc() after traverse the unsortedbin
    
        #if USE_TCACHE
            /* If we've processed as many chunks as we're allowed while
            filling the cache, return one of the cached ones.  */
            ++tcache_unsorted_count;
            if (return_cached
            && mp_.tcache_unsorted_limit > 0
            && tcache_unsorted_count > mp_.tcache_unsorted_limit)
            {
                return tcache_get (tc_idx);
            }
        #endif

        #define MAX_ITERS       10000
            if (++iters >= MAX_ITERS)
                break;
            }

        #if USE_TCACHE
            /* If all the small chunks we found ended up cached, return one now.  */
            if (return_cached)
            {
                return tcache_get (tc_idx);
            }
        #endif

tcache_6:  
        #if USE_TCACHE
        {
            size_t tc_idx = csize2tidx (size);

            if (tcache
            && tc_idx < mp_.tcache_bins
            && tcache->counts[tc_idx] < mp_.tcache_count)
            {
                    tcache_put (p, tc_idx);
                    return;
            }
        }
        #endif

__libc_malloc:
    tcache_1; //tcache_1: malloc chunk的时候先从tcache中尝试

    __int_malloc:    
        fastbin:
            exact fit:
                remove victim from fastbin

            tcache_2 // tcache_2: 把fastbin剩下的fastchunk挂到tcache上

            return victim
        smallbin:
            exact fit:
                remove victim from smallbin
            tcache_3 // tcache_3: 把smallbin剩下的smallchunk挂到tcache上

            return victim
        for(;;)
            unsortedbin:
                exact fit:
                    tcache_4 //[continue]   //在unsortedbin中只有exact fit才会进入tcache
                place chunk in its bin
                if(tcache_4)
                    tcache_5               //如果tcache_4可以执行, 那么将从tcache中返回victim
                    return victim          //并且这个victim是tcache中的第一个, 而不是unsortedbin中的最后一个exactfit
                return victim

__libc_free:
    MAYBE_INIT_TCACHE

    __int_free:
        check size
        check align
        check_inuse_chunk()           //这个貌似没有检查
        tcache_6                      // put freed chunk in tcache
        
