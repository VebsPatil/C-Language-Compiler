from dataclasses import dataclass
from enum import Enum, auto


class TokenKind(Enum):
	INT = auto()
	IDENT = auto()
	NUMBER = auto()
	STRING = auto()
	LPAREN = auto()
	RPAREN = auto()
	LBRACE = auto()
	RBRACE = auto()
	SEMICOLON = auto()
	COMMA = auto()
	ASSIGN = auto()  # =
	PLUS = auto()
	MINUS = auto()
	STAR = auto()
	SLASH = auto()
	RETURN = auto()
	EOF = auto()


KEYWORDS = {
	"int": TokenKind.INT,
	"return": TokenKind.RETURN,
}


@dataclass
class Token:
	kind: TokenKind
	lexeme: str
	position: int

	def __repr__(self) -> str:
		return f"Token({self.kind.name}, '{self.lexeme}', pos={self.position})"


