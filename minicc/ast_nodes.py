from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


# Expressions
@dataclass
class Expr:
	pass


@dataclass
class Number(Expr):
	value: int


@dataclass
class Name(Expr):
	ident: str


@dataclass
class String(Expr):
	value: str


@dataclass
class Binary(Expr):
	left: Expr
	op: str
	right: Expr


@dataclass
class Call(Expr):
	func: str
	args: List[Expr]


# Statements
@dataclass
class Stmt:
	pass


@dataclass
class VarDecl(Stmt):
	name: str
	init: Optional[Expr]


@dataclass
class Assign(Stmt):
	name: str
	value: Expr


@dataclass
class Return(Stmt):
	value: Optional[Expr]


@dataclass
class ExprStmt(Stmt):
	expr: Expr


@dataclass
class Function:
	name: str
	body: List[Stmt]


@dataclass
class Program:
	functions: List[Function]


