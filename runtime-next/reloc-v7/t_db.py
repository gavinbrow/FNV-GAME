import sys
sys.argv=['x']
exec(open('fix2.py').read().split("out = {}")[0])
for body in ["ret\n db 0xe2, 0x6e", "ret\n db 0x21", "ret\n db 0x21, 0xef, 0xba", "ret\n dd 0x11223344", "ret\n db 33, 239", "ret\n db 0e2h, 06eh", "ret\n db 0x7f, 0xff, 0x21"]:
    src="__declspec(naked) void f()\n{\n __asm {\n %s\n }\n}\n"%body
    c=compile_src(src,'sp1',['/MT','/O2','/GS','/EHsc','/Gy']); print(repr(body), 'ok' if c else 'FAIL')
