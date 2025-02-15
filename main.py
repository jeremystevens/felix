from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Any, Dict
import sys

class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    INPUT = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    IDENTIFIER = auto()
    EQUALS = auto()
    STRING = auto()
    PRINT = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    GREATER = auto()
    LESS = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    EOF = auto()

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None
        self.line = 1
        self.column = 1

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def get_number(self) -> Token:
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, int(result), self.line, self.column)

    def get_identifier(self) -> Token:
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        keywords = {
            'print': TokenType.PRINT,
            'if': TokenType.IF,
            'elif': TokenType.ELIF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
            'input': TokenType.INPUT
        }

        return Token(keywords.get(result, TokenType.IDENTIFIER), result, self.line, self.column)

    def get_string(self) -> Token:
        self.advance()  # Skip opening quote
        result = ''
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()  # Skip closing quote
            return Token(TokenType.STRING, result, self.line, self.column)
        raise SyntaxError('Unterminated string literal')

    def get_next_token(self) -> Token:
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char.isalpha():
                return self.get_identifier()

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.column)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.column)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*', self.line, self.column)

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.line, self.column)

            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EQUALS, '=', self.line, self.column)

            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GREATER, '>', self.line, self.column)

            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LESS, '<', self.line, self.column)

            if self.current_char == '"':
                return self.get_string()

            raise SyntaxError(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None, self.line, self.column)

class Interpreter:
    def __init__(self):
        self.variables: Dict[str, Any] = {}

    def evaluate_expression(self, tokens: List[Token], start: int) -> tuple[Any, int]:
        if tokens[start].type == TokenType.NUMBER:
            return tokens[start].value, start + 1
        elif tokens[start].type == TokenType.IDENTIFIER:
            value = self.variables.get(tokens[start].value, 0)
            return value, start + 1
        elif tokens[start].type == TokenType.STRING:
            return tokens[start].value, start + 1

        raise SyntaxError(f"Unexpected token: {tokens[start]}")

    def evaluate_math(self, tokens: List[Token], start: int) -> tuple[Any, int]:
        left_val, pos = self.evaluate_expression(tokens, start)

        while pos < len(tokens) and tokens[pos].type in {TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE}:
            op = tokens[pos]
            right_val, new_pos = self.evaluate_expression(tokens, pos + 1)

            if op.type == TokenType.PLUS:
                left_val = left_val + right_val
            elif op.type == TokenType.MINUS:
                left_val = left_val - right_val
            elif op.type == TokenType.MULTIPLY:
                left_val = left_val * right_val
            elif op.type == TokenType.DIVIDE:
                left_val = left_val / right_val

            pos = new_pos

        return left_val, pos

    def evaluate_condition(self, tokens: List[Token], start: int) -> tuple[bool, int]:
        if tokens[start].type == TokenType.NOT:
            result, pos = self.evaluate_condition(tokens, start + 1)
            return not result, pos

        left_val, pos = self.evaluate_math(tokens, start)

        if pos >= len(tokens):
            return bool(left_val), pos

        if tokens[pos].type not in {TokenType.GREATER, TokenType.LESS, TokenType.AND, TokenType.OR}:
            return bool(left_val), pos

        op = tokens[pos]
        right_val, new_pos = None, pos

        if op.type in {TokenType.AND, TokenType.OR}:
            right_val, new_pos = self.evaluate_condition(tokens, pos + 1)
        else:
            right_val, new_pos = self.evaluate_math(tokens, pos + 1)

        if op.type == TokenType.GREATER:
            return left_val > right_val, new_pos
        elif op.type == TokenType.LESS:
            return left_val < right_val, new_pos
        elif op.type == TokenType.AND:
            return bool(left_val) and bool(right_val), new_pos
        elif op.type == TokenType.OR:
            return bool(left_val) or bool(right_val), new_pos

    def run(self, source: str):
        lexer = Lexer(source)
        tokens = []
        while True:
            token = lexer.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.type == TokenType.IDENTIFIER and i + 1 < len(tokens) and tokens[i + 1].type == TokenType.EQUALS:
                var_name = token.value
                value, new_pos = self.evaluate_math(tokens, i + 2)
                self.variables[var_name] = value
                i = new_pos
            elif token.type == TokenType.PRINT:
                value, new_pos = self.evaluate_math(tokens, i + 1)
                print(value)
                i = new_pos
            elif token.type == TokenType.INPUT:
                if i + 1 < len(tokens) and tokens[i + 1].type == TokenType.STRING:
                    prompt = tokens[i + 1].value
                    print(prompt, end='')
                    i += 2
                else:
                    i += 1
                user_input = input()
                if i < len(tokens) and tokens[i].type == TokenType.IDENTIFIER:
                    self.variables[tokens[i].value] = user_input
                    i += 1
            elif token.type in {TokenType.IF, TokenType.ELIF}:
                condition, pos = self.evaluate_condition(tokens, i + 1)
                i = pos
                if condition:
                    # Execute this block
                    while i < len(tokens) and tokens[i].type not in {TokenType.IF, TokenType.ELIF, TokenType.ELSE, TokenType.WHILE}:
                        token = tokens[i]
                        if token.type == TokenType.PRINT:
                            value, new_pos = self.evaluate_math(tokens, i + 1)
                            print(value)
                            i = new_pos
                        elif token.type == TokenType.IDENTIFIER and i + 1 < len(tokens) and tokens[i + 1].type == TokenType.EQUALS:
                            var_name = token.value
                            value, new_pos = self.evaluate_math(tokens, i + 2)
                            self.variables[var_name] = value
                            i = new_pos
                        else:
                            i += 1
                    # Skip remaining elif/else blocks
                    while i < len(tokens) and tokens[i].type in {TokenType.ELIF, TokenType.ELSE}:
                        i += 1
                        while i < len(tokens) and tokens[i].type not in {TokenType.IF, TokenType.ELIF, TokenType.ELSE, TokenType.WHILE}:
                            i += 1
                else:
                    # Skip this block and continue to next elif/else
                    while i < len(tokens) and tokens[i].type not in {TokenType.IF, TokenType.ELIF, TokenType.ELSE, TokenType.WHILE}:
                        i += 1
            elif token.type == TokenType.ELSE:
                # Execute the else block
                i += 1
                while i < len(tokens) and tokens[i].type not in {TokenType.IF, TokenType.WHILE}:
                    token = tokens[i]
                    if token.type == TokenType.PRINT:
                        value, new_pos = self.evaluate_math(tokens, i + 1)
                        print(value)
                        i = new_pos
                    elif token.type == TokenType.IDENTIFIER and i + 1 < len(tokens) and tokens[i + 1].type == TokenType.EQUALS:
                        var_name = token.value
                        value, new_pos = self.evaluate_math(tokens, i + 2)
                        self.variables[var_name] = value
                        i = new_pos
                    else:
                        i += 1
            elif token.type == TokenType.WHILE:
                loop_start = i
                while True:
                    condition, pos = self.evaluate_condition(tokens, i + 1)
                    i = pos  # Move to loop body start

                    if not condition:
                        # Skip the loop body
                        while i < len(tokens) and tokens[i].type not in {TokenType.IF, TokenType.WHILE, TokenType.EOF}:
                            i += 1
                        break  # Exit the while loop in the interpreter

                    # Execute the loop body
                    loop_body_start = i
                    while i < len(tokens) and tokens[i].type not in {TokenType.WHILE, TokenType.IF, TokenType.EOF}:
                        token = tokens[i]
                        if token.type == TokenType.PRINT:
                            value, new_pos = self.evaluate_math(tokens, i + 1)
                            print(value)
                            i = new_pos
                        elif token.type == TokenType.IDENTIFIER and i + 1 < len(tokens) and tokens[i + 1].type == TokenType.EQUALS:
                            var_name = token.value
                            value, new_pos = self.evaluate_math(tokens, i + 2)
                            self.variables[var_name] = value
                            i = new_pos
                        else:
                            i += 1

                    # Go back to check the condition again
                    i = loop_start
            else:
                i += 1

def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a file to execute")
        return
        
    try:
        with open(sys.argv[1], 'r') as file:
            source = file.read()
            interpreter = Interpreter()
            interpreter.run(source)
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()