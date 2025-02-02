def is_fake_cmp(instr):
    if instr.tokens[0].text == "cmp":
        op1 = instr.tokens[2]
        op2 = instr.tokens[4]
        if op1.text == op2.text:
            return True

def is_jump(instr):
    if instr.tokens[0].text in ["je", "jne", "jz", "jnz"]:
        return True
    else:
        return False

def find_fake_jmps(basic_block):
    fake_jmps = []
    instructions = basic_block.get_disassembly_text()
    ctr = 0
    while ctr < len(instructions):
        instr = instructions[ctr]
        if is_fake_cmp(instr):
            #print(f"[i] Fake cmp @ 0x{instr.address:016X}")
            next_instr = instructions[ctr + 1]
            if is_jump(next_instr):
                print(f"[*] FOUND FAKE jump @ 0x{next_instr.address:016X}")
                fake_jmps.append( (instr, next_instr) )
                ctr += 1
        ctr += 1
    return fake_jmps

def patch_fake_jmp(instr_pair):
    cmp_instr = instr_pair[0]
    jmp_instr = instr_pair[1]
    jmp_type = jmp_instr.tokens[0].text

    if jmp_type == "je":
        bv.always_branch(jmp_instr.address)
    elif jmp_type == "jne":
        bv.never_branch(jmp_instr.address)
    elif jmp_type == "jz":
        bv.always_branch(jmp_instr.address)
    elif jmp_type == "jnz":
        bv.never_branch(jmp_instr)
    else:
        print(f"[!] Unhandled jmp @ 0x{jmp_instr.address:016X}")
        return False
    bv.convert_to_nop(cmp_instr.address)
    return True

def remove_fake_branches(fn_addr):
    n_patched = 0
    f = bv.get_function_at(fn_addr)
    for basic_block in f.basic_blocks:
        fake_jmps = find_fake_jmps(basic_block)
        for fj in fake_jmps:
            if patch_fake_jmp(fj):
                n_patched +=1

bv.begin_undo_actions()
remove_fake_branches(0x7ffd00e31000)
bv.commit_undo_actions()
