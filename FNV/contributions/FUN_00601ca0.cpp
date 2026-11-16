
struct SaveField {
    void FUN_00487010();
    void FUN_004891d0(unsigned int, unsigned int);
    void FUN_0047cac0();
    void FUN_0048b830();
    void FUN_0048d330();
    void FUN_0047bd70();
    void FUN_00477f20();
    void FUN_00483710();
    unsigned int FUN_009611e0();
};
struct FaceValue {
    float* data;
    unsigned int offset;
    const float* FUN_00629ab0();
};
struct FaceMatrix {
    unsigned int FUN_009611e0();
    FaceValue FUN_0060b370(unsigned int index, unsigned int column);
};
struct GameForm {
    unsigned int FUN_0084e3a0();
};
struct HeadPartNode {
    bool FUN_008256d0();
    GameForm** FUN_006815c0();
    HeadPartNode* FUN_00726070();
};
extern void __cdecl FUN_00485910(unsigned int tag, unsigned int data);
extern void __cdecl FUN_00485910(unsigned int tag, float value);
extern void __cdecl FUN_00485950(unsigned int tag, unsigned int value);
extern void __cdecl FUN_00485990(unsigned int tag, void* ptr, unsigned int length);
extern void __cdecl FUN_00485710(unsigned int tag, const void* ptr, unsigned int length);
extern void __cdecl FUN_00403d30(void*, int, unsigned int);
extern void* __cdecl FUN_00401000(unsigned int size);
extern void __cdecl FUN_00401030(void*);
extern bool __cdecl FUN_00401500();

struct NPCSerializer {
    void FUN_004855a0();
    void FUN_00485e00();
    HeadPartNode* FUN_00602170();
    GameForm* FUN_00603b50();
    float FUN_00602130();
    GameForm* FUN_00602150();
    void FUN_00485680();
    void FUN_00601ca0();
};

void NPCSerializer::FUN_00601ca0()
{
    unsigned int count;
    FUN_004855a0();
    ((SaveField*)((char*)this + 0xd0))->FUN_00487010();
    ((SaveField*)((char*)this + 0xdc))->FUN_004891d0(0x4c444f4d,0x54444f4d);
    ((SaveField*)((char*)this + 0x30))->FUN_0047cac0();
    ((SaveField*)((char*)this + 0x10c))->FUN_0048b830();
    ((SaveField*)((char*)this + 0x7c))->FUN_0048d330();
    ((SaveField*)((char*)this + 0x70))->FUN_0047bd70();
    ((SaveField*)((char*)this + 0x104))->FUN_00477f20();

    if (*(GameForm**)((char*)this + 0x130)) {
        count = (*(GameForm**)((char*)this + 0x130))->FUN_0084e3a0();
        FUN_00485910(0x4d414e43, count);
    }
    FUN_00485e00();
    if (FUN_00401500())
        ((SaveField*)((char*)this + 0x114))->FUN_00483710();
    FUN_00485990(0x4d414e44, (char*)this + 0x114, 0x1c);
    if (FUN_00401500())
        ((SaveField*)((char*)this + 0x114))->FUN_00483710();

    HeadPartNode* head = FUN_00602170();
    while (head && !head->FUN_008256d0()) {
        GameForm* item = *head->FUN_006815c0();
        FUN_00485910(0x4d414e50, item->FUN_0084e3a0());
        head = head->FUN_00726070();
    }

    if (FUN_00603b50()) {
        FUN_00485910(0x4d414e48, FUN_00603b50()->FUN_0084e3a0());
        FUN_00485910(0x4d414e4c, FUN_00602130());
    }
    if (FUN_00602150()) {
        FUN_00485910(0x4d414e45, FUN_00602150()->FUN_0084e3a0());
    }
    FUN_00485910(0x524c4348, *(unsigned int*)((char*)this + 0x1d8));

    typedef GameForm* (__thiscall *GetExtraFace)(NPCSerializer*);
    if (((GetExtraFace)((*(void***)this)[0x188/4]))(this)) {
        FUN_00485910(0x4d414e5a, ((GetExtraFace)((*(void***)this)[0x188/4]))(this)->FUN_0084e3a0());
    }
    FUN_00485910(0x344d414e, *(unsigned int*)((char*)this + 0x1e4));

    unsigned int formID = ((FaceMatrix*)((char*)this + 0x134))->FUN_009611e0();
    if (formID != 0) {
        unsigned int values = formID * 4;
        float* bytes = (float*)FUN_00401000(values);
        FUN_00403d30(bytes,0,values);
        for (unsigned int index = 0; index < formID; ++index) {
            bytes[index] = *((FaceMatrix*)((char*)this + 0x134))->FUN_0060b370(index,0).FUN_00629ab0();
        }
        FUN_00485710(0x53474746,bytes,formID);
        FUN_00401030(bytes);
        bytes = 0;
    }
    formID = ((FaceMatrix*)((char*)this + 0x154))->FUN_009611e0();
    if (formID != 0) {
        unsigned int bytesSecond = formID * 4;
        float* valuesSecond = (float*)FUN_00401000(bytesSecond);
        FUN_00403d30(valuesSecond,0,bytesSecond);
        for (unsigned int indexSecond = 0; indexSecond < formID; ++indexSecond) {
            valuesSecond[indexSecond] = *((FaceMatrix*)((char*)this + 0x154))->FUN_0060b370(indexSecond,0).FUN_00629ab0();
        }
        FUN_00485710(0x41474746,valuesSecond,formID);
        FUN_00401030(valuesSecond);
        valuesSecond = 0;
    }
    formID = ((FaceMatrix*)((char*)this + 0x174))->FUN_009611e0();
    if (formID != 0) {
        unsigned int bytesThird = formID * 4;
        float* valuesThird = (float*)FUN_00401000(bytesThird);
        FUN_00403d30(valuesThird,0,bytesThird);
        for (unsigned int indexThird = 0; indexThird < formID; ++indexThird) {
            valuesThird[indexThird] = *((FaceMatrix*)((char*)this + 0x174))->FUN_0060b370(indexThird,0).FUN_00629ab0();
        }
        FUN_00485710(0x53544746,valuesThird,formID);
        FUN_00401030(valuesThird);
        valuesThird = 0;
    }

    FUN_00485950(0x354d414e, *(unsigned short*)((char*)this + 0x1d0));
    FUN_00485910(0x364d414e, *(float*)((char*)this + 0x1f4));
    FUN_00485910(0x374d414e, *(float*)((char*)this + 0x1f8));
    FUN_00485680();
}
