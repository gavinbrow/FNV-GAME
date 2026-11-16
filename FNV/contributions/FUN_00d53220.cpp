// FUN_00d53220 — destructor of a polymorphic class.
//
// Shape deduced from the target disassembly:
//   * SEH prologue (push -1 / handler / fs:[0]) with an EH state slot at
//     [esp+0x14] and a saved `this` slot at [esp+8]  -> destructor whose
//     unwind funclet must run the base class destructor.
//   * `mov [esi], vftable`  -> class with a virtual destructor.
//   * state 0 guards the body call to the free routine at 0x00c876a0.
//   * `dec dword ptr [0x1268f80]` -> body decrements a global counter.
//   * `mov ecx, esi / state -1 / call 0x00c89640` -> compiler-generated
//     base class destructor call (stand-in base named by its address).

extern int DAT_01268f80;
void __cdecl FUN_00c876a0(void);

// Stand-in for the polymorphic base class whose destructor lives at
// 0x00c89640. The base supplies the vfptr at offset 0, so the generated
// base-destructor call in ~FUN_00d53220 passes `this` unchanged.
struct FUN_00c89640 {
    virtual ~FUN_00c89640();
};

struct FUN_00d53220 : FUN_00c89640 {
    virtual ~FUN_00d53220();
};

FUN_00d53220::~FUN_00d53220()
{
    FUN_00c876a0();
    --DAT_01268f80;
}
