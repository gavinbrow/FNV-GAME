// FUN_0069bcf0 - default constructor of a non-polymorphic class.
// Disassembly facts:
//   - __thiscall, no stack args, returns this (mov eax,[ebp-0x10] epilogue)
//   - no vtable store -> non-polymorphic
//   - ctor-call on this+0x00 and this+0x0C with 3 float args each
//     (globals D_01015f5c x3 then D_01016970 x3)
//   - ctor-call on this+0x18 (0x69cd10), no args
//   - EH scope state 0 set right after, covering only the call on
//     this+0x28 (0x49f1c0) -> member at +0x18 has a non-trivial dtor
//     (unwind funclet destroys it), member at +0x28 ctor is last.

extern float D_01015f5c;
extern float D_01016970;

struct FUN_00416870 {
    float unk00;
    float unk04;
    float unk08;
    FUN_00416870(float, float, float);
};

struct FUN_0069cd10 {
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0C;
    FUN_0069cd10();
    ~FUN_0069cd10();
};

struct FUN_0049f1c0 {
    void* unk00;
    FUN_0049f1c0();
};

class FUN_0069bcf0 {
public:
    FUN_00416870 unk00;
    FUN_00416870 unk0C;
    FUN_0069cd10 unk18;
    FUN_0049f1c0 unk28;

    FUN_0069bcf0();
};

FUN_0069bcf0::FUN_0069bcf0()
    : unk00(D_01015f5c, D_01015f5c, D_01015f5c),
      unk0C(D_01016970, D_01016970, D_01016970) {}
