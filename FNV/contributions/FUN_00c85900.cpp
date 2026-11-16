
extern __declspec(thread) unsigned int g_havokThreadMode;

struct CollisionObject;
struct CollisionResult {
    unsigned short kind;
    unsigned short enabled;
    struct CollisionRecord* record;
    unsigned int data08;
    unsigned int data0c;
    unsigned int state;
};
struct CollisionValue {
    unsigned int data00;
    unsigned int data04;
    CollisionRecord* record;
};
struct CollisionRecord {
    unsigned int data00;
    unsigned int data04;
    struct CollisionHandler* handler;
};
struct CollisionHandler {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17();
    virtual CollisionValue* Find(int target);
    virtual void v19(); virtual void v20(); virtual void v21(); virtual void v22();
    virtual void v23(); virtual void v24(); virtual void v25(); virtual void v26();
    virtual void v27(); virtual void v28(); virtual void v29(); virtual void v30();
    virtual void v31(); virtual void v32(); virtual void v33(); virtual void v34();
    virtual void v35(); virtual void v36(); virtual void v37(); virtual void v38();
    virtual void v39(); virtual void v40(); virtual void v41(); virtual void v42();
    virtual void v43(); virtual void v44(); virtual void v45(); virtual void v46();
    virtual void v47(); virtual void v48(); virtual void v49(); virtual void v50();
    virtual void v51();
    virtual bool IsAllowed(int target);
};
struct ScopedMode {
    unsigned int oldValue;
    ScopedMode() : oldValue(g_havokThreadMode) { g_havokThreadMode = 0x10; }
    ~ScopedMode() { g_havokThreadMode = oldValue; }
};
struct WorldObjectView {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void v12(); virtual void v13(); virtual void v14(); virtual void v15();
    virtual void v16(); virtual void v17(); virtual void v18(); virtual void v19();
    virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
    virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27();
    virtual void v28(); virtual void v29(); virtual void v30(); virtual void v31();
    virtual void v32(); virtual void v33(); virtual void v34(); virtual void v35();
    virtual void v36(); virtual void v37(); virtual void v38(); virtual void v39();
    virtual void v40(); virtual void v41(); virtual void v42(); virtual void v43();
    virtual void v44();
    virtual CollisionResult* GetResult(unsigned char* used);
    void FUN_00c87600(int a, int b);
    void FUN_00c85900(int a, int b);
};

void WorldObjectView::FUN_00c85900(int a, int b) {
    ScopedMode mode;
    unsigned char used;
    CollisionResult* result = GetResult(&used);
    result->state = 0;
    CollisionRecord*& nextRecord = result->record;
    CollisionRecord* record = nextRecord;
    if (record) {
        CollisionHandler* handler = record->handler;
        if (handler && !handler->IsAllowed(b)) {
            CollisionValue* value = handler->Find(b);
            result->record = value ? value->record : 0;
        }
    }
    result->enabled = 0;
    FUN_00c87600(a, b);
}
