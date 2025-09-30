from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from .lexer import Lexer
from .parser import Parser
from .codegen import CodeGen


def compile_to_python(input_path: Path, output_path: Path) -> None:
	source = input_path.read_text(encoding="utf-8")
	tokens = Lexer(source).lex()
	program = Parser(tokens).parse()
	py_code = CodeGen().generate(program)
	output_path.parent.mkdir(parents=True, exist_ok=True)
	output_path.write_text(py_code, encoding="utf-8")


def run_c_file(input_path: Path) -> int:
	build_dir = Path("build")
	build_dir.mkdir(exist_ok=True)
	py_out = build_dir / (input_path.stem + ".py")
	compile_to_python(input_path, py_out)
	proc = subprocess.run([sys.executable, str(py_out)])
	return proc.returncode


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(prog="minicc")
	sub = parser.add_subparsers(dest="cmd", required=True)

	compile_p = sub.add_parser("compile", help="compile .c to .py")
	compile_p.add_argument("input", type=Path)
	compile_p.add_argument("-o", "--output", type=Path, required=True)

	run_p = sub.add_parser("run", help="compile then run")
	run_p.add_argument("input", type=Path)

	args = parser.parse_args(argv)

	if args.cmd == "compile":
		compile_to_python(args.input, args.output)
		return 0
	if args.cmd == "run":
		return run_c_file(args.input)
	return 0


if __name__ == "__main__":
	sys.exit(main())


