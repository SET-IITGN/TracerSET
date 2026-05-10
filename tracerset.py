import ast
import sys
import tokenize
import os
import platform

COLOR = "\033[93m"
RESET = "\033[0m"

def getch():
	#press enter key...
    sys.stdin.read(1) 

try:
	fp=open(sys.argv[1],'r')
	buff=fp.read()
	fp.close()
	
	#generate AST	
	parsed=ast.parse(buff)
	dump=ast.dump(parsed,indent=2)
	
	#display source code (raw)
	print("[Source Code]:")
	print("==============")
	print(buff)
	
	#display stream of tokens
	print(f"{COLOR}Press Enter key to continue to [Tokens]{RESET}")
	getch()
	print("[Tokens]:")
	print("=========")
	with tokenize.open(sys.argv[1]) as f:
		tokens = tokenize.generate_tokens(f.readline)
		for token in tokens:
			print(token)
		f.close()
	'''
	#display AST (indent as hierarchy)
	print(f"\n{COLOR}Press Enter key to continue to [Syntax]{RESET}")
	getch()
	print("[Syntax]:")
	print("=========")
	print(dump)
	'''
	#display CST
	print(f"\n{COLOR}Press Enter key to continue to [Concrete Syntax]{RESET}")
	getch()
	print("[Concrete Syntax]:")
	print("==================")
	os.system(f"python{'.'.join(platform.python_version().split('.')[:2])} utilities/cst2dot.py {sys.argv[1]}")
	
	#display AST
	print(f"\n{COLOR}Press Enter key to continue to [Abstract Syntax]{RESET}")
	getch()
	print("[Abstract Syntax]:")
	print("==================")
	os.system(f"python{'.'.join(platform.python_version().split('.')[:2])} utilities/ast2dot.py {sys.argv[1]}")
	
	#display disassembled output of the source code 
	print(f"\n{COLOR}Press Enter key to continue to [Disassembly]{RESET}")
	getch()
	print("[Disassembly]:")
	print("============")
	mid_cmd="-m dis"
	os.system(f"python{'.'.join(platform.python_version().split('.')[:2])} {mid_cmd} {sys.argv[1]}")
	
	#display execution trace (end-to-end)
	print(f"\n{COLOR}Press Enter key to continue to [Execution Trace]{RESET}")
	getch()
	print("[Execution Trace]:")
	print("==================")
	mid_cmd="-m trace --count --trace --missing --summary"
	os.system(f"python{'.'.join(platform.python_version().split('.')[:2])} {mid_cmd} {sys.argv[1]}")
	
	#display execution trace (step-by-step)
	print(f"\n{COLOR}Press Enter key to continue to [Step-by-step Execution Trace]{RESET}")
	getch()
	os.system(f"python{'.'.join(platform.python_version().split('.')[:2])} utilities/detailed.py {sys.argv[1]}")
	
except OSError as ex:
	#file not found
	print(f"{ex.filename}: {ex.strerror}")
except SyntaxError as ex:
	#syntax error handling (fail-fast)
	print(f"In File \"{sys.argv[1]}\", line {ex.lineno}\n{ex.text}\n{ex.__class__.__name__}: {ex.msg}")
