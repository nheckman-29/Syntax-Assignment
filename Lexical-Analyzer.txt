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
    ('\d+',                              'NUMBER'),
    ('.*for\s*(.*;.*;.*){.*}',           'FOR LOOP'),   #CHECK REGEX FOR THIS, ADD THE OTHERS
    ('[a-zA-Z_]\w*',                     'IDENTIFIER'),
    ('\+',                               'PLUS'),
    ('\-',                               'MINUS'),
    ('\*',                               'MULTIPLY'),
    ('\/',                               'DIVIDE'),
    ('\(',                               'LEFT PARENTHESIS'),
    ('\)',                               'RIGHT PARENTHESIS'),
    ('=',                                'EQUALS'),
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
        
        float f = 10.4f;
        int i = 100;
    }
    public void nothing(){
        //do nothing
    }
    for(int i = 0; i < 4; i++){
        i++
    }
} 
''')
try:
    for token in lexer.tokens():
        print(token)
except LexerError as error:
    print('Error at position %s' % error.pos)