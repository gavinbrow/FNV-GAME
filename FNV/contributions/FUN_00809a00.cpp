struct Actor;
struct SaveFormHeader;
class TESForm
{
public:
    virtual void Reserved00();
    virtual void Reserved01();
    virtual void Reserved02();
    virtual void Reserved03();
    virtual void Reserved04();
    virtual void Reserved05();
    virtual void Reserved06();
    virtual void Reserved07();
    virtual void Reserved08();
    virtual void Reserved09();
    virtual void Reserved10();
    virtual void Reserved11();
    virtual void Reserved12();
    virtual void Reserved13();
    virtual void Reserved14();
    virtual void Reserved15();
    virtual void Reserved16();
    virtual void Reserved17();
    virtual void Reserved18();
    virtual void Reserved19();
    virtual void Reserved20();
    virtual void Reserved21();
    virtual void Reserved22();
    virtual void Reserved23();
    virtual void Reserved24();
    virtual void Reserved25();
    virtual void Reserved26();
    virtual void Reserved27();
    virtual void Reserved28();
    virtual void Reserved29();
    virtual void Reserved30();
    virtual void Reserved31();
    virtual void Reserved32();
    virtual void Reserved33();
    virtual void Reserved34();
    virtual void Reserved35();
    virtual void Reserved36();
    virtual void Reserved37();
    virtual void Reserved38();
    virtual void Reserved39();
    virtual void Reserved40();
    virtual void Reserved41();
    virtual void Reserved42();
    virtual void Reserved43();
    virtual void Reserved44();
    virtual void Reserved45();
    virtual void Reserved46();
    virtual void Reserved47();
    virtual void Reserved48();
    virtual void Reserved49();
    virtual void Reserved50();
    virtual void Reserved51();
    virtual void Reserved52();
    virtual void Reserved53();
    virtual void Reserved54();
    virtual void Reserved55();
    virtual void Reserved56();
    virtual void Reserved57();
    virtual void Reserved58();
    virtual void Reserved59();
    virtual void Reserved60();
    virtual void Reserved61();
    virtual void Reserved62();
    virtual void Reserved63();
    virtual void Reserved64();
    virtual void Reserved65();
    virtual void Reserved66();
    virtual void Reserved67();
    virtual void Reserved68();
    virtual void Reserved69();
    virtual void Reserved70();
    virtual void Reserved71();
    virtual void Reserved72();
    virtual void Reserved73();
    virtual void Reserved74();
    virtual void Reserved75();
    virtual char* GetSaveSizeLabel();
};

struct EffectItem
{
    unsigned short __thiscall FUN_004be5a0();
};

struct FUN_00806da0_shell
{
    unsigned short __thiscall FUN_00806da0(Actor* apActor);
};

class TESSaveLoadGame
{
public:
    bool __thiscall FUN_00862110();
    unsigned char __thiscall FUN_008df040();
    SaveFormHeader* __thiscall GetCurrentFormHeader();
};

extern TESSaveLoadGame* g_TESSaveLoadGame;

struct GlobalObject_0045cf30
{
    unsigned char* __thiscall Bool();
};
extern GlobalObject_0045cf30 g_011de4e8;

extern TESForm* __cdecl FUN_004839c0(unsigned int formID);
extern void __cdecl FUN_0040fbe0(const char* format, ...);

struct BoundItemEffectSaveSizeLayout
{
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    EffectItem* unk4c;
    EffectItem* effectItems[20];

    unsigned short __thiscall FUN_00809a00(Actor* apActor);
};

unsigned short __thiscall BoundItemEffectSaveSizeLayout::FUN_00809a00(Actor* apActor)
{
    unsigned short usSize9 = 0;
    usSize9 += ((FUN_00806da0_shell*)this)->FUN_00806da0(apActor);
    unsigned short usBaseSize8 = usSize9;

    if (g_TESSaveLoadGame->FUN_00862110())
    {
        usSize9 += 4;
        usSize9 += 2;
    }

    usSize9 += 1;
    if (unk4c != 0)
    {
        usSize9 += unk4c->FUN_004be5a0();
    }

    int i6;
    for (i6 = 0; i6 < 20; ++i6)
    {
        usSize9 += 1;
        if (effectItems[i6] != 0)
        {
            usSize9 += effectItems[i6]->FUN_004be5a0();
        }
    }

    if (g_011de4e8.Bool()[0] != 0)
    {
        SaveFormHeader* pHeader = g_TESSaveLoadGame->GetCurrentFormHeader();
        if (pHeader != 0)
        {
            TESForm* pForm = FUN_004839c0(*(unsigned int*)pHeader);
            FUN_0040fbe0("GetSaveSize(): %-5i for form %08X %s with flags %08X ending at line %i in file %s",
                usSize9 - usBaseSize8,
                *(unsigned int*)pHeader,
                pForm->GetSaveSizeLabel(),
                *(unsigned int*)((char*)pHeader + 5),
                0x29b,
                "D:\\_Fallout3\\Platforms\\Common\\Code\\Fallout\\Magic\\BoundItemEffect.cpp");
        }
        else
        {
            FUN_0040fbe0("GetSaveSize(): %-5i ending at line %i in file %s",
                usSize9 - usBaseSize8,
                0x29b,
                "D:\\_Fallout3\\Platforms\\Common\\Code\\Fallout\\Magic\\BoundItemEffect.cpp");
        }
    }

    if (g_TESSaveLoadGame->FUN_008df040() >= 0x41)
    {
        usSize9 += 4;
        usSize9 += 1;
    }
    if (g_TESSaveLoadGame->FUN_008df040() >= 0x6b)
    {
        usSize9 += 1;
    }
    return usSize9;
}


