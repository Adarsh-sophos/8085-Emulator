from tokens import create_tokens
import time
'''
function to add two binary numbers
it takes input two binary strings and return the string which represents sum of numbers represented by the input strings
'''
def binadd (a,b,flags):
    result=""
    carry = '0'
    no1=0
    no0=0
    for i in range(7,-1,-1):
        if a[i] == '0' and b[i] == '0' and carry =='0':
            result[i] = '0'
            carry = '0'
        elif a[i] == '1' and b[i] == '1' and carry =='0':
            result [i] ='0'
            carry = '1'
        elif a[i] == '1' and b[i] =='0' and carry == '0':
            result [i] = '1'
            carry ='0'
        elif a[i] == '0' and b[i] =='1' and carry == '0':
            result [i] = '1'
            carry ='0'
        elif a[i] == '1' and b[i] =='0' and carry == '1':
            result [i] = '0'
            carry ='1'
        elif a[i] == '0' and b[i] =='1' and carry == '1':
            result [i] = '1'
            carry ='0'
        elif a[i] == '1' and b[i] =='1' and carry == '1':
            result [i] = '1'
            carry ='1'
        elif a[i] == '0' and b[i] =='0' and carry == '1':
            result [i] = '1'
            carry ='0'
        if i == 3 and carry == '1':
            flags['AC'] =1
        if result[i] == '1':
            no1 = no1+1
        else:
            no0+=1
    if carry == '1':
        flags['C'] =1 
    if int (result , 2)==0:
            flags['Z'] =1
    if result[0] == '1':
            flags['S'] = 1
    if no1 %2 ==0:
            flags['P'] =1
    retrun result
              
def comp (a):
    for i in range(8):
        if a[i] == "0":
            a[i] ="1" 
        elif a[i] == "1":
            a[i] = "0"
    carry = 0
    for i in range(7,-1,-1):
        if a[i] == "0" and carry == 0:
            a[i] = 0
            carry =0 
        elif a[i] == "1" and carry == 1:
            a[i] =1
            carry = 0
        elif a[i] == "1" and carry == 1:
            a[i] = 0
            carry =1
        elif a[i] == "0" and carry ==1 :
            a[i] = 1
            carry = 0
    return a
              
              
        
# starting program
if __name__ == '__main__':
        
    start_time = time.clock()
    print("Enter file name : ",end="")
    input_file = input()
    # input file
    fo = open(input_file,"r")
    
    lines = fo.readlines()
    fo.close()
    prnt = list(lines)
    i=0
    
    # remove any whitespaces before processing
    for q in lines:
        lines[i] = q.strip()
        i=i+1

    # lexical analysis (Creating tokens)
    for q in lines:             
        lines[lines.index(q)] = create_tokens(q)
    
    reg = {'A':"00000000", 'B':"00000000", 'C':"00000000", 'D':"00000000", 'E':"00000000", 'H':"00000000", 'L':"00000000"}
    flags = {'S':0, 'Z':0, 'AC':0, 'P':0, 'C':0}
    
    memory = []
    for i in range(0x0000, 0xFFFF):
        memory.append("00000000")
    
    # tracks number of lines
    pq = 1
    
    # iterate over every line in files
    for t in lines:
        
        # create tokens
        p = t.split()
        
        # if a empty line is encountered
        if(t == ""):
            pq=pq+1
            continue




        ##########################################################
        #################### 1. Data Transfer ####################
        ##########################################################

        # MOV Rd, Rs (Move the content of the one register to another)
        # Here Rd and Rs can be any one of the registers A, B, C, D, E, H, or L
        # One byte instruction.
        # Register addressing mode instruction.
        # MOV A,B will copy the content of register B into the accumulator (i.e. register A).
        #
        # MOV R,M
        # Indirect addressing mode instruction
        #       the instruction MOV D,M will copy the content of a memory location whose
        # address is present in register pair HL into the register D.
        #
        # MOV M,R

        if(p[0] == "MOV"):
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L'] and p[3] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                reg[p[1]] = reg[p[3]]
            
            elif(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L'] and p[3] == 'M'):
                reg[p[1]] = memory[int(reg['H']+reg['L'], 2)]

            elif(p[1] == "M" and p[3] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                memory[int(reg['H'] + reg['L'], 2)] = reg[p[3]]

        # MVI R,8-bit
        # Two byte instruction. 
        # Immediate addressing mode instruction.
        # MVI C,7FH will load register C with the data byte 7FH.
        #
        # MVI M,8-bit

        elif(p[0] == "MVI"):

            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                reg[p[1]] = hexToBin(p[3])

            elif(p[1] == "M"):
                memory[int(reg['H'] + reg['L'], 2)] = hexToBin(p[3])

        # LXI Rp, 16-bit  (Load register pair immediate)
        # Rp can be any one of the register pairs BC, DE, HL, or SP
        # Three byte instruction.
        # Immediate addressing mode instruction.
        # Load register pair Rp immediate with 16-bit data.
        #       instruction LXI D,207FH will load the lower order byte 7FH
        # into the lower order register E and the higher order byte 20H 
        # into the higher order register D.

        elif(p[0] == "LXI"):

            if(p[1] in ['B', 'D']):
                reg[p[1]] = hexToBin(p[3][0-2])
                reg[chr(ord(p[1])+1)] = hexToBin(p[3][2-4])
            
            elif(p[1] == "H"):
                reg['H'] = hexToBin(p[3][0-2])
                reg['L'] = hexToBin(p[3][2-4])                

        # LDAX Rp  (LOAD accumulator indirect) [A] <-- [[rp]]
        # Here Rp can be any one of the register pairs BC or DE.
        # One byte instruction.
        # Indirect addressing mode instruction.
        #       Load accumulator from memory location indirectly through register
        # pair Rp. For example the instruction LDAX B will load the accumulator 
        # with the data byte present in a memory location whose 16-bit address is 
        # specified by the register pair BC.

        elif(p[0] == "LDAX"):
            if(p[1] in ['B', 'D']):
                reg['A'] = memory[int(reg[p[1]]+reg[chr(ord(p[1])+1)], 2)]

        # STAX Rp  (Store accumulator indirect) [[rp]] <-- [A]
        # Here Rp can be any one of the register pairs BC or DE.
        # One byte, Indirect addressing mode
        #       Store the content of the accumulator into a memory location indirectly
        # through register pair Rp. For example the instruction STAX D will store 
        # the data byte present in the accumulator into a memory location whose 
        # 16-bit address is specified by the register pair DE.

        elif(p[0] == "STAX"):
            if(p[1] in ['B', 'D']):
                memory[int(reg[p[1]]+reg[chr(ord(p[1])+1)], 2)] = reg['A']

        # LDA 16-bit  (Load Accumulator direct) [A] <-- [addr]
        # Three byte, Direct addressing mode
        #       Load accumulator with the contents of a memory location whose 16-bit
        # address is directly specified in the instruction. For example the instruction 
        # LDA 207DH will load the accumulator with the data byte present in the memory 
        # location 207DH. 

        elif(p[0] == "LDA"):
            reg['A'] = memory[eval("0x"+p[1])]

        # STA 16-bit  (Store accumulator direct). [addr] <-- [A].
        # Three byte, Direct addressing mode
        #       Store the content of the accumulator in a memory location whose 16-bit
        # address is directly specified in the instruction. For example the instruction 
        # STA 20B4H will store the accumulator data byte in the memory location 20B4H. 

        elif(p[0] == "STA"):
            memory[eval("0x"+p[1])] = reg['A']

        # LHLD 16-bit  (Load H-L pair direct). [L] <-- [addr], [H] <-- [addr+1].
        # Three byte instruction
        #       Copy the data of memory location with the 16-bit address into register L
        # and the data of the next memory location into register H. 
        # No flags are modified.

        elif(p[0] == "LHLD"):
            reg['L'] =  memory[eval("0x"+p[1])]
            reg['H'] =  memory[eval("0x"+p[1])+1]

        # SHLD 16-bit  (Store H-L pair direct) [addr] <-- [L], [addr+1] <-- [H].
        # Three byte instruction.
        #       Copy the data of register L into the memory location with the 16-bit
        # address and the data of register H into the next memory location. No 
        # flags are modified.

        elif(p[0] == "SHLD"):
            memory[eval("0x"+p[1])] = reg['L']
            memory[eval("0x"+p[1])+1] = reg['H']


        # PCHL
        # One byte instruction.
        # Load Program Counter with the 16-bit data of register pair HL. 
        # No flags are affected.

        elif(p[0] == "PCHL"):
            pass

        # SPHL  (Move the contents of H-L pair to stack pointer)
        # One byte instruction.
        # Load the Stack Pointer with the 16-bit data of register pair HL. 
        # No flags are affected.

        elif(p[0] == "SPHL"):
            pass

        # XCHG  (Exchange the contents of H-L with D-E pair) [H-L] <--> [D-E].
        # One byte instruction.
        # Exchange data of registers H and L with D and E respectively. 
        # No flags are modified.

        elif(p[0] == "XCHG"):
            temp_h = reg['H']
            temp_l = reg['L']
            reg['H'] = reg['D']
            reg['L'] = reg['E']
            reg['D'] = temp_h
            reg['E'] = temp_l

        # XTHL  (Exchange stack-top with H-L)
        # One byte instruction.
        # Exchange data of registers H and L with top two memory locations of Stack. 
        # No flags are modified.

        elif(p[0] == "XTHL"):
            pass

        # PUSH Rp  (Push the content of register pair to stack)
        # Rp can be BC, DE, HL, or PSW
        # One byte instruction.
        # Pushes the contents (two bytes) of the specified register pair onto the stack.
        #
        # PUSH PSW (PUSH Processor Status Word)

        elif(p[0] == "PUSH"):
            pass

        # POP Rp  (Pop the content of register pair, which was saved, from the stack)
        # Rp can be BC, DE, HL, or PSW
        # One byte instruction.
        # Pops the top two bytes from a stack to the specified register pair.
        #
        # POP PSW (Pop Processor Status Word)

        elif(p[0] == "POP"):
            pass




        #######################################################
        #################### 2. Arithmetic ####################
        #######################################################

        # ADD R  (Add register to accumulator) [A] <-- [A] + [r].
        # One byte, Register addressing mode
        #       Adds the data in register R with the data in the accumulator and stores
        # the sum in the accumulator. All flags are modified reflecting the data 
        # conditions of the result in the accumulator.
        #
        # ADD M  (Add memory to accumulator) [A] <-- [A] + [[H-L]].
        # Indirect addressing mode
        #       Add the data in a memory location whose address is present in
        # the register pair HL with the data in the accumulator and store the result 
        # in the accumulator. All flags are affected.

        elif(p[0] == "ADD"):
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                reg['A'] = binadd(reg['A'], reg[p[1]], flags)
            elif(p[1] == "M"):
                reg['A'] = binadd(reg['A'], memory[int(reg['H']+reg['L'], 2)], flags)                

        # ADI 8-bit  (Add immediate data to accumulator) [A] <-- [A] + data.
        # Two byte, Immediate addressing mode
        #       Adds the second byte of the instruction with the data in the accumulator
        # and stores the sum in the accumulator. All flags are modified reflecting the 
        # data conditions of the result in the accumulator.

        elif(p[0] == "ADI"):
            temp_a = bin(int(p[1], 16)).lstrip('-0b').zfill(8)
            reg['A'] = binadd(reg['A'], temp_a, flags)
                

        # ADC R/M  (Add register/memory with carry to accumulator). [A] <-- [A] + [r]/[[H-L]] + [CS]
        # One byte instruction.
        #       Add the data in register R or memory location M along with the bit in
        # carry flag with the data in the accumulator and store the result in the 
        # accumulator. All flags are affected.

        elif(p[0] == "ADC"):
            if flags['C'] == 1:
                tc = "00000001"
            else :
                tc = "00000000"
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']): 
                reg['A'] = binadd(reg['A'] , reg[p[1]] , flags)
                reg['A'] = binadd(reg['A'] , tc , flags)
            elif p[1] == "M":
                reg['A'] = binadd(reg['A'] , memory[int(reg['H'] + reg['L'], 2)] , flags)
                reg['A'] = binadd(reg['A'] , tc , flags)
                
            

        # ACI 8-bit  (Add with carry immediate data to accumulator). [A] <-- [A] + data + [CS].
        # Two byte instruction.
        # Add 8-bit data along with CY flag bit to the data in accumulator and store 
        # the result in accumulator. All flags are affected.

        elif(p[0] == "ACI"):
            
            if flags['C'] == 1:
                tc = "00000001"
            else :
                tc = "00000000"
           
            temp_a = bin(int(p[1], 16)).lstrip('-0b').zfill(8)
            reg['A'] = binadd(reg['A'], temp_a, flags)
            reg['A'] = binadd(reg['A'], tc , flags)
                   

        # SUB R  (Subtract register from accumulator). [A] <-- [A] - [r].
        # One byte, Register addressing mode
        #
        # SUB M  (Subtract memory from accumulator). [A] <-- [A] - [[H-L]].
        # Indirect addressing mode    
        #       Subtract the data in a memory location whose address is present in
        # the register pair HL with the data in the accumulator and store the result 
        # in the accumulator. All flags are affected.

        elif(p[0] == "SUB"):
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_a = comp(reg[p[1]])
                reg['A'] = binadd(reg['A'], temp_a, flags)
            
            elif p[1] == "M":
                temp_a = comp(memory[int(reg['H'] + reg['L'], 2)])
                reg['A'] = binadd(reg['A'], temp_a, flags)
            

        # SUI 8-bit  (Subtract immediate data from accumulator) [A] <-- [A] - data.
        # Two byte, Immediate addressing mode

        elif(p[0] == "SUI"):
            temp_a = bin(int(p[1], 16)).lstrip('-0b').zfill(8)
            temp_b = comp(temp_a)
            reg['A'] = binadd(reg['A'] , temp_b, flags)
            

        # SBB R/M  (Subtract register/memory from accumulator with borrow). [A] <-- [A] - [r]/[[H-L]] - [CS].
        # One byte instruction.
        #       Subtract the data in register R or memory location M along with the bit
        # in carry flag (borrow) from the data in the accumulator and store the result 
        # in the accumulator. All flags are affected.

        elif(p[0] == "SBB"):
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_a = comp(reg[p[1]])
            elif p[1] == "M":
                temp_a = comp(memory[int(reg['H'] + reg['L'], 2)])
            
            if flags['C'] == 0:
                temp_b = comp("00000000")
            else :
                temp_b = comp("00000001")
            
            reg['A'] = binadd(reg['A'], temp_a, flags)
            reg['A'] = binadd(reg['A'], temp_b, flags)
        
        
        # SBI 8-bit  (Subtract immediate data from accumulator with borrow). [A] <-- [A] - data - [CS].
        # Two byte instruction.

        elif(p[0] == "SBI"):
            temp_a = bin(int(p[1], 16)).lstrip('-0b').zfill(8)
            temp_b = comp(temp_a)
            
            if flags['C'] == 0:
                temp_c = comp("00000000")
            else :
                temp_c = comp("00000001")
            
            reg['A'] = binadd(reg['A'], temp_b, flags)
            reg['A'] = binadd(reg['A'], temp_c, flags)

        # INR R/M, DCR R/M  ([r] <-- [r] + 1, [[H-L]] <-- [[H-L]] + 1)
        # One byte, Register/Indirect addressing mode
        # Increment/decrement the data in the register R or memory location whose address 
        # is present in register pair HL by 1. 
        # These instructions affect all flags except the Carry flag.

        elif(p[0] == "INR"):
            temp_c = flags['C']
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                reg[p[1]] = binadd(reg[p[1]], "00000001", flags)
            elif p[1] == 'M':
                memory[int(reg['H'] + reg['L'], 2)] = binadd(memory[int(reg['H'] + reg['L'], 2)], "00000001", flags)
            
            flags['C'] = temp_c
        
        elif(p[0] == "DCR"):
            temp_c = flags['C']
            temp_a = comp("00000001")
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):               
                reg[p[1]] = binadd(reg[p[1]], temp_a, flags)
            elif p[1] == 'M':
                memory[int(reg['H'] + reg['L'], 2)] = binadd(memory[int(reg['H'] + reg['L'], 2)], temp_a, flags)
            
            flags['C'] = temp_c        
                

        # INX Rp, DCX Rp  ([rp] <-- [rp] - 1, [rp] <-- [rp] - 1)
        # One byte, Register addressing mode
        # Increment/decrement the data in the register pair Rp by 1. 
        # These instructions do not affect the flags.

        elif(p[0] == "INX"):
            temp_flags = dict(flags)
            
            if p[1] == 'B':
                reg['C'] = binadd(reg['C'], "00000001", flags)
                if flags['C'] == 1:
                    reg['B'] = binadd(reg['B'], "00000001", flags)
                    
            elif p[1] == 'D':
                reg['E'] = binadd(reg['E'], "00000001", flags)
                if flags['C'] == 1:
                    reg['D'] = binadd(reg['D'], "00000001", flags)
                    
            elif p[1] == 'H':
                reg['L'] = binadd(reg['L'], "00000001", flags)
                if flags['C'] == 1:
                    reg['H'] = binadd(reg['H'], "00000001", flags)
            
            flags = dict(temp_flags)
        
        
        elif(p[0] == "DCX"):
            temp_flags = dict(flags)
            temp_a = comp("00000001")
            
            if p[1] == 'B':
                reg['C'] = binadd(reg['C'], temp_a, flags)
                if flags['C'] == 1:
                    reg['B'] = binadd(reg['B'], "00000001", flags)
                    
            elif p[1] == 'D':
                reg['E'] = binadd(reg['E'], temp_a, flags)
                if flags['C'] == 1:
                    reg['D'] = binadd(reg['D'], "00000001", flags)
                    
            elif p[1] == 'H':
                reg['L'] = binadd(reg['L'], temp_a, flags)
                if flags['C'] == 1:
                    reg['H'] = binadd(reg['H'], "00000001", flags)
            
            flags = dict(temp_flags)           
            

        # DAD Rp
        # Rp can be BC, DE, HL, or SP.
        # One byte instruction.
        # Add the specified register pair Rp data with that of HL and store the result 
        # in HL. Only CY flag is affected.

        elif(p[0] == "DAD"):
            temp1 = flags['AC']
            temp2 = flags['P']
            temp3 = flags['S'] 
            temp4 = flags['Z']
            
            if p[1] == 'B':
                reg['L'] = binadd(reg['L'], reg['C'], flags)
                temp_c = flags['C'] 
                reg['H'] = binadd(reg['H'], reg['B'], flags)
                reg['H'] = binadd(reg['H'], hello, flags)
            
            if p[1] == 'D':
                reg['L'] = binadd(reg['L'], reg['E'], flags)
                temp_c = flags['C'] 
                reg['H'] = binadd(reg['H'], reg['D'], flags)
                reg['H'] = binadd(reg['H'], hello, flags)
                    
            if p[1] == 'H':
                reg['L'] = binadd(reg['L'], reg['L'], flags)
                temp_c = flags['C'] 
                reg['H'] = binadd(reg['H'], reg['H'], flags)
                reg['H'] = binadd(reg['H'], hello, flags)               
                    
            flags['AC'] = temp1
            flags['P'] = temp2
            flags['S'] = temp3
            flags['Z'] = temp4




        ####################################################
        #################### 3. Logical ####################
        ####################################################

        # ANA R/M  (AND register/memory with accumulator) [A] <-- [A] ^ [r]/[[H-L]].
        # One byte instruction.
        # Logically AND the data in register R or memory location M with the data in the 
        # accumulator and store the result in the accumulator.
        # All flags except CY and AC are modified reflecting the data conditions of the 
        # result in the accumulator. 
        # CY flag is reset and AC flag is set. 

        elif(p[0] == "ANA"):
            temp_a = reg['A']
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_b = reg[p[1]]
            elif p[1] == 'M':       
                temp_b = memory[int(reg['H'] + reg['L'], 2)]            
                
            for i in range(8):
                if temp_a[i] == '0' and temp_b[i] == '0':
                    temp_a[i]  = '0'
                    
                elif temp_a[i] == '1' and temp_b[i] == '0':
                    temp_a[i]  = '0'
                    
                elif temp_a[i] == '0' and temp_b[i] == '1':
                    temp_a[i]  = '0'
             
                elif temp_a[i] == '1' and temp_b[i] == '1':
                    temp_a[i]  = '1'                   
                    
            reg['A'] = temp_a                    
                    
            flag['C'] = 0
            flag['AC'] = 1
                    
            if int(reg['A'] , 2) == 0:
                flag['Z'] = 1
            if reg['A'][0] == 1:
                flag['S'] = 1
            
            no1=0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            if no1 % 2 == 0 :
                flags['P'] = 1                    

        # ANI 8-bit
        # Two byte instruction.
        # Logically AND the second byte of the instruction with the data in the accumulator 
        # and store the result in the accumulator. 
        # All flags except CY and AC are modified reflecting the data conditions of the 
        # result in the accumulator. 
        # CY flag is reset and AC flag is set.

        elif(p[0] == "ANI"):
            temp_a = int(p[1] , 16)
            temp_b = bin(temp_a).lstrip("-0b").zfill(8)            
            temp_x = reg['A']
            
            for i in range(8):
                if temp_x[i] == '0' and temp_b[i] == '0':
                    temp_x[i] = '0'
                    
                elif temp_x[i] == '1' and temp_b[i] == '0':
                    temp_x[i] = '0'
                    
                elif temp_x[i] == '0' and temp_b[i] == '1':
                    temp_x[i] = '0'
             
                elif temp_x[i] == '1' and temp_b[i] == '1':
                    temp_x[i] = '1'
                    
                    
            reg['A'] = temp_x                     
            flag['C'] = 0
            flag['AC'] = 1
                    
            if int(reg['A'] , 2) == 0:
                flag['Z'] = 1
            if reg['A'][0] == 1:
                flag['S'] = 1
            
            no1=0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            
            if no1 % 2 == 0 :
                flags['P'] = 1
                

        # ORA R/M
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "ORA"):
            temp_a = reg['A']
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_b = reg[p[1]]
            elif p[1] == 'M':        
                temp_b = memory[int(reg['H'] + reg['L'], 2)]
                
            for i in range(8):
                if temp_a[i] == '0' and temp_b[i] == '0':
                    temp_a[i]  = '0'
                
                elif temp_a[i] == '1' and temp_b[i] == '0':
                    temp_a[i]  = '1'
                
                elif temp_a[i] == '0' and temp_b[i] == '1':
                    temp_a[i]  = '1'
         
                elif temp_a[i] == '1' and temp_b[i] == '1':
                    temp_a[i]  = '1'                   
                    
            reg['A'] = temp_a               
            flag['C'] = 0
            flag['AC'] = 0
                    
            if int(reg['A'] , 2) == 0:
                flag['Z'] = 1
            if reg['A'][0] == 1:
                flag['S'] = 1
            
            no1=0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            if no1 % 2 == 0 :
                flags['P'] = 1       

        # ORI 8-bit
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "ORI"):
            temp_a = int(p[1] , 16)
            temp_b = bin(temp_a).lstrip("-0b").zfill(8)
            temp_x = reg['A']
            
            for i in range(8):
                if temp_x[i] == '0' and temp_b[i] == '0':
                    temp_x[i]  = '0'
                    
                elif temp_x[i] == '1' and temp_b[i] == '0':
                    temp_x[i]  = '1'
                    
                elif temp_x[i] == '0' and temp_b[i] == '1':
                    temp_x[i]  = '1'
             
                elif temp_x[i] == '1' and temp_b[i] == '1':
                    temp_x[i]  = '1'                  
                    
            reg['A'] = temp_x 
                    
            flag['C'] = 0
            flag['AC'] = 0
                    
            if int(reg['A'] , 2) == 0:
                flag['Z'] = 1
            if reg['A'][0] == 1:
                flag['S'] = 1
            
            no1 = 0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            
            if no1 % 2 == 0 :
                flags['P'] = 1
                

        # XRA R/M
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "XRA"):
            temp_a = reg['A']
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_b = reg[p[1]]
            elif p[1] == 'M':        
                temp_b = memory[int(reg['H'] + reg['L'], 2)]            
                
            for i in range(8):
                if temp_a[i] == '0' and temp_b[i] == '0':
                    temp_a[i]  = '0'
                
                elif temp_a[i] == '1' and temp_b[i] == '0':
                    temp_a[i]  = '1'
                
                elif temp_a[i] == '0' and temp_b[i] == '1':
                    temp_a[i]  = '1'
         
                elif temp_a[i] == '1' and temp_b[i] == '1':
                    temp_a[i]  = '0'
                                       
                reg['A'] = temp_a                   
            
            flag['C'] = 0
            flag['AC'] = 0
                    
            if int(reg['A'], 2) == 0:
                flag['Z'] = 1
            if reg['A'][0] == 1:
                flag['S'] = 1
            
            no1=0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            
            if no1 % 2 == 0 :
                flags['P'] = 1

        # XRI 8-bit
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "XRI"):
            temp_a = int (p[1] , 16)
            temp_b = bin(temp_a).lstrip("-0b").zfill(8)
            temp_x = reg['A']
            
            for i in range(8):
                if temp_x[i] == '0' and temp_b[i] == '0':
                    temp_x[i]  = '0'
                    
                elif temp_x[i] == '1' and temp_b[i] == '0':
                    temp_x[i]  = '1'
                    
                elif temp_x[i] == '0' and temp_b[i] == '1':
                    temp_x[i]  = '1'
             
                elif temp_x[i] == '1' and temp_b[i] == '1':
                    temp_x[i]  = '0'                  
                    
            reg['A'] = temp_x 
                    
            flag['C'] = 0
            flag['AC'] = 0
                    
            if int(reg['A'], 2) == 0:
                flag['Z'] = 1
            if reg['A'][0] == 1:
                flag['S'] = 1
            
            no1=0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            if no1 % 2 == 0 :
                flags['P'] = 1

        # CMA
        # One byte instruction.
        # Complement (logical NOT) the contents of the accumulator.

        elif(p[0] == "CMA"):
            for i in range(8):
                if reg['A'][i] == 0:
                    reg['A'][i] = 1
                elif reg['A'][i] == 1:
                    reg['A'][i] = 0
            
        # RLC  (Rotate accumulator left) [An+1] <-- [An], [A0] <-- [A7],[CS] <-- [A7]
        # Rotate each bit in the accumulator by one position to the left with the MSB 
        # shifting to the LSB position as well as to the CY flag.

        elif(p[0] == "RLC"):
            flags['C'] = reg['A'][0]
            
            for i in range(0,7):
                reg['A'][i] = reg['A'][i+1]
            
            reg['A'][7] = flags['C']

        # RAL  (Rotate accumulator left through carry) [An+1] <-- [An], [CS] <-- [A7], [A0] <-- [CS].
        # Rotate each bit in the accumulator by one position to the left with the MSB 
        # shifting to the CY flag and the CY flag bit shifting to the LSB position.

        elif(p[0] == "RAL"):
            temp = flags['C']
            flags['C'] = reg['A'][0]
            for i in range(0,7):
                reg['A'][i] = reg['A'][i+1]
            reg['A'][7] = temp
            

        # RRC  (Rotate accumulator right) [A7] <-- [A0], [CS] <-- [A0], [An] <-- [An+1]
        # Rotate each bit in the accumulator by one position to the right with the LSB 
        # shifting to the MSB position as well as to the CY flag.

        elif(p[0] == "RRC"):
            flags['C'] = reg['A'][7]
            for i in range(7,0,-1):
                reg['A'][i] = reg['A'][i-1]
            reg['A'][0] = flags['C']
            

        # RAR  (Rotate accumulator right through carry) [An] <-- [An+1], [CS] <-- [A0], [A7] <-- [CS] 
        # Rotate each bit in the accumulator by one position to the right with the LSB 
        # shifting to the CY flag and the CY flag bit shifting to the MSB position.

        elif(p[0] == "RAR"):
            temp = flags['C']
            flags['C'] = reg['A'][7]
            for i in range(7,0,-1):
                reg['A'][i] = reg['A'][i-1]
            reg['A'][0] = temp

        # CMP R/M
        # Compare the data in register R or memory location M with the data in the 
        # accumulator for equality, greater than or less than.
        # The flags are modified according to the subtraction result of A–R/M. 
        # However, the accumulator retains its earlier value and not the difference.

        elif(p[0] == "CMP"):
            temp = reg['A']
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_a = int (reg[p[1]] , 2)
                temp_b = int(reg['A'] ,2)
                if temp_a == temp_b:
                    flags['Z'] = 1
                elif temp_a > temp_b:
                    flags['C'] = 1
                elif temp_a < temp_b:
                    flags['C'] =0
            elif p[1] == "M":
                temp_a = int (memory[int(reg['H'] + reg['L'], 2)] , 2)
                temp_b = int(reg['A'] ,2)
                if temp_a == temp_b:
                    flags['Z'] = 1
                elif temp_a > temp_b:
                    flags['C'] = 1
                elif temp_a < temp_b:
                    flags['C'] =0
                    
            reg['A'] = temp
            

        # CPI 8-bit
        # Compare the second byte of the instruction with the data in the accumulator 
        # for equality, greater than or less than.
        #
        # The flags are modified according to the subtraction result of A–8-bit data. 
        # However, the accumulator retains its earlier value and not the difference.
        #
        # If
        # (i) A=data, then Z flag is set.
        # (ii) A>data, then CY flag is reset.
        # (iii) A<data, then CY flag is set.

        elif(p[0] == "CPI"):
            temp_a = bin(int(p[1] , 16)).lstrip("-0b").zfill(8)
            temp_b = int(reg['A'] ,2)
            if temp_a == temp_b:
                flags['Z'] = 1
            elif temp_a > temp_b:
                flags['C'] = 1
            elif temp_a < temp_b:
                flags['C'] =0

        # CMC
        # Complement the CY flag bit. No other flag is modified.

        elif(p[0] == "CMC"):
            if flags['C'] == 1:
                flags['C'] =0
            elif flags['C'] == 0:
                flags['C'] = 1

        # STC
        # Set the CY flag. No other flag is modified.

        elif(p[0] == "STC"):
            flags['C'] = 1

        # DAA
        # Decimal Adjust Accumulator. 
        # It converts the accumulator data from binary to BCD using the AC flag internally.

        elif(p[0] == "DAA"):
            pass




        ######################################################
        #################### 4. Branching ####################
        ######################################################

        # All three byte instructions.
        # In case of conditional jumping the instructions test the status of one of the
        # four flags S, Z, P, and CY.

        # JMP 16-bit
        # Jump the program control unconditionally to the memory location specified by 
        # the 16-bit address mentioned in the instruction (as second and third bytes 
        # of the instruction).

        elif(p[0] == "JMP"):
            pass

        # JC 16-bit
        # Jump if Carry flag is set to the 16-bit address.

        elif(p[0] == "JC"):
            pass

        # JNC 16-bit
        # Jump if Carry flag is not set to the 16-bit address.

        elif(p[0] == "JNC"):
            pass

        # JZ 16-bit
        # Jump if Zero flag is set to the 16-bit address.

        elif(p[0] == "JZ"):
            pass

        # JNZ 16-bit
        # Jump if Zero flag is not set to the 16-bit address.

        elif(p[0] == "JNZ"):
            pass

        # JP 16-bit
        # Jump on Plus i.e. if sign flag is reset to the 16-bit address.

        elif(p[0] == "JP"):
            pass

        # JM 16-bit
        # Jump on Minus i.e. if sign flag is set to the 16-bit address.

        elif(p[0] == "JM"):
            pass

        # JPE 16-bit
        # Jump if Parity flag is set to the 16-bit address. (Even Parity)

        elif(p[0] == "JPE"):
            pass

        # JPO 16-bit
        # Jump if Parity flag is reset to the 16-bit address. (Odd Parity)

        elif(p[0] == "JPO"):
            pass

        # CALL 16-bit
        # Call a subroutine i.e. transfer the program control to starting memory 
        # location of a subroutine specified by the 16-bit address mentioned in the 
        # instruction. There are conditional Call instructions as well.

        elif(p[0] == "CALL"):
            pass

        # RET
        # Return to the main program after completing the subroutine. 
        # There are conditional return instructions as well.

        elif(p[0] == "RET"):
            pass




        ############################################################
        #################### 5. Machine Control ####################
        ############################################################

        # HLT
        # Halts any further execution and makes the microprocessor enter into a wait state. 
        # The buses are placed in high impedance state.

        elif(p[0] == "HLT"):
            pass

        # NOP  (No Operation)
        # No operation is to be executed.
        # Generally used while trouble shooting a program.

        elif(p[0] == "NOP"):
            pass







