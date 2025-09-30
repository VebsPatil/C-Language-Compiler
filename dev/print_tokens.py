from pathlib import Path
from minicc.lexer import Lexer

src = Path('examples/hello.c').read_text(encoding='utf-8')
print(src)
print('--- TOKENS ---')
for t in Lexer(src).lex():
	print(t)


