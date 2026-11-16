
struct WorldPoint {
    float x, y, z;
    void FUN_006815c0();
};
struct ReferenceObject {
    bool FUN_00425fd0();
};
struct SecondaryObject {
    ReferenceObject* FUN_00587550(WorldPoint*);
};
struct SearchTable {
    bool FUN_004511e0(ReferenceObject*, int);
};
extern SearchTable* DAT_011dea10;
void __cdecl FUN_00846190(void*, ReferenceObject**, SecondaryObject**);
void __cdecl FUN_00573800(void*, ReferenceObject*, SecondaryObject*);

struct WorldReference {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8();
    virtual void v9();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual void v35();
    virtual void v36();
    virtual void v37();
    virtual void v38();
    virtual void v39();
    virtual void v40();
    virtual void v41();
    virtual void v42();
    virtual void v43();
    virtual void v44();
    virtual void v45();
    virtual void v46();
    virtual void v47();
    virtual void v48();
    virtual void v49();
    virtual void v50();
    virtual void v51();
    virtual void v52();
    virtual void v53();
    virtual void v54();
    virtual void v55();
    virtual void v56();
    virtual void v57();
    virtual void v58();
    virtual void v59();
    virtual void v60();
    virtual void v61();
    virtual void v62();
    virtual void v63();
    virtual void v64();
    virtual void v65();
    virtual void v66();
    virtual void v67();
    virtual void v68();
    virtual void v69();
    virtual void v70();
    virtual void v71();
    virtual void v72();
    virtual void v73();
    virtual void v74();
    virtual void v75();
    virtual void v76();
    virtual void v77();
    virtual bool v78(WorldPoint*, WorldPoint*, void**, int);
    bool FUN_005653d0();
    void FUN_00575830(WorldPoint*);
    void FUN_00575700(WorldPoint);
    void FUN_00562020();
    bool FUN_00561ef0(int);
};

bool WorldReference::FUN_00561ef0(int flags) {
    WorldPoint start;
    WorldPoint end;
    start.FUN_006815c0();
    end.FUN_006815c0();
    void* result = 0;
    if (v78(&start, &end, &result, flags)) {
        ReferenceObject* object = 0;
        SecondaryObject* secondary = 0;
        FUN_00846190(result, &object, &secondary);
        if (secondary)
            object = secondary->FUN_00587550(&start);
        if (FUN_005653d0() || (object && DAT_011dea10->FUN_004511e0(object, 0))) {
            FUN_00575830(&start);
            FUN_00575700(end);
            if (object && object->FUN_00425fd0())
                FUN_00573800(this, object, 0);
            else
                FUN_00573800(this, 0, secondary);
            FUN_00562020();
            return true;
        }
    }
    return false;
}
