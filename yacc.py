import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens

def p_LXI(p):
    '''statements : statement statements
                  | statement

       statement : MOV register COMMA register
                 | MOV register COMMA memory
                 | MOV memory COMMA register
                 | LABEL COLON MOV register COMMA register
                 | LABEL COLON MOV register COMMA memory
                 | LABEL COLON MOV memory COMMA register
       statement : MVI register COMMA byte_8
                 | MVI memory COMMA byte_8
                 | LABEL COLON MVI register COMMA byte_8
                 | LABEL COLON MVI memory COMMA byte_8
       statement : LXI register_pair_3 COMMA byte_16
                 | LABEL COLON LXI register_pair_3 COMMA byte_16
       statement : LDAX register_pair_2
                 | LABEL COLON LDAX register_pair_2
       statement : STAX register_pair_2
                 | LABEL COLON STAX register_pair_2
       statement : LDA byte_16
                 | LABEL COLON LDA byte_16
       statement : STA byte_16
                 | LABEL COLON STA byte_16
       statement : LHLD byte_16
                 | LABEL COLON LHLD byte_16
       statement : SHLD byte_16
                 | LABEL COLON SHLD byte_16
       statement : XCHG
                 | LABEL COLON XCHG
       statement : ADD register
                 | ADD memory
                 | LABEL COLON ADD register
                 | LABEL COLON ADD memory
       statement : ADI byte_8
                 | LABEL COLON ADI byte_8
       statement : ADC register
                 | ADC memory
                 | LABEL COLON ADC register
                 | LABEL COLON ADC memory
       statement : ACI byte_8
                 | LABEL COLON ACI byte_8
       statement : SUB register
                 | SUB memory
                 | LABEL COLON SUB register
                 | LABEL COLON SUB memory
       statement : SUI byte_8
                 | LABEL COLON SUI byte_8
       statement : SBB register
                 | SBB memory
                 | LABEL COLON SBB register
                 | LABEL COLON SBB memory
       statement : SBI byte_8
                 | LABEL COLON SBI byte_8
       statement : INR register
                 | INR memory
                 | LABEL COLON INR register
                 | LABEL COLON INR memory
       statement : DCR register
                 | DCR memory
                 | LABEL COLON DCR register
                 | LABEL COLON DCR memory
       statement : INX register_pair_3
                 | LABEL COLON INX register_pair_3
       statement : DCX register_pair_3
                 | LABEL COLON DCX register_pair_3
       statement : DAD register_pair_3
                 | LABEL COLON DAD register_pair_3
       statement : ANA register
                 | ANA memory
                 | LABEL COLON ANA register
                 | LABEL COLON ANA memory
       statement : ORA register
                 | ORA memory
                 | LABEL COLON ORA register
                 | LABEL COLON ORA memory
       statement : XRA register
                 | XRA memory
                 | LABEL COLON XRA register
                 | LABEL COLON XRA memory
       statement : ANI byte_8
                 | LABEL COLON ANI byte_8
       statement : ORI byte_8
                 | LABEL COLON ORI byte_8
       statement : XRI byte_8
                 | LABEL COLON XRI byte_8
       statement : CMA
                 | LABEL COLON CMA
       statement : RLC
                 | LABEL COLON RLC
       statement : RAL
                 | LABEL COLON RAL
       statement : RRC
                 | LABEL COLON RRC
       statement : RAR
                 | LABEL COLON RAR
       statement : CMP register
                 | CMP memory
                 | LABEL COLON CMP register
                 | LABEL COLON CMP memory
       statement : CPI byte_8
                 | LABEL COLON CPI byte_8
       statement : CMC
                 | LABEL COLON CMC
       statement : STC
                 | LABEL COLON STC
       statement : DAA
                 | LABEL COLON DAA
       statement : JMP byte_16
                 | JMP LABEL
                 | LABEL COLON JMP byte_16
                 | LABEL COLON JMP LABEL
       statement : JC byte_16
                 | JC LABEL
                 | LABEL COLON JC byte_16
                 | LABEL COLON JC LABEL
       statement : JNC byte_16
                 | JNC LABEL
                 | LABEL COLON JNC byte_16
                 | LABEL COLON JNC LABEL
       statement : JZ byte_16
                 | JZ LABEL
                 | LABEL COLON JZ byte_16
                 | LABEL COLON JZ LABEL
       statement : JNZ byte_16
                 | JNZ LABEL
                 | LABEL COLON JNZ byte_16
                 | LABEL COLON JNZ LABEL
       statement : JP byte_16
                 | JP LABEL
                 | LABEL COLON JP byte_16
                 | LABEL COLON JP LABEL
       statement : JM byte_16
                 | JM LABEL
                 | LABEL COLON JM byte_16
                 | LABEL COLON JM LABEL
       statement : JPE byte_16
                 | JPE LABEL
                 | LABEL COLON JPE byte_16
                 | LABEL COLON JPE LABEL
       statement : JPO byte_16
                 | JPO LABEL
                 | LABEL COLON JPO byte_16
                 | LABEL COLON JPO LABEL
       statement : CALL byte_16
                 | CALL LABEL
                 | LABEL COLON CALL byte_16
                 | LABEL COLON CALL LABEL
       statement : RET
                 | LABEL COLON RET
       statement : MACHINE
                 | LABEL COLON MACHINE
       
       register : A
                | B
                | C
                | D
                | E
                | H
                | L
       
       memory : M
       
       register_pair_2 : B
                       | D
       
       register_pair_3 : B
                       | D
                       | H
       
       byte_8 : DIGIT DIGIT
       
       byte_16 : DIGIT DIGIT DIGIT DIGIT
    '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

input_file = input("Enter file name : ")
fp = open("Example programs/" + input_file + ".txt", "r")   
data = fp.read()
fp.close()

while True:
    result = parser.parse(data)
    if not result:
        break
    print(result)