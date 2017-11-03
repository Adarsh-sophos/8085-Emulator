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
        flags['C"] =1 
    if int (result , 2)==0:
            flags['Z'] =1
    if result[0] == '1':
            flags['S'] = 1
    if no1 %2 ==0:
            flags['P'] =1
    retrun result
        
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

            if(p[1] in ['B', 'D', 'H']):
                reg[p[1]] = p[3][0-2]
                reg[chr(ord(p[1])+1)] = p[3][2-4]

        # LDAX Rp  (LOAD accumulator indirect) [A] <-- [[rp]]
        # Here Rp can be any one of the register pairs BC or DE.
        # One byte instruction.
        # Indirect addressing mode instruction.
        #       Load accumulator from memory location indirectly through register
        # pair Rp. For example the instruction LDAX B will load the accumulator 
        # with the data byte present in a memory location whose 16-bit address is 
        # specified by the register pair BC.

        elif(p[0] == "LDAX"):
            pass

        # STAX Rp  (Store accumulator indirect) [[rp]] <-- [A]
        # Here Rp can be any one of the register pairs BC or DE.
        # One byte, Indirect addressing mode
        #       Store the content of the accumulator into a memory location indirectly
        # through register pair Rp. For example the instruction STAX D will store 
        # the data byte present in the accumulator into a memory location whose 
        # 16-bit address is specified by the register pair DE.

        elif(p[0] == "STAX"):
            pass

        # LDA 16-bit  (Load Accumulator direct) [A] <-- [addr]
        # Three byte, Direct addressing mode
        #       Load accumulator with the contents of a memory location whose 16-bit
        # address is directly specified in the instruction. For example the instruction 
        # LDA 207DH will load the accumulator with the data byte present in the memory 
        # location 207DH. 

        elif(p[0] == "LDA"):
            pass

        # STA 16-bit  (Store accumulator direct). [addr] <-- [A].
        # Three byte, Direct addressing mode
        #       Store the content of the accumulator in a memory location whose 16-bit
        # address is directly specified in the instruction. For example the instruction 
        # STA 20B4H will store the accumulator data byte in the memory location 20B4H. 

        elif(p[0] == "STA"):
            pass

        # LHLD 16-bit  (Load H-L pair direct). [L] <-- [addr], [H] <-- [addr+1].
        # Three byte instruction
        #       Copy the data of memory location with the 16-bit address into register L
        # and the data of the next memory location into register H. 
        # No flags are modified.

        elif(p[0] == "LHLD"):
            pass

        # SHLD 16-bit  (Store H-L pair direct) [addr] <-- [L], [addr+1] <-- [H].
        # Three byte instruction.
        #       Copy the data of register L into the memory location with the 16-bit
        # address and the data of register H into the next memory location. No 
        # flags are modified.

        elif(p[0] == "SHLD"):
            pass

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
            pass

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
              reg['A'] = binadd(reg['A'] , reg[p[1]] ,flags)
            

        # ADI 8-bit  (Add immediate data to accumulator) [A] <-- [A] + data.
        # Two byte, Immediate addressing mode
        #       Adds the second byte of the instruction with the data in the accumulator
        # and stores the sum in the accumulator. All flags are modified reflecting the 
        # data conditions of the result in the accumulator.

        elif(p[0] == "ADI"):
            pass

        # ADC R/M  (Add register/memory with carry to accumulator). [A] <-- [A] + [r]/[[H-L]] + [CS]
        # One byte instruction.
        #       Add the data in register R or memory location M along with the bit in
        # carry flag with the data in the accumulator and store the result in the 
        # accumulator. All flags are affected.

        elif(p[0] == "ADC"):
            pass

        # ACI 8-bit  (Add with carry immediate data to accumulator). [A] <-- [A] + data + [CS].
        # Two byte instruction.
        # Add 8-bit data along with CY flag bit to the data in accumulator and store 
        # the result in accumulator. All flags are affected.

        elif(p[0] == "ACI"):
            pass

        # SUB R  (Subtract register from accumulator). [A] <-- [A] – [r].
        # One byte, Register addressing mode
        #
        # SUB M  (Subtract memory from accumulator). [A] <-- [A] – [[H-L]].
        # Indirect addressing mode    
        #       Subtract the data in a memory location whose address is present in
        # the register pair HL with the data in the accumulator and store the result 
        # in the accumulator. All flags are affected.

        elif(p[0] == "SUB"):
            pass

        # SUI 8-bit  (Subtract immediate data from accumulator) [A] <-- [A] – data.
        # Two byte, Immediate addressing mode

        elif(p[0] == "SUI"):
            pass

        # SBB R/M  (Subtract register/memory from accumulator with borrow). [A] <-- [A] – [r]/[[H-L]] – [CS].
        # One byte instruction.
        #       Subtract the data in register R or memory location M along with the bit
        # in carry flag (borrow) from the data in the accumulator and store the result 
        # in the accumulator. All flags are affected.

        elif(p[0] == "SBB"):
            pass

        # SBI 8-bit  (Subtract immediate data from accumulator with borrow). [A] <-- [A] – data – [CS].
        # Two byte instruction.

        elif(p[0] == "SBI"):
            pass

        # INR R/M, DCR R/M  ([r] <-- [r] + 1, [[H-L]] <-- [[H-L]] + 1)
        # One byte, Register/Indirect addressing mode
        # Increment/decrement the data in the register R or memory location whose address 
        # is present in register pair HL by 1. 
        # These instructions affect all flags except the Carry flag.

        elif(p[0] == "INR"):
            pass

        # INX Rp, DCX Rp  (   [rp] <-- [rp] – 1, [rp] <-- [rp] - 1)
        # One byte, Register addressing mode
        # Increment/decrement the data in the register pair Rp by 1. 
        # These instructions do not affect the flags.

        elif(p[0] == "INX"):
            pass

        # DAD Rp
        # Rp can be BC, DE, HL, or SP.
        # One byte instruction.
        # Add the specified register pair Rp data with that of HL and store the result 
        # in HL. Only CY flag is affected.

        elif(p[0] == "DAD"):
            pass




        ####################################################
        #################### 3. Logical ####################
        ####################################################

        # ANA R/M  (AND register/memory with accumulator) [A] <-- [A] ^ [r]/[[H-L]].
        # One byte instruction.
        # Logically AND the data in register R or memory location M with the data in the 
        # accumulator and store the result in the accumulator. A
        # ll flags except CY and AC are modified reflecting the data conditions of the 
        # result in the accumulator. 
        # CY flag is reset and AC flag is set. 

        elif(p[0] == "ANA"):
            pass

        # ANI 8-bit
        # Two byte instruction.
        # Logically AND the second byte of the instruction with the data in the accumulator 
        # and store the result in the accumulator. 
        # All flags except CY and AC are modified reflecting the data conditions of the 
        # result in the accumulator. 
        # CY flag is reset and AC flag is set.

        elif(p[0] == "ANI"):
            pass

        # ORA R/M
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "ORA"):
            pass

        # ORI 8-bit
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "ORI"):
            pass

        # XRA R/M
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "XRA"):
            pass

        # XRI 8-bit
        # All flags except CY and AC are modified reflecting the data conditions of the result in the accumulator. 
        # Both CY flag and AC flag are reset.

        elif(p[0] == "XRI"):
            pass

        # CMA
        # One byte instruction.
        # Complement (logical NOT) the contents of the accumulator.

        elif(p[0] == "CMA"):
            pass

        # RLC  (Rotate accumulator left) [An+1] <-- [An], [A0] <-- [A7],[CS] <-- [A7]
        # Rotate each bit in the accumulator by one position to the left with the MSB 
        # shifting to the LSB position as well as to the CY flag.

        elif(p[0] == "RLC"):
            pass

        # RAL  (Rotate accumulator left through carry) [An+1] <-- [An], [CS] <-- [A7], [A0] <-- [CS].
        # Rotate each bit in the accumulator by one position to the left with the MSB 
        # shifting to the CY flag and the CY flag bit shifting to the LSB position.

        elif(p[0] == "RAL"):
            pass

        # RRC  (Rotate accumulator right) [A7] <-- [A0], [CS] <-- [A0], [An] <-- [An+1]
        # Rotate each bit in the accumulator by one position to the right with the LSB 
        # shifting to the MSB position as well as to the CY flag.

        elif(p[0] == "RRC"):
            pass

        # RAR  (Rotate accumulator right through carry) [An] <-- [An+1], [CS] <-- [A0], [A7] <-- [CS] 
        # Rotate each bit in the accumulator by one position to the right with the LSB 
        # shifting to the CY flag and the CY flag bit shifting to the MSB position.

        elif(p[0] == "RAR"):
            pass

        # CMP R/M
        # Compare the data in register R or memory location M with the data in the 
        # accumulator for equality, greater than or less than.
        # The flags are modified according to the subtraction result of A–R/M. 
        # However, the accumulator retains its earlier value and not the difference.

        elif(p[0] == "CMP"):
            pass

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
            pass

        # CMC
        # Complement the CY flag bit. No other flag is modified.

        elif(p[0] == "CMC"):
            pass

        # STC
        # Set the CY flag. No other flag is modified.

        elif(p[0] == "STC"):
            pass

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







