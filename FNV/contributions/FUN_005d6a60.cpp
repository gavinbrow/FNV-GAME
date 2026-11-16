struct ScriptContextObject {virtual void Unk00();
virtual void Unk01();
virtual void Unk02();
virtual void Unk03();
virtual void Unk04();
virtual void Unk05();
virtual void Unk06();
virtual void Unk07();
virtual void Unk08();
virtual void Unk09();
virtual void Unk0a();
virtual void Unk0b();
virtual void Unk0c();
virtual void Unk0d();
virtual void Unk0e();
virtual void Unk0f();
virtual void Unk10();
virtual void Unk11();
virtual void Unk12();
virtual void Unk13();
virtual void Unk14();
virtual void Unk15();
virtual void Unk16();
virtual void Unk17();
virtual void Unk18();
virtual void Unk19();
virtual void Unk1a();
virtual void Unk1b();
virtual void Unk1c();
virtual void Unk1d();
virtual void Unk1e();
virtual void Unk1f();
virtual void Unk20();
virtual void Unk21();
virtual void Unk22();
virtual void Unk23();
virtual void Unk24();
virtual void Unk25();
virtual void Unk26();
virtual void Unk27();
virtual void Unk28();
virtual void Unk29();
virtual void Unk2a();
virtual void Unk2b();
virtual void Unk2c();
virtual void Unk2d();
virtual void Unk2e();
virtual void Unk2f();
virtual void Unk30();
virtual void Unk31();
virtual void Unk32();
virtual void Unk33();
virtual void Unk34();
virtual void Unk35();
virtual void Unk36();
virtual void Unk37();
virtual void Unk38();
virtual void Unk39();
virtual void Unk3a();
virtual void Unk3b();
virtual void Unk3c();
virtual void Unk3d();
virtual void Unk3e();
virtual void Unk3f(); virtual unsigned char IsActive();};
struct ScriptNode { unsigned char m_0[0xbc]; unsigned char m_flag; int __thiscall FUN_0055d520(); };
extern "C" bool __cdecl FUN_005accb0(int, int, int, ScriptContextObject*, int, int, int, int*);
extern "C" ScriptNode* __cdecl FUN_00ec43fb(ScriptContextObject*, int, const void*, const void*, int);
extern "C" void __cdecl FUN_00703c00(void*, int, const void*);
extern const char DAT_011841cc;
extern const char DAT_011846d4;
extern const char DAT_010399b8;
extern const char DAT_010399bc;
extern const char DAT_01039f58;
extern __declspec(thread) unsigned char isScriptDebugging;
bool __cdecl FUN_005d6a60(int a, int b, ScriptContextObject* context, int d, int e, int f, int unused, int h)
{
    ScriptNode* scriptNode = 0;
    int didParse;
    const void* statusString;
    if (context->IsActive()) {
        if (!FUN_005accb0(a,b,h,context,d,e,f,&didParse))
            return false;
        if (scriptNode == 0)
            scriptNode = FUN_00ec43fb(context,0,&DAT_011841cc,&DAT_011846d4,0);
        if (scriptNode != 0) {
            if (didParse == 0) scriptNode->m_flag = 0;
            else scriptNode->m_flag = 1;
            if (isScriptDebugging) {
                if (scriptNode->m_flag)
                    statusString = &DAT_010399bc;
                else
                    statusString = &DAT_010399b8;
                FUN_00703c00((void*)&DAT_01039f58, scriptNode->FUN_0055d520(), statusString);
            }
        }
    }
    return true;
}