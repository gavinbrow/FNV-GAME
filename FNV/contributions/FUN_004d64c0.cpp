struct ClearMap64 { int unk00; void __thiscall FUN_00438af0(); };
const char* __cdecl FUN_00464f30(const char* value, bool format);
typedef int (__stdcall *SendMessageResult64)(void*,int,int,int);
extern void (__stdcall *DAT_00fdf288)(void*, int);
extern void (__stdcall *DAT_00fdf284)(void*);
struct Header64 {
    int primary, secondary, tertiary, unused0c, unused10, unused14;
};
struct Params64 {
    const char* message;
    int unused04;
    int flags;
    int flagsCopy;
    int unused10;
    int number;
    int status18;
    int context1c;
    int callback20;
    int source24;
};
struct Owner64 {
    void* unk00;
    void* unk04;
    void* window;
    void* dialog;
    int result;
    int hwndContext;
    ClearMap64 messageMap;
    int unk1c,unk20,unk24,unk28;
    const char* defaultText;
    void __thiscall FUN_004d66d0(int a, int b);
    void __thiscall FUN_004d64c0(int value, const char* text);
};
void Owner64::FUN_004d64c0(int value, const char* text) {
    messageMap.FUN_00438af0();
    DAT_00fdf28c(dialog, 0x1109, 0, hwndContext);
    Header64 header;
    header.secondary = 0xffff0002;
    header.tertiary = 0x27;
    header.primary = 0xffff0000;
    Params64 params;
    params.message = text ? FUN_00464f30(text, false) : defaultText;
    params.flags = 0;
    params.flagsCopy = params.flags;
    params.number = value;
    result = ((SendMessageResult64)DAT_00fdf28c)(dialog,0x1100,0,(int)&header);
    FUN_004d66d0(result, value);
    DAT_00fdf288(window,10);
    DAT_00fdf284(window);
}