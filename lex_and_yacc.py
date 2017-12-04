import ply.lex as lex
import ply.yacc as yacc

# List of token names.

#tokens = (
#    'NUMBER',
#   'DATA_TRANSFER',
#   'ARITHMETIC',
#   'LOGICAL',
#   'BRANCH',
#   'MACHINE',
#   'REGISTER',
#   'COMMA',
#   'COLON',
#   'LABEL'
#)

# Regular expression rules for simple tokens
#t_DATA_TRANSFER = r'MOV|MVI|LXI|LDAX|STAX|LDA|STA|LHLD|SHLD|PCHL|SPHL|XCHG|XTHL|PUSH|POP'
#t_ARITHMETIC = r'ADD|ADI|ADC|ACI|SUB|SUI|SBB|SBI|INR|DCR|INX|DCX|DAD'
#t_LOGICAL = r'ANA|ANI|ORA|ORI|XRA|XRI|CMA|RLC|RAL|RRC|RAR|CMP|CPI|CMC|STC|DAA'
#t_BRANCH = r'JMP|JC|JNC|JZ|JNZ|JP|JM|JPE|JPO|CALL|RET'
#t_NUMBER = r'\d+'
#t_COMMA = r','
#t_COLON = r':'

print("\n------LEXER START------\n")

tokens = (
   'MOV','MVI','LXI','LDAX','STAX','LDA','STA','LHLD','SHLD','PCHL','SPHL','XCHG','XTHL','PUSH','POP',
   'ADD','ADI','ADC','ACI','SUB','SUI','SBB','SBI','INR','DCR','INX','DCX','DAD',
   'ANA', 'ANI', 'ORA', 'ORI', 'XRA', 'XRI',
   'CMA', 'RLC', 'RAL', 'RRC', 'RAR', 'CMP', 'CPI', 'CMC', 'STC', 'DAA',
   'JMP','JC','JNC','JZ','JNZ','JP','JM','JPE','JPO','CALL','RET',
   'DIGIT',
   'MACHINE',
   'LABEL',
   'A','B','C','D','E','H','L','M',
   'COMMA',
   'COLON'
)

def t_MOV(t):
    r'MOV'
    return t

def t_MVI(t):
    r'MVI'
    return t

def t_LXI(t):
    r'LXI'
    return t
def t_LDAX(t):
    r'LDAX'
    return t
def t_STAX(t):
    r'STAX'
    return t
def t_LDA(t):
    r'LDA'
    return t
def t_STA(t):
    r'STA'
    return t
def t_LHLD(t):
    r'LHLD'
    return t
def t_SHLD(t):
    r'SHLD'
    return t
def t_XCHG(t):
    r'XCHG'
    return t
def t_ADD(t):
    r'ADD'
    return t
def t_ADI(t):
    r'ADI'
    return t
def t_ADC(t):
    r'ADC'
    return t
def t_ACI(t):
    r'ACI'
    return t
def t_SUB(t):
    r'SUB'
    return t
def t_SUI(t):
    r'SUI'
    return t
def t_SBB(t):
    r'SBB'
    return t
def t_SBI(t):
    r'SBI'
    return t
def t_INR(t):
    r'INR'
    return t
def t_DCR(t):
    r'DCR'
    return t
def t_INX(t):
    r'INX'
    return t
def t_DCX(t):
    r'DCX'
    return t
def t_DAD(t):
    r'DAD'
    return t
def t_ANA(t):
    r'ANA'
    return t
def t_ANI(t):
    r'ANI'
    return t
def t_ORA(t):
    r'ORA'
    return t
def t_ORI(t):
    r'ORI'
    return t
def t_XRA(t):
    r'XRA'
    return t
def t_XRI(t):
    r'XRI'
    return t
def t_CMA(t):
    r'CMA'
    return t
def t_RLC(t):
    r'RLC'
    return t
def t_RAL(t):
    r'RAL'
    return t
def t_RRC(t):
    r'RRC'
    return t
def t_RAR(t):
    r'RAR'
    return t
def t_CMP(t):
    r'CMP'
    return t
def t_CPI(t):
    r'CPI'
    return t
def t_CMC(t):
    r'CMC'
    return t
def t_STC(t):
    r'STC'
    return t
def t_DAA(t):
    r'DAA'
    return t
def t_JMP(t):
    r'JMP'
    return t
def t_JC(t):
    r'JC'
    return t
def t_JNC(t):
    r'JNC'
    return t
def t_JZ(t):
    r'JZ'
    return t
def t_JNZ(t):
    r'JNZ'
    return t
def t_JM(t):
    r'JM'
    return t
def t_JP(t):
    r'JP'
    return t
def t_JPE(t):
    r'JPE'
    return t
def t_JPO(t):
    r'JPO'
    return t
def t_CALL(t):
    r'CALL'
    return t
def t_RET(t):
    r'RET'
    return t
def t_COMMA(t):
    r','
    return t
def t_COLON(t):
    r':'
    return t

def t_DIGIT(t):
    r'\d'
    return t

def t_MACHINE(t):
    r'HLT|NOP'
    return t

def t_LABEL(t):
    r'[A-Z][A-Z]+'
    return t

def t_A(t):
    r'A'
    return t

def t_B(t):
    r'B'
    return t

def t_C(t):
    r'C'
    return t

def t_D(t):
    r'D'
    return t

def t_E(t):
    r'E'
    return t

def t_H(t):
    r'H'
    return t

def t_M(t):
    r'M'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'//.*'
    pass
    # No return value. Token discarded

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

literals = {'F'}

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

input_file = input("Enter file name : ")
fp = open("Example programs/" + input_file + ".txt", "r")   
data = fp.read()
fp.close()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
print("")

print("\n------LEXER ENDS------\n")

print("\n------PARSING START------\n")

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
              | hex DIGIT
              | DIGIT hex
       
       byte_16 : DIGIT DIGIT DIGIT DIGIT
               | hex DIGIT DIGIT DIGIT
               | DIGIT hex DIGIT DIGIT
               | DIGIT DIGIT hex DIGIT
               | DIGIT DIGIT DIGIT hex
      
       hex : 'A'
           | 'B'
           | 'C'
           | 'D'
           | 'E'
           | 'F'
    '''

# Error rule for syntax errors
def p_error(p):
    print(p)
    print("\n--------Syntax error in input----------")

# Build the parser
parser = yacc.yacc()

while True:
    result = parser.parse(data)
    if not result:
        break
    print(result)

print("\n------PARSING ENDS------\n")
