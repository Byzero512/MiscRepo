check_malloced_chunk(p){
	prev_inuse(p)
	
	check_remalloced_chunk(p){
		check:
			arena
			non_mmap
			p->size > minsize
			addr align

		check_inuse_chunk(p){
			inuse(p)
			do_check_chunk(){
				max_address = topchunk_adr + topchunk->size
				min_address = max_address - av->system_mem
				if(not mmap)
				{
					if(p!=top)
						if(contiguous(av))
						{
							p >= min_address
							p+p->size <= top
			
						}
					if(p==top)
					{
						p->size >= minsize
						prev_inuse(p)
					}
				}
			}

			if(!prev_inuse(p)){
				
				check:
					prv=prev_chunk(p)
					next_chunk(prv)==p
					do_check_free_chunk(prv){
						
						!inuse(prv)
						not_mmap
						if( prv->size >= minsize){
							check:
								prv not_mmap
								prv->size align
								prv addr align
								prev_size(next_chunk(prv))==prv->size
								prev_inuse(prv)
								prv->next_chunk == topchunk || inuse(prv->next_chunk)
						}
						else{
							prv->size ==8  // 用于use last_remainder
						}

						do_check_chunk(prv){
							max_address = topchunk_adr + topchunk->size
							min_address = max_address - av->system_mem
							if(prv not mmap)
							{
								if(prv != top)
									if(contiguous(av))
									{
										prv >= min_address
										prv + prv->size <= top
						
									}
								if(prv == top)
								{
									prv->size >= minsize
									prev_inuse(prv)
								}
							}
						}
					}
			}
			next=next_chunk(p)
			if(next==topchunk){
				prev_inuse(next)
				next->size >= minsize
			}
			else if(!inuse(next)){
				check_free_chunk(next){
					!inuse(next)
					not_mmap
					if(next->size >= minsize){
						check:
							not_mmap
							next->size align
							next addr align
							prev_size(next_chunk(next))==next->size
							prev_inuse(next)
							next->next_chunk == topchunk || innuse(next->next_chunk) 

					}
					else{
						next -> size ==8
					}

					do_check_chunk(next){
						max_address = topchunk_adr + topchunk->size
						min_address = max_address - av->system_mem
						if(not mmap)
						{
							if(p!=top)
								if(contiguous(av))
								{
									p >= min_address
									p+p->size <= top
					
								}
							if(p==top)
							{
								p->size >= minsize
								prev_inuse(p)
							}
						}
					}
				}
			}
		}
	}
}
