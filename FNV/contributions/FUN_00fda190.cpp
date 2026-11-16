extern "C" char DAT_01094e9c;extern "C" void *DAT_011f3360;
extern "C" void FUN_00aa10f0(void*);
struct __declspec(novtable) BSMapBase_00a09200 {
 virtual void dummy();void FUN_00ae91f0();
 ~BSMapBase_00a09200(){*(void**)this=&DAT_01094e9c;FUN_00ae91f0();FUN_00aa10f0(DAT_011f3360);}
};
struct FUN_00a0d840 : BSMapBase_00a09200 {
 virtual ~FUN_00a0d840(){volatile unsigned u0;
volatile unsigned u1;
volatile unsigned u2;
volatile unsigned u3;FUN_00ae91f0();}
};
extern "C" FUN_00a0d840 DAT_011f3358;
struct Dummy{~Dummy(){DAT_011f3358.FUN_00a0d840::~FUN_00a0d840();}};
Dummy g_dummy;