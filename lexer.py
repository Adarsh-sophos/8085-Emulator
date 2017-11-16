import ply.lex as lex

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