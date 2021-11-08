#Created by Nathan Heckman
import re

#Example Java program shown below for demonstration purposes.
data = ''' 
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
} 
'''

#Tokens derived from requirements detailed in assignment directions.
tokens = re.compile(r'''
  (\s+) |                      # whitespace
  (//)[^\n]* |                 # single-line comments
  (\d*)\.\d+f? |               # float literals
  (\d+) |                      # integer literals
  ([][(){}<>=,;:*+-/]) |     # special
  ([A-Za-z_][A-Za-z0-9_]*) |   # identifiers
  "((?:[^"\n\\]|\\.)*)" |      # string literal
  (.)                          # error
''', re.DOTALL | re.VERBOSE)
#DOTALL allows for whitespace/newlines in token set to be ignored
#VERBOSE allows for greater token set readability

for match in re.finditer(tokens, data):     #for all matches in data...
    space, comment, _float, integer, \
    punct, identifier, stringlit, \
    badchar = match.groups()                #group together matches based on token set
    if space:
        continue                            #can be ignored since whitespace only used for readability in Java
    elif comment:
        print(match.group(), "--> COMMENT") #for remaining groups, print match and description based on what it is
    elif integer:
        print(match.group(), "--> INTEGER LITERAL")
    elif _float:
        print(match.group(), "--> FLOAT LITERAL")
    elif punct:
        if match.group() == "(":
            print(match.group(), "--> LEFT PARENTHESIS")
        if match.group() == ")":
            print(match.group(), "--> RIGHT PARENTHESIS")
        if match.group() == "[":
            print(match.group(), "--> LEFT BRACKET")
        if match.group() == "]":
            print(match.group(), "--> RIGHT BRACKET")
        if match.group() == "+":
            print(match.group(), "--> ADDITION")
        if match.group() == "-":
            print(match.group(), "--> SUBTRACTION")
        if match.group() == "*":
            print(match.group(), "--> MULTIPLICATION")
        if match.group() == "/":
            print(match.group(), "--> DIVISION")
        if match.group() == "<":
            print(match.group(), "--> LEFT WEDGE")
        if match.group() == ">":
            print(match.group(), "--> RIGHT WEDGE")
        if match.group() == "=":
            print(match.group(), "--> EQUALS SIGN")
        if match.group() == ":":
            print(match.group(), "--> COLON")
        if match.group() == ";":
            print(match.group(), "--> SEMICOLON")
        if match.group() == "{":
            print(match.group(), "--> LEFT BRACE")
        if match.group() == "}":
            print(match.group(), "--> RIGHT BRACE")
    elif identifier:
        if match.group() == "public" or match.group() == "class" or match.group() == "void" or match.group() == "String" or match.group() == "static":
            print(match.group(), "--> SYSTEM IDENTIFIER")
        else:
            print(match.group(), "--> IDENTIFIER")
    elif stringlit:
        print(match.group(), "--> STRING LITERAL")
    elif badchar:
        print("TOKEN NOT FOUND")    #would throw exception or error here