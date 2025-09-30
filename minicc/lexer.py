from __future__ import annotations

from typing import List

from .tokens import Token, TokenKind, KEYWORDS


class Lexer:
	def __init__(self, source: str) -> None:
		self.source = source
		self.length = len(source)
		self.index = 0

	def lex(self) -> List[Token]:
		tokens: List[Token] = []
		while True:
			self._skip_whitespace_and_comments()
			if self._is_eof():
				tokens.append(Token(TokenKind.EOF, "", self.index))
				break
			ch = self._peek()
			start = self.index

			if ch.isalpha() or ch == "_":
				ident = self._consume_identifier()
				kind = KEYWORDS.get(ident, TokenKind.IDENT)
				tokens.append(Token(kind, ident, start))
				continue

			if ch.isdigit():
				num = self._consume_number()
				tokens.append(Token(TokenKind.NUMBER, num, start))
				continue

			if ch == '"':
				string = self._consume_string()
				tokens.append(Token(TokenKind.STRING, string, start))
				continue

			# single-char tokens
			self._advance()
			if ch == "(":
				tokens.append(Token(TokenKind.LPAREN, ch, start))
			elif ch == ")":
				tokens.append(Token(TokenKind.RPAREN, ch, start))
			elif ch == "{":
				tokens.append(Token(TokenKind.LBRACE, ch, start))
			elif ch == "}":
				tokens.append(Token(TokenKind.RBRACE, ch, start))
			elif ch == ";":
				tokens.append(Token(TokenKind.SEMICOLON, ch, start))
			elif ch == ",":
				tokens.append(Token(TokenKind.COMMA, ch, start))
			elif ch == "=":
				tokens.append(Token(TokenKind.ASSIGN, ch, start))
			elif ch == "+":
				tokens.append(Token(TokenKind.PLUS, ch, start))
			elif ch == "-":
				tokens.append(Token(TokenKind.MINUS, ch, start))
			elif ch == "*":
				tokens.append(Token(TokenKind.STAR, ch, start))
			elif ch == "/":
				tokens.append(Token(TokenKind.SLASH, ch, start))
			else:
				raise SyntaxError(f"Unexpected character '{ch}' at {start}")

		return tokens

	def _skip_whitespace_and_comments(self) -> None:
		while not self._is_eof():
			ch = self._peek()
			if ch in " \t\r\n":
				self._advance()
				continue
			# preprocessor directive like #include ... -> skip entire line
			if ch == "#":
				while not self._is_eof() and self._peek() != "\n":
					self._advance()
				continue
			# // comment
			if ch == "/" and self._peek_next() == "/":
				self._advance(); self._advance()
				while not self._is_eof() and self._peek() != "\n":
					self._advance()
				continue
			break

	def _consume_identifier(self) -> str:
		start = self.index
		while not self._is_eof() and (self._peek().isalnum() or self._peek() == "_"):
			self._advance()
		return self.source[start:self.index]

	def _consume_number(self) -> str:
		start = self.index
		while not self._is_eof() and self._peek().isdigit():
			self._advance()
		return self.source[start:self.index]

	def _consume_string(self) -> str:
		# assumes current char is '"'
		self._advance()  # skip opening quote
		chars: list[str] = []
		while not self._is_eof():
			ch = self._peek()
			if ch == '"':
				self._advance()
				break
			if ch == "\\":
				self._advance()
				esc = self._peek()
				mapping = { 'n': "\n", 't': "\t", '"': '"', "\\": "\\" }
				chars.append(mapping.get(esc, esc))
				self._advance()
				continue
			chars.append(ch)
			self._advance()
		return "".join(chars)

	def _peek(self) -> str:
		return self.source[self.index]

	def _peek_next(self) -> str:
		if self.index + 1 >= self.length:
			return "\0"
		return self.source[self.index + 1]

	def _advance(self) -> None:
		self.index += 1

	def _is_eof(self) -> bool:
		return self.index >= self.length


