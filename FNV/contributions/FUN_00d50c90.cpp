
struct FUN_00d50c90;
struct ReferenceFields {
    virtual void Release() = 0;
    unsigned short memSizeAndFlags;
    short referenceCount;
    unsigned int userData;
    ReferenceFields() : referenceCount(1), userData(0) {}
};
struct BridgeAtom {
    unsigned short type;
    unsigned short flags;
    void* jacobian;
    void* constraintData;
    BridgeAtom() : type(1) {}
    void FUN_00d21ce0(FUN_00d50c90* parent);
};
template<class T>
struct ConstraintArray {
    T* data;
    int size;
    int capacityAndFlags;
    ConstraintArray() : data(0), size(0), capacityAndFlags(0x80000000) {}
};
struct ConstraintScheme {
    hkpGenericConstraintDataSchemeConstraintInfo info;
    ConstraintArray<hkVector4> data;
    ConstraintArray<int> commands;
    ConstraintArray<void*> modifiers;
    ConstraintArray<hkpConstraintMotor*> motors;
    ConstraintScheme() {
        info.m_maxSizeOfSchema = 0;
        info.m_sizeOfSchemas = 0;
        info.m_numSolverResults = 0;
        info.m_numSolverElemTemps = 0;
    }
};
struct FUN_00d50c90 : ReferenceFields {
    BridgeAtom atom;
    ConstraintScheme scheme;
    FUN_00d50c90();
};
FUN_00d50c90::FUN_00d50c90() {
    *(volatile int*)&scheme.info.m_sizeOfSchemas += 16;
    atom.FUN_00d21ce0(this);
}