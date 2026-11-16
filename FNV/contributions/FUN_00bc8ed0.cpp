struct ShaderPropertyFlags {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned char flags18;
};
extern unsigned int DAT_011f91e4;
void __cdecl FUN_00b97fa0(int, int);
void __cdecl FUN_00b97ff0(int, int, int);
struct ShaderDispatcher {
    void FUN_00bc8ed0(ShaderPropertyFlags** property);
    void FUN_00be1ff0(ShaderPropertyFlags** property);
};
void ShaderDispatcher::FUN_00bc8ed0(ShaderPropertyFlags** property)
{
    unsigned int mode = DAT_011f91e4;
    ShaderPropertyFlags* shader = *property;
    if ((!shader || !(shader->flags18 & 1)) &&
        (mode - 74U <= 7U)) {
        FUN_00b97fa0(1, 0);
        FUN_00b97ff0(6, 7, 0);
    } else {
        FUN_00be1ff0(property);
    }
}