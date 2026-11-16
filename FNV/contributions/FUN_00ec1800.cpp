struct FUN_00ec1800_cls
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int hObject;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    bool bWaiting;
    void __thiscall FUN_00ec1800();
};

extern "C" __declspec(dllimport) unsigned long __stdcall WaitForSingleObject(unsigned long, unsigned long);

void __thiscall FUN_00ec1800_cls::FUN_00ec1800()
{
    if (hObject != 0)
    {
        bWaiting = true;
        WaitForSingleObject(hObject, 0xffffffffu);
        hObject = 0;
        bWaiting = false;
    }
}