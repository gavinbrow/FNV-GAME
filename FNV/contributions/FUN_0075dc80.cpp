// FUN_0075dc80 v1
extern void* DAT_011d93fc;
extern const char DAT_01012058[];
struct EntrySrc75 { void* FUN_007a22d0(void** pp); };
struct FloatSrc75 { float FUN_00a011b0(); };
bool __fastcall FUN_004d1360(void* player);

float __cdecl FUN_0048ebc0(int a, bool b);
struct Sound75 { double FUN_00577250(int a); };
struct StrThis75 { const char* FUN_00403df0(); };
extern StrThis75 g_011d2628;
struct Name75 { const char* FUN_0055d520(); };
struct Msg75 { static bool __cdecl FUN_007052f0(const char* msg, int a2, const char* a3, const char* a4, float a5, bool a6); };

class TESTopic : public TESForm { public: virtual ~TESTopic(); };
TESForm* __cdecl FUN_00483a00(void* a1);

extern char DAT_010722dc;
extern int DAT_01183028;
extern int DAT_01184720;
struct FloatThis75 { double FUN_008a0c20(); };
struct MenuEc75 { void FUN_0075ec60(int id); };
struct Form75 { void* __thiscall FUN_004bd740(); };
void* __fastcall FUN_007af430(void* p);
struct MenuE0B75 { bool __thiscall FUN_0075e0b0(void* refObj, int stolenDelta); };
struct MenuD6B75 { void FUN_0075d6b0(void* entry, void* fc, int param); };
struct MenuC28B75 { void FUN_0075c280(int a); };
struct PlayerAct75 { void FUN_008aded0(void* a1, int a2, int a3); };
struct ActorProc75 {
    virtual void vfn_0000();
    virtual void vfn_0004();
    virtual void vfn_0008();
    virtual void vfn_000c();
    virtual void vfn_0010();
    virtual void vfn_0014();
    virtual void vfn_0018();
    virtual void vfn_001c();
    virtual void vfn_0020();
    virtual void vfn_0024();
    virtual void vfn_0028();
    virtual void vfn_002c();
    virtual void vfn_0030();
    virtual void vfn_0034();
    virtual void vfn_0038();
    virtual void vfn_003c();
    virtual void vfn_0040();
    virtual void vfn_0044();
    virtual void vfn_0048();
    virtual void vfn_004c();
    virtual void vfn_0050();
    virtual void vfn_0054();
    virtual void vfn_0058();
    virtual void vfn_005c();
    virtual void vfn_0060();
    virtual void vfn_0064();
    virtual void vfn_0068();
    virtual void vfn_006c();
    virtual void vfn_0070();
    virtual void vfn_0074();
    virtual void vfn_0078();
    virtual void vfn_007c();
    virtual void vfn_0080();
    virtual void vfn_0084();
    virtual void vfn_0088();
    virtual void vfn_008c();
    virtual void vfn_0090();
    virtual void vfn_0094();
    virtual void vfn_0098();
    virtual void vfn_009c();
    virtual void vfn_00a0();
    virtual void vfn_00a4();
    virtual void vfn_00a8();
    virtual void vfn_00ac();
    virtual void vfn_00b0();
    virtual void vfn_00b4();
    virtual void vfn_00b8();
    virtual void vfn_00bc();
    virtual void vfn_00c0();
    virtual void vfn_00c4();
    virtual void vfn_00c8();
    virtual void vfn_00cc();
    virtual void vfn_00d0();
    virtual void vfn_00d4();
    virtual void vfn_00d8();
    virtual void vfn_00dc();
    virtual void vfn_00e0();
    virtual void vfn_00e4();
    virtual void vfn_00e8();
    virtual void vfn_00ec();
    virtual void vfn_00f0();
    virtual void vfn_00f4();
    virtual void vfn_00f8();
    virtual void vfn_00fc();
    virtual void vfn_0100();
    virtual void vfn_0104();
    virtual void vfn_0108();
    virtual void vfn_010c();
    virtual void vfn_0110();
    virtual void vfn_0114();
    virtual void vfn_0118();
    virtual void vfn_011c();
    virtual void vfn_0120();
    virtual void vfn_0124();
    virtual void vfn_0128();
    virtual void vfn_012c();
    virtual void vfn_0130();
    virtual void vfn_0134();
    virtual void vfn_0138();
    virtual void vfn_013c();
    virtual void vfn_0140();
    virtual void vfn_0144();
    virtual void vfn_0148();
    virtual void* vfn_014c();
    virtual void vfn_0150();
    virtual void vfn_0154();
    virtual void vfn_0158();
    virtual void vfn_015c();
    virtual void vfn_0160();
    virtual void vfn_0164();
    virtual void vfn_0168(int);
};
struct ProcGet75 { ActorProc75* FUN_008d8520(); };
struct Inv75 { static Inv75* __cdecl FUN_004bf220(void* refr); int FUN_004c8f30(void* form); };

void __cdecl FUN_0075dc80(int param)
{
    void* expected;
    void* refObj;
    void* entry;
    {
    bool flag;
    {
    char msgtext[260];
    entry = ((EntrySrc75*)*(void**)&DAT_011d93f8->otherData[0x70])->FUN_007a22d0(&DAT_011d93fc);
    refObj = (DAT_011d93f8->pContainerRef && ((CloseVirtualSlots*)DAT_011d93f8->pContainerRef)->IsActor()) ? (void*)DAT_011d93f8->pContainerRef : 0;
    flag = false;
    expected = (*(void**)&DAT_011d93f8->otherData[0x70] == (void*)&DAT_011d93f8->otherData[0x10]) ? (void*)DAT_011dea3c : (void*)DAT_011d93f8->pContainerRef;
    if (param == 0 || DAT_011d93fc == 0 || entry == 0)
        flag = true;
    if (((FloatSrc75*)*(void**)((ContainerLikeObj*)((int*)entry + 1))->FUN_007b5370(4009))->FUN_00a011b0() == 128.0)
        flag = true;
    if (DAT_011d93f8->eContainerMode == 3 && *(void**)&DAT_011d93f8->otherData[0x70] == (void*)&DAT_011d93f8->otherData[0x10] && refObj != 0)
    {
        if (((Sound75*)refObj)->FUN_00577250(0) + FUN_0048ebc0((int)FUN_0044ddc0(DAT_011d93fc), FUN_004d1360((void*)DAT_011dea3c)) * param >= ((FloatThis75*)refObj)->FUN_008a0c20())
        {
            FUN_00406d00(msgtext, 260, DAT_01012058, (char*)((Name75*)refObj)->FUN_0055d520(), (int)g_011d2628.FUN_00403df0());
            Msg75::FUN_007052f0(msgtext, 2, 0, 0, 2.0f, false);
            flag = true;
            int id = (int)dynamic_cast<TESTopic*>(FUN_00483a00(&DAT_010722dc));
            ((MenuEc75*)DAT_011d93f8)->FUN_0075ec60(id);
        }
    }
    }
    if (DAT_011d93f8 != 0 && DAT_011d93f8->eContainerMode == 2)
    {
        if ((expected == (void*)DAT_011dea3c && refObj != 0) ||
            (expected != (void*)DAT_011dea3c && ((Form75*)DAT_011d93fc)->FUN_004bd740() != FUN_007af430((void*)DAT_011dea3c)))
        {
            int stolenDelta;
            bool isC8 = (*(void**)&DAT_011d93f8->otherData[0x70] == (void*)&DAT_011d93f8->otherData[0x40]);
            stolenDelta = ((ContainerValue*)DAT_011d93f8)->FUN_0075e240((ItemEntry*)DAT_011d93fc, param, isC8) * (isC8 ? 1 : -1);
            DAT_011d93f8->iValueStolen += stolenDelta;
            if (!isC8)
                stolenDelta = 1;
            if (refObj != 0)
            {
                if (!((MenuE0B75*)DAT_011d93f8)->FUN_0075e0b0(refObj, stolenDelta))
                {
                    flag = true;
                    ContainerMenu::Close();
                }
            }
        }
    }
    if (!flag)
    {
        void* processBaseObject;
        void* cached = (void*)FUN_0044ddc0(DAT_011d93fc);
        processBaseObject = ((ProcGet75*)DAT_011dea3c)->FUN_008d8520()->vfn_014c();
        ((PlayerAct75*)DAT_011dea3c)->FUN_008aded0(cached, 1, 0);
        ((MenuD6B75*)DAT_011d93f8)->FUN_0075d6b0(entry, DAT_011d93fc, param);
        ((MenuC28B75*)DAT_011d93f8)->FUN_0075c280((int)cached);
        if (processBaseObject != 0)
        {
            if (Inv75::FUN_004bf220((void*)DAT_011dea3c)->FUN_004c8f30((void*)FUN_0044ddc0(processBaseObject)) == 0)
            {
                ((ProcGet75*)DAT_011dea3c)->FUN_008d8520()->vfn_0168(0);
            }
        }
    }
    }}
