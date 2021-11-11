#Created by Nathan Heckman

#import regex and string matching module
import re             

#Simple Token object. Token type, value, and position
class Token(object):    
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos
        
    #define regulated print format for object
    def __str__(self):  
        return '%s(%s) at %s' % (self.type, self.val, self.pos)

#Define error handling in case no tokens are matched
class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos
        
#Define lexical analysis object and 
class Lexer(object):
    #Rules is essentially a regex and type pair. Type describes the token defined by the regex
    #Whitespace is skipped so errors can be avoided. Whitespace is also not necessary in Java.
    def __init__(self, rules, skip_whitespace=True):
        self.rules = []
        
        #add each element to the rules array
        for regex, type in rules:
            self.rules.append((re.compile(regex), type))
            
        self.skip_whitespace = skip_whitespace
        
        #Define a regex whitespace
        self.re_ws_skip = re.compile('\S')
    
    #Initialize lexer with buffer input
    def input(self, buf):
        self.buf = buf
        self.pos = 0

    #Return next token object found in the input. Error handling included
    def token(self):
        
        #Check for empty input string
        if self.pos >= len(self.buf):
            return None
            
        #Function to skip the whitespace present in the input string
        if self.skip_whitespace:
            m = self.re_ws_skip.search(self.buf, self.pos)
            if m:
                self.pos = m.start()
            #If only whitespace, return None
            else:
                return None
                
        #Create tokens for found regex matches in the input string, return the token if found
        for regex, type in self.rules:
            m = regex.match(self.buf, self.pos)
            if m:
                token = Token(type, m.group(), self.pos)
                self.pos = m.end()
                return token

        #If none of the above works, error
        raise LexerError(self.pos)

    def tokens(self):
        #Returns an iterator to the tokens found in the input. Allows token list to be created
        while 1:
            token = self.token()
            if token is None: break
            yield token

#Java defined regex rules
rules = [
    ('//[^\n]*',                          'SINGLE LINE COMMENT'),
    ('(\d*)\.\d+f?',                      'FLOAT LITERAL'),
    ('"[^\n]*"',                          'STRING LITERAL'),
    ('if',                                'IF STATEMENT'),
    ('else',                              'ELSE STATEMENT'),
    ('while',                             'WHILE LOOP'),
    ('do',                                'DO STATEMENT'),
    ('switch',                            'SWITCH STATEMENT'),
    ('for',                               'FOR LOOP'),
    ('\d+',                               'INTEGER LITERAL'),
    ('[a-zA-Z_]\w*',                      'IDENTIFIER'),
    ('\+\+',                              'INCREMENT'),
    ('\-\-',                              'DECREMENT'),
    ('\+',                                'PLUS'),
    ('\-',                                'MINUS'),
    ('\*',                                'MULTIPLY'),
    ('\/',                                'DIVIDE'),
    ('\(',                                'LEFT PARENTHESIS'),
    ('\)',                                'RIGHT PARENTHESIS'),
    ('\{',                                'LEFT CURLY'),
    ('\}',                                'RIGHT CURLY'),
    ('\[',                                'LEFT BRACKET'),
    ('\]',                                'RIGHT BRACKET'),
    ('<',                                 'LEFT WEDGE'),
    ('>',                                 'LEFT WEDGE'),
    (',',                                 'COMMA'),
    (';',                                 'SEMICOLON'),
    ('\.',                                'PERIOD'),
    ('=',                                 'EQUALS'),
    ('.',                                 'ERROR')  #if code gets here, the input is unknown. End analysis
]
#Create lexer object
lexer = Lexer(rules, skip_whitespace=True)

#run lexical analysis on input string
lexer.input('''
public class add { //add two numbers
    public static void main(String[] args){
        int num1 = 5, num2 = 15, sum;
        sum = num1 + num2;
        System.out.println("Sum of these 2 numbers: " + sum);
        String fourty = "40";
        float f = 10.4f;
        int i = 100;
    }
    public void nothing(){
        //do nothing
    }
    for(int i = 0; i < 4; i++){
        i++;
    }
    if(x < 0){
        //nothing
    }
    else{
        //nothing
    }
    do{
        //nothing
    } while(x = 0){
        //nothing
        switch(x){
            //nothing
        }
    }
} 
''')
tokens = []                                         #Array to store the computed tokens
try:
    for token in lexer.tokens():                    #Add each token to list and print with object format
        tokens.append(token.type)
        print(token)
except LexerError as error:
    print('Error at position %s' % error.pos)       #Error checking

print()
print(tokens)                                       #Print token list. Used to compute RDA and EBNF for other questions

# Question 1 code is above. Question 2 and 3 begin below and follow Java convention

# <selection_statement> --> if '(' <expression> ')' <statement> [ else <statement> ]
# <while_loop> --> while '(' <expression> ')' <statement>
# <for_loop> --> for '(' <expression> ';' <expression> ';' <expression> ')' <statement>
# <block> --> '{' {<statement>} '}'

index = 0
nextToken = tokens[index]                   #Start analysis at beginning of token list

def selection_statement():
    if(nextToken != 'IF STATEMENT'):
        error()                                 #End analysis and error out
    else:
        index += 1                              #Process out next token and grab token after it
        expression()
        if(nextToken != 'RIGHT PARENTHESIS'):
            error()                             #End analysis and error out
        else:
            index += 1                          #Process out next token and grab token after it
            statement()
            if(nextToken == 'ELSE STATEMENT'):  #No error if else isn't present
                index += 1
                statement()
    print('Success')
def while_loop():
    if(nextToken != 'WHILE LOOP'):
        error()                                 #End analysis and error out
    else:
        index += 1                              #Process out next token and grab token after it
        if(nextToken != 'LEFT PARENTHESIS'):
            error()                             #End analysis and error out
        else:
            index += 1                          #Process out next token and grab token after it
            expression()
            if(nextToken != 'RIGHT PARENTHESIS'):  #No error if else isn't present
                error()
            else:
                index += 1
                statement()
    print('Success')
def for_loop():
    if(nextToken != 'FOR LOOP'):
        error()                                 #End analysis and error out
    else:
        index += 1                              #Process out next token and grab token after it
        if(nextToken != 'LEFT PARENTHESIS'):
            error()                             #End analysis and error out
        else:
            index += 1                          #Process out next token and grab token after it
            expression()
            if(nextToken != 'SEMICOLON'):       #No error if else isn't present
                error()
            else:
                index += 1
                expression()
                if(nextToken != 'SEMICOLON'):
                    error()
                else:
                    index += 1
                    expression()
                    if(nextToken != 'RIGHT PARENTHESIS'):
                        error()
                    else:
                        index += 1
                        statement()
    print('Success')
def statement():
    if(nextToken == 'IF STATEMENT'):
        selection_statement()
    if(nextToken == 'WHILE LOOP'):
        selection_statement()
    if(nextToken == 'FOR LOOP'):
        for_loop()
    #More are possible but this demonstrates the use
def expression():
    x = 0   #Ignore this
    #This is where expression checking would go. Not required for assignment
def error():
    x = 0   #Ignore this
    #This is where error reporting would go
