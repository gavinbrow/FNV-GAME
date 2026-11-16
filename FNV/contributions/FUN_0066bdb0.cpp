struct FUN_0094db80_shell { void FUN_0094db80(unsigned char); };
struct BSTreeNodeVisibilityWork : BSTreeNodeVisibility {
    bool FUN_0066bdb0(unsigned short type, unsigned char mode);
};
bool BSTreeNodeVisibilityWork::FUN_0066bdb0(unsigned short type, unsigned char mode) {
    typedef NiAVObject* (__thiscall *GetAtFn)(void*, unsigned int);
    NiAVObject* node = ((GetAtFn)(*(void***)this)[0x45])(this, type);
    if (node == 0)
        return false;
    if (mode == 0xff) {
        node->SetAppCulled(true);
    } else {
        node->SetAppCulled(false);
        NiObject* property = (NiObject*)((PropHelper*)node)->GetProperty(0);
        if (property != 0)
            ((FUN_0094db80_shell*)property)->FUN_0094db80(mode);
    }
    return true;
}
