struct TESObjectREFR_GetFlags_caller {
    unsigned int CallGetFlags();
    operator const char*() const;
};

struct FUN_00726070_shell {
    void* FUN_00726070();
};

struct FUN_005ab240_shell {
    bool FUN_005ab240(void*);
};

struct FUN_0067dbf0_shell {
    int unk00;
    int unk04;
    int unk08;
    bool FUN_0067dbf0(TESObjectREFR_GetFlags_caller* apParam);
};

bool FUN_0067dbf0_shell::FUN_0067dbf0(TESObjectREFR_GetFlags_caller* apParam)
{
    if (unk00 != (int)(void*)apParam->operator const char*())
        return true;
    if (unk08 != apParam->CallGetFlags())
        return true;
    if ((void*)unk04 || ((FUN_00726070_shell*)apParam)->FUN_00726070())
    {
        if (!(void*)unk04 || !((FUN_00726070_shell*)apParam)->FUN_00726070())
            return true;
        if (((FUN_005ab240_shell*)unk04)->FUN_005ab240(((FUN_00726070_shell*)apParam)->FUN_00726070()))
            return true;
    }
    return false;
}