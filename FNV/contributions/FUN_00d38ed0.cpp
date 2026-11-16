// Stand-in for the 12-byte record the callee receives by pointer.
// Field order/offsets come from the target frame layout:
//   +0 : pointer, +4 : float, +8 : dword
struct FUN_00d38ed0_Local
{
    const char* unk00;
    float       unk04;
    int         unk08;
};

// Global float loaded with `fld dword ptr [0x104da48]`.
extern float unk_104da48;

// Global object whose address (0x10ce7fc) is stored into the record.
extern char unk_10ce7fc[];

// Callee at 0x00d386c0: __cdecl, four arguments,
// the last one being a pointer to the record built on the stack.
void __cdecl FUN_00d386c0(int unk04, int unk08, int unk0c, FUN_00d38ed0_Local* unk10);

void __cdecl FUN_00d38ed0(int param_1, int param_2, int param_3, int param_4)
{
    FUN_00d38ed0_Local local;

    local.unk04 = unk_104da48;
    local.unk08 = param_4;
    local.unk00 = unk_10ce7fc;

    FUN_00d386c0(param_2, param_1, param_3, &local);
}