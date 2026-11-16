// FUN_00d60020 - slot-allocator + duplicate-key registry insert.
// Bumps the 0x34-byte slot cursor at this+0x238 (int3 assert against the
// limit at +0x23c), runs the new slot's 4-arg initializer with a pointer to
// this+0x28, then scans the FUN_00dd7200_cls* registry at this+0x190
// (count at +0x234) comparing the dword key at slot+4. Duplicate: hand the
// new slot to the pack-declared FUN_00d5fc70(FUN_00dd7200_cls*) and return
// the existing entry; otherwise append and return the new slot.
//
// Target: __thiscall (this in ecx), callee pops 12, 146 B, /MT /O2 /GS /EHsc /Gy.

#include <intrin.h>

// Free-list slot object: 0x34 bytes, key dword at +4.
struct Slot17 : FUN_00dd7200_cls {
    int unk00;      // +0x00
    int f4;         // +0x04 key compared against registry entries
    int pad08;
    int pad0C;
    int pad10;
    int pad14;
    int pad18;
    int pad1C;
    int pad20;
    int pad24;
    int pad28;
    int pad2C;
    int pad30;      // ends at +0x34

    void FUN_00dd7650(int a1, int a2, int a3, void* out);
};

// Registry owner object (same this as FUN_00d5fc70_cls).
struct Owner17 : FUN_00d5fc70_cls {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;      // +0x28 object whose address seeds FUN_00dd7650
    int unk02C;
    int unk030;
    int unk034;
    int unk038;
    int unk03C;
    int unk040;
    int unk044;
    int unk048;
    int unk04C;
    int unk050;
    int unk054;
    int unk058;
    int unk05C;
    int unk060;
    int unk064;
    int unk068;
    int unk06C;
    int unk070;
    int unk074;
    int unk078;
    int unk07C;
    int unk080;
    int unk084;
    int unk088;
    int unk08C;
    int unk090;
    int unk094;
    int unk098;
    int unk09C;
    int unk0A0;
    int unk0A4;
    int unk0A8;
    int unk0AC;
    int unk0B0;
    int unk0B4;
    int unk0B8;
    int unk0BC;
    int unk0C0;
    int unk0C4;
    int unk0C8;
    int unk0CC;
    int unk0D0;
    int unk0D4;
    int unk0D8;
    int unk0DC;
    int unk0E0;
    int unk0E4;
    int unk0E8;
    int unk0EC;
    int unk0F0;
    int unk0F4;
    int unk0F8;
    int unk0FC;
    int unk100;
    int unk104;
    int unk108;
    int unk10C;
    int unk110;
    int unk114;
    int unk118;
    int unk11C;
    int unk120;
    int unk124;
    int unk128;
    int unk12C;
    int unk130;
    int unk134;
    int unk138;
    int unk13C;
    int unk140;
    int unk144;
    int unk148;
    int unk14C;
    int unk150;
    int unk154;
    int unk158;
    int unk15C;
    int unk160;
    int unk164;
    int unk168;
    int unk16C;
    int unk170;
    int unk174;
    int unk178;
    int unk17C;
    int unk180;
    int unk184;
    int unk188;
    int unk18C;
    FUN_00dd7200_cls* slots[41];   // +0x190 registry, count at +0x234
    int count234;                  // +0x234
    Slot17* volatile cur238;       // +0x238 slot bump cursor (volatile: assert + reload pattern)
    Slot17* end23c;                // +0x23c allocation limit

    FUN_00dd7200_cls* FUN_00d60020(int a1, int a2, int a3);
};

FUN_00dd7200_cls* Owner17::FUN_00d60020(int a1, int a2, int a3)
{
    if (cur238 >= end23c) {
        __debugbreak();
    }
    Slot17* s = cur238;
    cur238 = s + 1;

    if (s != 0) {
        s->FUN_00dd7650(a1, a2, a3, &unk28);
    }

    for (int i = 0; i < count234; i++) {
        if (((Slot17*)slots[i])->f4 == s->f4) {
            FUN_00d5fc70(s);
            return slots[i];
        }
    }

    slots[count234] = s;
    count234++;
    return s;
}
