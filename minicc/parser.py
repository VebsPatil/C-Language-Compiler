from __future__ import annotations

from typing import List, Optional

from .tokens import Token, TokenKind
from .ast_nodes import Program, Function, Stmt, VarDecl, Assign, Return, ExprStmt, Expr, Number, Name, Binary, Call, String


class Parser:
	def __init__(self, tokens: List[Token]) -> None:
		self.tokens = tokens
		self.index = 0

	def parse(self) -> Program:
		functions: List[Function] = []
		while not self._match(TokenKind.EOF):
			functions.append(self._function())
		return Program(functions)

	def _function(self) -> Function:
		self._consume(TokenKind.INT, "expected 'int' at function start")
		name = self._consume(TokenKind.IDENT, "expected function name").lexeme
		self._consume(TokenKind.LPAREN, "expected '('")
		self._consume(TokenKind.RPAREN, "expected ')'")
		self._consume(TokenKind.LBRACE, "expected '{'")
		body: List[Stmt] = []
		while not self._check(TokenKind.RBRACE):
			body.append(self._statement())
		self._consume(TokenKind.RBRACE, "expected '}' at end of function body")
		return Function(name=name, body=body)

	def _statement(self) -> Stmt:
		if self._match(TokenKind.INT):
			name_tok = self._consume(TokenKind.IDENT, "expected variable name")
			init: Optional[Expr] = None
			if self._match(TokenKind.ASSIGN):
				init = self._expression()
			self._consume(TokenKind.SEMICOLON, "expected ';' after declaration")
			return VarDecl(name=name_tok.lexeme, init=init)
		if self._match(TokenKind.RETURN):
			value: Optional[Expr] = None
			if not self._check(TokenKind.SEMICOLON):
				value = self._expression()
			self._consume(TokenKind.SEMICOLON, "expected ';' after return")
			return Return(value=value)
		# assignment or expr stmt
		if self._check(TokenKind.IDENT) and self._check_next(TokenKind.ASSIGN):
			name = self._advance().lexeme
			self._consume(TokenKind.ASSIGN, "expected '=' in assignment")
			value = self._expression()
			self._consume(TokenKind.SEMICOLON, "expected ';' after assignment")
			return Assign(name=name, value=value)
		expr = self._expression()
		self._consume(TokenKind.SEMICOLON, "expected ';' after expression")
		return ExprStmt(expr=expr)

	def _expression(self) -> Expr:
		return self._additive()

	def _additive(self) -> Expr:
		expr = self._multiplicative()
		while self._match(TokenKind.PLUS) or self._match(TokenKind.MINUS):
			op_tok = self._previous()
			right = self._multiplicative()
			expr = Binary(left=expr, op=op_tok.lexeme, right=right)
		return expr

	def _multiplicative(self) -> Expr:
		expr = self._unary()
		while self._match(TokenKind.STAR) or self._match(TokenKind.SLASH):
			op_tok = self._previous()
			right = self._unary()
			expr = Binary(left=expr, op=op_tok.lexeme, right=right)
		return expr

	def _unary(self) -> Expr:
		# No unary operators for simplicity; extend here if needed
		return self._primary()

	def _primary(self) -> Expr:
		if self._match(TokenKind.NUMBER):
			value = int(self._previous().lexeme)
			return Number(value=value)
		if self._match(TokenKind.STRING):
			return String(value=self._previous().lexeme)
		if self._match(TokenKind.IDENT):
			name_tok = self._previous()
			# function call?
			if self._match(TokenKind.LPAREN):
				args: List[Expr] = []
				if not self._check(TokenKind.RPAREN):
					args.append(self._expression())
					while self._match(TokenKind.COMMA):
						args.append(self._expression())
				self._consume(TokenKind.RPAREN, "expected ')' after arguments")
				return Call(func=name_tok.lexeme, args=args)
			return Name(ident=name_tok.lexeme)
		if self._match(TokenKind.LPAREN):
			expr = self._expression()
			self._consume(TokenKind.RPAREN, "expected ')'")
			return expr
		raise SyntaxError("expected expression")

	# helpers
	def _match(self, *kinds: TokenKind) -> bool:
		for k in kinds:
			if self._check(k):
				self._advance()
				return True
		return False

	def _check(self, kind: TokenKind) -> bool:
		# Allow checking EOF explicitly; do not preempt with _is_at_end()
		return self._peek().kind == kind

	def _check_next(self, kind: TokenKind) -> bool:
		if self._is_at_end():
			return False
		if self.index + 1 >= len(self.tokens):
			return False
		return self.tokens[self.index + 1].kind == kind

	def _consume(self, kind: TokenKind, message: str) -> Token:
		if self._check(kind):
			return self._advance()
		raise SyntaxError(f"{message} at token {self._peek()}")

	def _advance(self) -> Token:
		self.index += 1
		return self.tokens[self.index - 1]

	def _previous(self) -> Token:
		return self.tokens[self.index - 1]

	def _peek(self) -> Token:
		return self.tokens[self.index]

	def _is_at_end(self) -> bool:
		return self._peek().kind == TokenKind.EOF


