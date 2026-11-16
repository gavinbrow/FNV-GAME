struct FUN_00c91620_Target;

struct FUN_00c91620_Args {
    unsigned char type;
    FUN_00c91620_Target* target;
};

struct FUN_00c91620_Aux {
    void* m_00; void* m_04; void* m_08; void* m_0c;
    void* m_10; void* m_14; void* m_18; void* m_1c; void* m_20;
    void FUN_00d01a80();
};

struct FUN_00c91620_Target {
    virtual void vf00(); virtual void vf04(); virtual void vf08();
    virtual void vf0c(); virtual void vf10(); virtual void vf14();

    unsigned short m_04;
    void* m_08; void* m_0c; void* m_10; void* m_14;
    void* m_18; void* m_1c; void* m_20; void* m_24;
    void* m_28; void* m_2c;
    FUN_00c91620_Aux m_30;
    int m_54;

    void FUN_00c905b0();
};

struct FUN_00c91620_Class {
    void* m_00; void* m_04; void* m_08; void* m_0c;
    void* m_10; void* m_14; void* m_18; void* m_1c;
    void* m_20; void* m_24; void* m_28; void* m_2c;
    void* m_30; void* m_34; void* m_38; void* m_3c;
    void* m_40; void* m_44; void* m_48; void* m_4c;
    void* m_50; void* m_54; void* m_58; void* m_5c;
    void* m_60; void* m_64; void* m_68; void* m_6c;
    void* m_70; void* m_74; void* m_78; void* m_7c;
    void* m_80; void* m_84; void* m_88; void* m_8c;
    void* m_90;
    int m_94;
    void* m_98;
    unsigned char m_9c;
    unsigned char m_9d;
    void* m_a0;
    int m_a4;
    void FUN_00c91160(FUN_00c91620_Args* args);
    void FUN_00c91120();
    void FUN_00c91140();
    unsigned char* FUN_00c91620(unsigned char* result, FUN_00c91620_Target* target);
};

void __cdecl FUN_00cb5c10(FUN_00c91620_Class* self, FUN_00c91620_Target* target);
void __cdecl FUN_00d005a0(FUN_00c91620_Class* self, FUN_00c91620_Target* target);
void __cdecl FUN_00cffab0(FUN_00c91620_Target* target);
void __cdecl FUN_00cb4740(FUN_00c91620_Class* self, FUN_00c91620_Target* target);

unsigned char* FUN_00c91620_Class::FUN_00c91620(
    unsigned char* result, FUN_00c91620_Target* target)
{
    if (m_94 != 0) {
        FUN_00c91620_Args args;
        args.type = 2;
        args.target = target;
        FUN_00c91160(&args);
        *result = 0;
        return result;
    }

    m_94 = 1;
    FUN_00cb5c10(this, target);
    FUN_00d005a0(this, target);
    FUN_00cffab0(target);
    m_9d = 0;
    FUN_00cb4740(this, target);

    if (target->m_54 != 0) {
        target->m_30.FUN_00d01a80();
    }

    if (target->m_04 == 0) {
        target->vf14();
    }
    target->FUN_00c905b0();

    --m_94;
    m_9d = 1;

    if (m_94 == 0 && m_9c == 0) {
        if (m_8c != 0)
            FUN_00c91120();
        if (m_a4 == 1 && m_90 != 0)
            FUN_00c91140();
    }
    *result = 1;
    return result;
}