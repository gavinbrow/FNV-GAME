struct StrArrView {
    void* vtable;
    char** data;
    unsigned short capacity;
    unsigned short count;
    unsigned short elementSize;
    unsigned short growBy;
};
extern void* DAT_012007d8;
extern const char DAT_010b9e1c[];
extern const char DAT_010b9e0c[];
extern const char DAT_010b9dfc[];
extern const char DAT_010b9df4[];
extern const char DAT_010b9dec[];
extern char DAT_011f444c;
extern char* __cdecl FUN_00a7d550(const char*, float);
extern char* __cdecl FUN_00a7d5e0(const char*, unsigned int);
struct GameGraphicsObject {
    virtual void Method0();
    virtual void Method1();
    virtual void Method2();
    virtual void Method3();
    virtual void Method4();
    virtual void Method5();
    virtual void Method6();
    virtual void Method7();
    virtual void Method8();
    virtual void Method9();
    virtual void Method10();
    virtual void Method11();
    virtual void Method12();
    virtual void Method13();
    virtual void Method14();
    virtual void Method15();
    virtual void Method16();
    virtual void Method17();
    virtual void Method18();
    virtual void Method19();
    virtual void Method20();
    virtual void Method21();
    virtual void Method22();
    virtual void Method23();
    virtual void Method24();
    virtual void Method25();
    virtual void Method26();
    virtual void Method27();
    virtual void Method28();
    virtual void Method29();
    virtual void Method30();
    virtual void Method31();
    virtual void Method32();
    virtual void Method33();
    virtual void Method34();
    virtual void Method35();
    virtual void Method36();
    virtual void Method37();
    virtual void Method38();
    virtual unsigned int* GetGraphicsValue();
};
extern GameGraphicsObject* __stdcall FUN_00653290(const void*);
struct ShaderPassParameters {
    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1c;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned int unknown28;
    unsigned int unknown2c;
    unsigned int unknown30;
    unsigned int unknown34;
    unsigned int unknown38;
    unsigned int unknown3c;
    unsigned int unknown40;
    unsigned int unknown44;
    unsigned int unknown48;
    unsigned int unknown4c;
    unsigned int unknown50;
    unsigned int unknown54;
    unsigned int unknown58;
    unsigned int unknown5c;
    void* volatile enabledData;
    unsigned int unknown64;
    float parameter68;
    float parameter6c;
    float parameter70;
    float parameter74;
    void FUN_00bb7f90(StrArr*);
};
void ShaderPassParameters::FUN_00bb7f90(StrArr* array) {
    FUN_00ba9890(array);
    StrArrView* arrayView = reinterpret_cast<StrArrView*>(array);
    char* value = FUN_00a7d330(DAT_012007d8);
    { unsigned int at = arrayView->count;
      if (at >= arrayView->capacity)
        array->SetSize(at + arrayView->growBy);
      array->SetAt(at, value);
    }
    value = FUN_00a7d550(DAT_010b9e1c, parameter68);
    { unsigned int at = arrayView->count;
      if (at >= arrayView->capacity)
        array->SetSize(at + arrayView->growBy);
      array->SetAt(at, value);
    }
    value = FUN_00a7d550(DAT_010b9e0c, parameter6c);
    { unsigned int at = arrayView->count;
      if (at >= arrayView->capacity)
        array->SetSize(at + arrayView->growBy);
      array->SetAt(at, value);
    }
    value = FUN_00a7d550(DAT_010b9dfc, parameter70);
    { unsigned int at = arrayView->count;
      if (at >= arrayView->capacity)
        array->SetSize(at + arrayView->growBy);
      array->SetAt(at, value);
    }
    value = FUN_00a7d550(DAT_010b9df4, parameter74);
    { unsigned int at = arrayView->count;
      if (at >= arrayView->capacity)
        array->SetSize(at + arrayView->growBy);
      array->SetAt(at, value);
    }
    if (enabledData) {
        GameGraphicsObject* object = FUN_00653290(&DAT_011f444c);
        if (object) {
            unsigned int graphicalValue = *object->GetGraphicsValue();
            value = FUN_00a7d5e0(DAT_010b9dec, graphicalValue);
    { unsigned int at = arrayView->count;
      if (at >= arrayView->capacity)
        array->SetSize(at + arrayView->growBy);
      array->SetAt(at, value);
    }
        }
    }
}