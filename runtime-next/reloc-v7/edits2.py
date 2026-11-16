import re, shutil, os
S = 'C:/Projects/Decompilation/fnv_decomp/src/'
def rd(f):
    b = open(S + f, 'rb').read().decode('latin1'); return b, ('\r\n' if '\r\n' in b else '\n')
def wr(f, b):
    if not os.path.exists(S + f + '.bak-20261116-wB'): shutil.copy(S + f, S + f + '.bak-20261116-wB')
    open(S + f, 'wb').write(b.encode('latin1'))
def sub(f, old, new, n=1):
    b, nl = rd(f); old = old.replace('\n', nl); new = new.replace('\n', nl)
    assert b.count(old) == n, (f, old[:50], b.count(old)); wr(f, b.replace(old, new)); print('ok', f, old[:40].strip())
def before_fnv(f, line, text):
    b, nl = rd(f); L = b.split(nl); j = line - 1
    while j > 0 and not L[j].startswith('// @fnv'): j -= 1
    while j > 0 and L[j - 1].startswith('//'): j -= 1
    L[j:j] = text.split('\n'); wr(f, nl.join(L)); print('ok', f, 'decl before', j + 1)
# C: IsFlag80Set
sub('fallout_shared/tesobjectcell.cpp', 'bool __fastcall IsFlag80Set(void* pThis);', 'struct FUN_0050d210_Class\n{\n    bool IsFlag80Set() const;\n};')
sub('fallout_shared/tesobjectcell.cpp', '!IsFlag80Set(pThis)', '!((FUN_0050d210_Class*)pThis)->IsFlag80Set()')
# F: QuestStage::MarkDone(bool) -> FUN_0067fdb0
sub('fallout_shared/tesquest.cpp', 'stage->MarkDone(false);', '((FUN_0067fdb0_shell*)stage)->FUN_0067fdb0(false);')
sub('fallout_shared/tesquest.cpp', 'stage->MarkDone(done);', '((FUN_0067fdb0_shell*)stage)->FUN_0067fdb0(done);')
sub('fallout_shared/tesquest.cpp', 'pStage->MarkDone(false);', '((FUN_0067fdb0_shell*)pStage)->FUN_0067fdb0(false);')
b, nl = rd('fallout_shared/tesquest.cpp'); i = b.index(nl + '// @fnv', 0)
# declaration before the first function that uses it: the earliest use is line 205
before_fnv('fallout_shared/tesquest.cpp', 205 - 0, 'struct FUN_0067fdb0_shell\n{\n    void FUN_0067fdb0(bool);\n};')
# I: BSFile
sub('fallout/misc/saveload/bgssaveloadfile.cpp', 'return pFile->Read(buffer, size);', 'return ((FUN_00462d80_shell*)pFile)->ReadBytes(buffer, size);')
sub('fallout/misc/saveload/bgssaveloadfile.cpp', 'return pFile->GetFilePosition();', 'return FUN_004720a0((char*)pFile);')
sub('fallout/misc/saveload/bgssaveloadfile.cpp', '\nclass FNVFileSeek', '\nstruct FUN_00462d80_shell\n{\n    unsigned int ReadBytes(void*, unsigned int);\n};\nint __fastcall FUN_004720a0(char*);\n\nclass FNVFileSeek')
# K: NiPixelFormat::GetPixelBitData -> FUN_00a77980
f = 'gamebryo2.2/corelibs/niconsolerenderer/niconsolepixelformat.cpp'
b, nl = rd(f)
n = len(re.findall(r'kPixelFormat\.GetPixelBitData\((COMP_\w+)\)', b)); print('pixelbitdata uses', n)
b = re.sub(r'kPixelFormat\.GetPixelBitData\((COMP_\w+)\)', r'((FUN_00a77980_shell*)&kPixelFormat)->FUN_00a77980(\1)', b); wr(f, b)
ln = b.split(nl).index([l for l in b.split(nl) if 'FUN_00a77980_shell*' in l][0]) + 1
before_fnv(f, ln, 'struct FUN_00a77980_shell\n{\n    unsigned char FUN_00a77980(int);\n};')
