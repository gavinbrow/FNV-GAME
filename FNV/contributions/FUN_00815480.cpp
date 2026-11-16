
struct EventData {
    bool FUN_004062a0();
    bool FUN_00405f30();
};
struct Event {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual int GetType();
    int id;
    int state;
    EventData data;
};
struct Handler {
    virtual void Handle4(void*, bool);
    virtual void Handle10(void*, bool);
    virtual void v2();
    virtual void v3();
    virtual void Handle1(void*, int, bool);
    virtual void v5();
    virtual void v6();
    virtual void HandleYes();
    virtual void HandleNo();
    virtual void v9();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual int HasError();
    virtual void v14();
    virtual void v15();
    virtual void SetEvent(Event*);
    virtual void v17();
    virtual void SetValue(int);
    void FUN_00818af0(int, const char*);
    bool FUN_00815480(Event*, int, bool);
};
extern char DAT_0107acc8[];
extern char DAT_0107acac[];
extern char DAT_01183140[];
extern char DAT_01183060[];
extern "C" void* __cdecl FUN_00ec43fb(Event*,int,const char*,const char*,int);
bool Handler::FUN_00815480(Event* evt, int value, bool flag) {
    if (evt->data.FUN_004062a0()) {
        FUN_00818af0(5, DAT_0107acc8);
        return false;
    }
    switch (evt->GetType()) {
      case 4:
        Handle4(FUN_00ec43fb(evt, 0, DAT_01183140, DAT_01183060, 0), flag);
        return true;
        break;
      case 1:
        Handle1(FUN_00ec43fb(evt, 0, DAT_01183140, DAT_01183060, 0), value, flag);
        return true;
        break;
      case 10:
        Handle10(FUN_00ec43fb(evt, 0, DAT_01183140, DAT_01183060, 0), flag);
        return true;
    }
    if (HasError()) {
       FUN_00818af0(6, DAT_0107acac);
       return false;
    }
    SetEvent(evt);
    SetValue(value);
    if (evt->data.FUN_00405f30() && value) {
       HandleYes();
    } else {
       HandleNo();
    }
    return true;
}