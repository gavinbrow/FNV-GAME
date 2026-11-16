class TESForm { public: virtual ~TESForm() {} };
class Actor : public TESForm {};
struct DbeffectBaseCall { void FUN_00806e70(void*); };
class ActiveEffect { public: void Dispel(bool); };
TESForm* __cdecl FUN_004839c0(unsigned int);
struct Dbeffect : SummonCreatureEffect {
    int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18;
    int unk1C; int unk20; int unk24; int unk28; int unk2C; int unk30;
    int unk34; int unk38; int unk3C; int unk40; int unk44; int unk48;
    int formId;
    void FUN_00829900(void* arg);
};
void Dbeffect::FUN_00829900(void* arg)
{
    ((DbeffectBaseCall*)this)->FUN_00806e70(arg);
    int current = formId;
    if (current) {
        formId = (int)dynamic_cast<Actor*>(FUN_004839c0((unsigned int)current));
        if (!formId)
            ((ActiveEffect*)this)->Dispel(true);
    }
}
