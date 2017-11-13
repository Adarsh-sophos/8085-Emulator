from tokens import create_tokens
import time


def binadd(a, b, flags):
    '''
    Function to add two binary numbers.
    It takes input two binary strings and return the string which represents sum of numbers represented by the input strings
    '''    
    
    result = ""
    carry = '0'
    no1 = 0
    
    for i in range(7,-1,-1):
        if a[i] == '0' and b[i] == '0' and carry =='0':
            result = '0' + result
            carry = '0'
        elif a[i] == '1' and b[i] == '1' and carry =='0':
            result ='0' + result
            carry = '1'
        elif a[i] == '1' and b[i] =='0' and carry == '0':
            result = '1' + result
            carry = '0'
        elif a[i] == '0' and b[i] =='1' and carry == '0':
            result = '1' + result
            carry = '0'
        elif a[i] == '1' and b[i] =='0' and carry == '1':
            result = '0' + result
            carry = '1'
        elif a[i] == '0' and b[i] =='1' and carry == '1':
            result = '0' + result
            carry = '1'
        elif a[i] == '1' and b[i] =='1' and carry == '1':
            result = '1' + result
            carry = '1'
        elif a[i] == '0' and b[i] =='0' and carry == '1':
            result = '1' + result
            carry = '0'
        
        # Auxiliary flag
        if i == 4 and carry == '1':
            flags['AC'] = 1
        else:
            flags['AC'] = 0
        
    # Count number of 1's
    for i in range(8):
        if result[i] == '1':
            no1 = no1+1
    
    # Carry flag    
    if carry == '1':
        flags['C'] = 1
    else:
        flags['C'] = 0
    
    # Zero flag
    if int(result, 2) == 0:
        flags['Z'] = 1
    else:
        flags['Z'] = 0
    
    # Sign flag
    if result[0] == '1':
        flags['S'] = 1
    else:
        flags['S'] = 0
    
    # Parity flag
    if no1%2 == 0:
        flags['P'] = 1
    else:
        flags['P'] = 0
    
    return result

              
def comp(a):
    # Function for 2's complement of a binary number.
    
    result = ""
    
    # take 1's complement
    for i in range(8):
        if a[i] == "0":
            result += "1"
        elif a[i] == "1":
            result += "0"

    carry = 1
    
    for i in range(7,-1,-1):
        if result[i] == "0" and carry == 0:
            result = result[:i] + str(0) + result[i+1:]
            carry = 0 
        elif result[i] == "0" and carry == 1:
            result = result[:i] + str(1) + result[i+1:]
            carry = 0
        elif result[i] == "1" and carry == 0:
            result = result[:i] + str(1) + result[i+1:]
            carry = 0
        elif result[i] == "1" and carry == 1:
            result = result[:i] + str(0) + result[i+1:]
            carry = 1
    
    return result


def hexToBin(a):
    # Converts a hexadecimal number in binary
    
    result = ""
    
    for c in a:
        result += bin(eval('0x'+c)).lstrip("0b").zfill(4)
    
    return result


def binToHex(a):
    # Converts a binary number in hexadecimal
       
    result = hex(int(a, 2)).lstrip('0x').zfill(2)
    
    return result
        
        
        
# starting program
if __name__ == '__main__':
        
    start_time = time.clock()
    print("Enter file name : ",end="")
    input_file = input()
    
    # input file
    fo = open("Example programs/" + input_file + ".txt", "r")   
    lines = fo.readlines()
    fo.close()
    
    prnt = list(lines)
    i = 0
    
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
    
    memory[eval('0x2200')] = hexToBin('04')
    memory[eval('0x2201')] = hexToBin('9A')
    memory[eval('0x2202')] = hexToBin('52')
    memory[eval('0x2203')] = hexToBin('89')
    memory[eval('0x2204')] = hexToBin('3F')
    memory[eval('0x2205')] = hexToBin('40')
    memory[eval('0x2206')] = hexToBin('11')
    memory[eval('0x2207')] = hexToBin('38')
    memory[eval('0x2208')] = hexToBin('35')
    memory[eval('0x2209')] = hexToBin('3A')
    '''
    # initialize memory locations by user
    print("\nStore data in memory locations.")
    print("(Type 'E' to exit)")
    while(1):
        mem_addr = input("Memory Address: 0x")
        
        if(mem_addr == "E" or mem_addr == "e"):
            print("-----------------\n")
            break
        
        mem_value = input("   Enter Value: 0x")
        memory[eval("0x"+mem_addr)] = hexToBin(mem_value)
        print('')
    '''
    # save labels for jump statements
    labels = {}
    
    for i in range(len(lines)):
        
        # create tokens
        p = lines[i].split()
        
        # if a empty line is encountered
        if(lines[i] == ""):
            continue
        
        if(prnt[i].find('//') != -1):
            continue
        
        if(':' in lines[i]):
            labels[p[0]] = i
            temp_a = lines[i].find(':')
            lines[i] = lines[i][temp_a+1:]
            #print(lines[i])

    j = 0
    
    # tracks number of lines
    pq = 1    
    
    # iterate over every line in program
    while(j < len(lines)):
        
        # create tokens
        p = lines[j].strip().split()
        
        # if a empty line is encountered
        if(lines[j] == ""):
            pq=pq+1
            j=j+1
            continue
        
        if(prnt[j].find('//') != -1):
            pq=pq+1
            j=j+1            
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
                reg[p[1]] = hexToBin(p[3][0:2])
                reg[chr(ord(p[1])+1)] = hexToBin(p[3][2:4])
            
            elif(p[1] == "H"):
                reg['H'] = hexToBin(p[3][0:2])
                reg['L'] = hexToBin(p[3][2:4])                

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
            
            if flags['S'] == 0:
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
            
            if flags['S'] == 0:
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
            
            if p[1] == 'B':
                temp_a = bin(int(reg['B']+reg['C'], 2)+1).lstrip("0b").zfill(16)
                reg['B'] = temp_a[0:8]
                reg['C'] = temp_a[8:16]
                    
            elif p[1] == 'D':
                temp_a = bin(int(reg['D']+reg['E'], 2)+1).lstrip("0b").zfill(16)
                reg['D'] = temp_a[0:8]
                reg['E'] = temp_a[8:16]
                    
            elif p[1] == 'H':
                temp_a = bin(int(reg['H']+reg['L'], 2)+1).lstrip("0b").zfill(16)
                reg['H'] = temp_a[0:8]
                reg['L'] = temp_a[8:16]
        
        elif(p[0] == "DCX"):
            
            if p[1] == 'B':
                temp_a = bin(int(reg['B']+reg['C'], 2)-1).lstrip("0b").zfill(16)
                reg['B'] = temp_a[0:8]
                reg['C'] = temp_a[8:16]
                    
            elif p[1] == 'D':
                temp_a = bin(int(reg['D']+reg['E'], 2)-1).lstrip("0b").zfill(16)
                reg['D'] = temp_a[0:8]
                reg['E'] = temp_a[8:16]
                    
            elif p[1] == 'H':
                temp_a = bin(int(reg['H']+reg['L'], 2)-1).lstrip("0b").zfill(16)
                reg['H'] = temp_a[0:8]
                reg['L'] = temp_a[8:16]  
            

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
                temp_c = "0000000" + str(flags['C']) 
                reg['H'] = binadd(reg['H'], reg['B'], flags)
                reg['H'] = binadd(reg['H'], temp_c, flags)
            
            if p[1] == 'D':
                reg['L'] = binadd(reg['L'], reg['E'], flags)
                temp_c = "0000000" + str(flags['C']) 
                reg['H'] = binadd(reg['H'], reg['D'], flags)
                reg['H'] = binadd(reg['H'], temp_c, flags)
                    
            if p[1] == 'H':
                reg['L'] = binadd(reg['L'], reg['L'], flags)
                temp_c = "0000000" + str(flags['C']) 
                reg['H'] = binadd(reg['H'], reg['H'], flags)
                reg['H'] = binadd(reg['H'], temp_c, flags)               
                    
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
            
            result = ""
            
            for i in range(8):
                if temp_a[i] == '0' and temp_b[i] == '0':
                    result += '0'
                    
                elif temp_a[i] == '1' and temp_b[i] == '0':
                    result += '0'
                    
                elif temp_a[i] == '0' and temp_b[i] == '1':
                    result += '0'
             
                elif temp_a[i] == '1' and temp_b[i] == '1':
                    result += '1'
                    
            reg['A'] = result
                    
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
            result = ""
            
            for i in range(8):
                if reg['A'][i] == '0' and temp_b[i] == '0':
                    result += '0'
                    
                elif reg['A'][i] == '1' and temp_b[i] == '0':
                    result += '0'
                    
                elif reg['A'][i] == '0' and temp_b[i] == '1':
                    result += '0'
             
                elif reg['A'][i] == '1' and temp_b[i] == '1':
                    result += '1'
                    
            reg['A'] = result                    
            flags['C'] = 0
            flags['AC'] = 1
                    
            if int(reg['A'] , 2) == 0:
                flags['Z'] = 1
            if reg['A'][0] == 1:
                flags['S'] = 1
            
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
            
            result = ""
            
            for i in range(8):
                if temp_a[i] == '0' and temp_b[i] == '0':
                    result += '0'
                
                elif temp_a[i] == '1' and temp_b[i] == '0':
                    result += '1'
                
                elif temp_a[i] == '0' and temp_b[i] == '1':
                    result += '1'
         
                elif temp_a[i] == '1' and temp_b[i] == '1':
                    result += '1'                   
                    
            reg['A'] = result               
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
            
            result = ""
            
            for i in range(8):
                if temp_x[i] == '0' and temp_b[i] == '0':
                    result += '0'
                    
                elif temp_x[i] == '1' and temp_b[i] == '0':
                    result += '1'
                    
                elif temp_x[i] == '0' and temp_b[i] == '1':
                    result += '1'
             
                elif temp_x[i] == '1' and temp_b[i] == '1':
                    result += '1'                  
                    
            reg['A'] = result 
                    
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
            
            result = ""
            
            for i in range(8):
                if temp_a[i] == '0' and temp_b[i] == '0':
                    result += '0'
                
                elif temp_a[i] == '1' and temp_b[i] == '0':
                    result += '1'
                
                elif temp_a[i] == '0' and temp_b[i] == '1':
                    result += '1'
         
                elif temp_a[i] == '1' and temp_b[i] == '1':
                    result += '0'
                                       
            reg['A'] = result                   
            
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
            temp_a = int(p[1] , 16)
            temp_b = bin(temp_a).lstrip("-0b").zfill(8)
            temp_x = reg['A']
            
            result = ""
            
            for i in range(8):
                if temp_x[i] == '0' and temp_b[i] == '0':
                    result += '0'
                    
                elif temp_x[i] == '1' and temp_b[i] == '0':
                    result += '1'
                    
                elif temp_x[i] == '0' and temp_b[i] == '1':
                    result += '1'
             
                elif temp_x[i] == '1' and temp_b[i] == '1':
                    result += '0'                  
                    
            reg['A'] = result
                    
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
            temp_a = ""
            for i in range(8):
                if reg['A'][i] == '0':
                    temp_a += '1'
                elif reg['A'][i] == '1':
                    temp_a += '0'
            reg['A'] = temp_a
            
        # RLC  (Rotate accumulator left) [An+1] <-- [An], [A0] <-- [A7],[CS] <-- [A7]
        # Rotate each bit in the accumulator by one position to the left with the MSB 
        # shifting to the LSB position as well as to the CY flag.

        elif(p[0] == "RLC"):
            flags['C'] = int(reg['A'][0])
            result = ""
            
            for i in range(0,7):
                result += reg['A'][i+1]
            result += flags['C']
            
            reg['A'] = result

        # RAL  (Rotate accumulator left through carry) [An+1] <-- [An], [CS] <-- [A7], [A0] <-- [CS].
        # Rotate each bit in the accumulator by one position to the left with the MSB 
        # shifting to the CY flag and the CY flag bit shifting to the LSB position.

        elif(p[0] == "RAL"):
            temp = flags['C']
            flags['C'] = int(reg['A'][0])
            result = ""
            
            for i in range(0,7):
                result += reg['A'][i+1]
            result += str(temp)
            
            reg['A'] = result
            

        # RRC  (Rotate accumulator right) [A7] <-- [A0], [CS] <-- [A0], [An] <-- [An+1]
        # Rotate each bit in the accumulator by one position to the right with the LSB 
        # shifting to the MSB position as well as to the CY flag.

        elif(p[0] == "RRC"):
            flags['C'] = int(reg['A'][7])
            result = ""
            
            for i in range(7,0,-1):
                result = reg['A'][i-1] + result
            result = flags['C'] + result
            
            reg['A'] = result
            

        # RAR  (Rotate accumulator right through carry) [An] <-- [An+1], [CS] <-- [A0], [A7] <-- [CS] 
        # Rotate each bit in the accumulator by one position to the right with the LSB 
        # shifting to the CY flag and the CY flag bit shifting to the MSB position.

        elif(p[0] == "RAR"):
            temp = flags['C']
            flags['C'] = int(reg['A'][7])
            result = ""
            
            for i in range(7,0,-1):
                result = reg['A'][i-1] + result
            result = str(temp) + result
            
            reg['A'] = result
            
        # CMP R/M
        # Compare the data in register R or memory location M with the data in the 
        # accumulator for equality, greater than or less than.
        # The flags are modified according to the subtraction result of A - R/M. 
        # However, the accumulator retains its earlier value and not the difference.

        elif(p[0] == "CMP"):
            temp = reg['A']
            temp_b = int(reg['A'], 2)
            
            if(p[1] in ['A', 'B', 'C', 'D', 'E', 'H', 'L']):
                temp_a = int(reg[p[1]], 2)
            elif p[1] == "M":
                temp_a = int(memory[int(reg['H'] + reg['L'], 2)] , 2)
            
            if temp_a == temp_b:
                flags['Z'] = 1
            elif temp_a > temp_b:
                flags['C'] = 1
            elif temp_a < temp_b:
                flags['C'] = 0
                    
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
            temp_a = int(p[1], 16)
            temp_b = int(reg['A'] ,2)
            
            if temp_a == temp_b:
                flags['Z'] = 1
            elif temp_a > temp_b:
                flags['C'] = 1
            elif temp_a < temp_b:
                flags['C'] = 0

        # CMC
        # Complement the CY flag bit. No other flag is modified.

        elif(p[0] == "CMC"):
            if flags['C'] == 1:
                flags['C'] = 0
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
            x = int (reg['A'] , 2)
            y = bin(x/10).lstrip("-0b").zfill(4)
            z = bin(x%10).lstrip("-0b").zfill(4)
            p = y+z
            if int (y , 2) > 9:
                flags['C'] = 1
            if int (z , 2) > 9:
                flags['AC'] = 1
            reg['A'] = p
            
            
            no1=0
            
            for i in range(8):
                if reg['A'][i] == 1:
                    no1+=1
            if no1 % 2 == 0 :
                flags['P'] = 1
                
            if int (p , 2) == 0:
                flags['Z'] = 1
                
            if p[0] == 1:
                flags['S'] =1



        ######################################################
        #################### 4. Branching ####################
        ######################################################

        # All three byte instructions.
        # In case of conditional jumping the instructions test the status of one of the
        # four flags S, Z, P, and CY.

        # JMP 16-bit/label
        # Jump the program control unconditionally to the memory location specified by 
        # the 16-bit address mentioned in the instruction (as second and third bytes 
        # of the instruction).

        elif(p[0] == "JMP"):
            if(labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1            
            continue

        # JC 16-bit
        # Jump if Carry flag is set to the 16-bit address.

        elif(p[0] == "JC"):
            if(flags['C'] == 1 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1
            continue

        # JNC 16-bit
        # Jump if Carry flag is not set to the 16-bit address.

        elif(p[0] == "JNC"):
            if(flags['C'] == 0 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1
            continue

        # JZ 16-bit
        # Jump if Zero flag is set to the 16-bit address.

        elif(p[0] == "JZ"):
            if(flags['Z'] == 1 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1
            continue

        # JNZ 16-bit
        # Jump if Zero flag is not set to the 16-bit address.

        elif(p[0] == "JNZ"):
            if(flags['Z'] == 0 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1
            continue

        # JP 16-bit
        # Jump on Plus i.e. if sign flag is reset to the 16-bit address.

        elif(p[0] == "JP"):
            if(flags['S'] == 0 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1            
            continue

        # JM 16-bit
        # Jump on Minus i.e. if sign flag is set to the 16-bit address.

        elif(p[0] == "JM"):
            if(flags['S'] == 1 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1            
            continue

        # JPE 16-bit
        # Jump if Parity flag is set to the 16-bit address. (Even Parity)

        elif(p[0] == "JPE"):
            if(flags['P'] == 1 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1            
            continue

        # JPO 16-bit
        # Jump if Parity flag is reset to the 16-bit address. (Odd Parity)

        elif(p[0] == "JPO"):
            if(flags['P'] == 0 and labels.get(p[1]) != None):
                j = labels.get(p[1])
            else:
                j += 1            
            continue

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
            break

        # NOP  (No Operation)
        # No operation is to be executed.
        # Generally used while trouble shooting a program.

        elif(p[0] == "NOP"):
            pass        
        
        j = j + 1


    # calculate time
    end_time = time.clock()
    run_time = end_time - start_time
    
    # total time in execution
    print("\n Time : {0} seconds\n". format(run_time))
    
    # Register values
    print("  Registers |   Binary    Decimal  Hexadecimal")
    print(" -------------------------------------------")
    print(" Register A |  {0}    {1:0>5d}       0x{2}". format(reg['A'], int(reg['A'], 2), binToHex(reg['A'])))
    print(" Register B |  {0}    {1:0>5d}       0x{2}". format(reg['B'], int(reg['B'], 2), binToHex(reg['B'])))
    print(" Register C |  {0}    {1:0>5d}       0x{2}". format(reg['C'], int(reg['C'], 2), binToHex(reg['C'])))
    print(" Register D |  {0}    {1:0>5d}       0x{2}". format(reg['D'], int(reg['D'], 2), binToHex(reg['D'])))
    print(" Register E |  {0}    {1:0>5d}       0x{2}". format(reg['E'], int(reg['E'], 2), binToHex(reg['E'])))
    print(" Register H |  {0}    {1:0>5d}       0x{2}". format(reg['H'], int(reg['H'], 2), binToHex(reg['H'])))
    print(" Register L |  {0}    {1:0>5d}       0x{2}". format(reg['L'], int(reg['L'], 2), binToHex(reg['L'])))
    
    print('')
    
    # Flags values
    print(" Flags")
    print(" -------------------------------")
    print(" | S | Z |  | AC |  | P |  | C |")
    print(" -------------------------------")
    print(" | {0} | {1} |  |  {2} |  | {3} |  | {4} |". format(flags['S'], flags['Z'], flags['AC'], flags['P'], flags['C']))
    print(" -------------------------------")
    
    print("\n Enter memory address to see its content.")
    #print(" (Use '0x' for addess in hexadecimal)")
    print(" (Type 'E' to exit)")
    
    while(1):
        mem_addr = input("\n Memory Address: 0x")
        
        if(mem_addr == 'E' or mem_addr == 'e'):
            break
        
        print("          Value: {0} {1} 0x{2}". format(memory[eval("0x"+mem_addr)], int(memory[eval("0x"+mem_addr)], 2), hex(int(memory[eval("0x"+mem_addr)], 2)).lstrip("0x").zfill(2)))
    
      
    print("=================================\n")
