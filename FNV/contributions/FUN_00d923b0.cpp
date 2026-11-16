typedef void (*Callback)();
extern void FUN_00d92300(); extern void FUN_00d921e0(); extern void FUN_00d922a0();
extern void FUN_00d922c0(); extern void FUN_00d922e0(); extern void FUN_00d92200();
extern void FUN_00d92230(); extern void FUN_00d92250(); extern void FUN_00d92270(); extern void FUN_00d92380();
struct __declspec(align(16)) CallbackTable {
    Callback callback00; Callback callback04; Callback callback08; Callback callback0c;
    Callback callback10; Callback callback14; Callback callback18; Callback callback1c;
    Callback callback20; Callback callback24; Callback callback28; Callback callback2c;
    unsigned char flag30; unsigned char flag31; unsigned char flag32; unsigned char flag33;
    Callback unk34; Callback unk38; Callback unk3c;
};
struct Context { void FUN_00cfbd60(CallbackTable*, int, int); };
void __cdecl FUN_00d923b0(void* context) {
    CallbackTable table;
    table.flag31 = 0;
    table.flag32 = 0;
    table.callback28 = 0;
    table.callback08 = 0;
    table.callback10 = FUN_00d922c0;
    table.callback14 = FUN_00d922e0;
    table.callback0c = FUN_00d922a0;
    table.callback00 = FUN_00d92300;
    table.callback2c = FUN_00d92380;
    table.callback04 = FUN_00d921e0;
    table.callback18 = FUN_00d92200;
    table.callback1c = FUN_00d92230;
    table.callback20 = FUN_00d92250;
    table.callback24 = FUN_00d92270;
    table.flag30 = 1;
    ((Context*)context)->FUN_00cfbd60(&table, -1, -1);
}

