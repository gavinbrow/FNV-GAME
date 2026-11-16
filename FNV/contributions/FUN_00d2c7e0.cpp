extern int DAT_010cc2fc;
struct Prefix { int vtable; int unk04; int unk08; int unk0c; int unk10; ~Prefix(); };

struct FUN_00cb0a70_Class { void FUN_00cb0a70(int); };
struct FUN_00d2c7e0_class : Prefix { FUN_00cb0a70_Class sub; FUN_00d2c7e0_class(int value); };
FUN_00d2c7e0_class::FUN_00d2c7e0_class(int value) {
    vtable = (int)&DAT_010cc2fc;
    sub.FUN_00cb0a70(value);
}

