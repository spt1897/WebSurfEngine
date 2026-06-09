#exceptions during tokenization
class InvalidSyntax(Exception):
    pass

class EmptyLine(InvalidSyntax):
     pass

class Unclosed_Double_Quotes(InvalidSyntax):
    pass

class Unclosed_Single_Quotes(InvalidSyntax):
    pass



def tokenize(line:str) -> list[str]:
    words = []
    word = ""
    inside_double_quotes =False
    inside_single_quotes =False
    for char in line+" ":    
       
        if char == '"' and not inside_single_quotes:
                inside_double_quotes = not inside_double_quotes

        elif char == '\'' and not inside_double_quotes:
                inside_single_quotes = not inside_single_quotes

        elif char == ' ' and not inside_single_quotes and not inside_double_quotes:
            if word:
                words.append(word)
                word=""
        
        else:
            word+=char
    
    if inside_double_quotes:
        raise Unclosed_Double_Quotes()
    
    if inside_single_quotes:
        raise Unclosed_Single_Quotes()
    
    if not words:
         raise EmptyLine()
    
    return words
