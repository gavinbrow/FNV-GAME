extern int DAT_0102f024;
struct CellHandleData {
    int FUN_004bc320();
    void FUN_0054e710();
};
struct CellHandle {
    void* object;
    void FUN_00633c90(int value);
    CellHandleData* FUN_00559450(int index);
    CellHandleData* FUN_00559450();
    void FUN_0066b0d0(int value);
    void FUN_0045cec0();
    CellHandle(int value) { FUN_00633c90(value); }
    ~CellHandle() { FUN_0045cec0(); }
};
struct CellTypedHandle : CellHandle {
    void* typeData;
    CellTypedHandle(int value) : CellHandle(value) {}
    void FUN_006e5cc0(CellTypedHandle* other);
};
struct CellHandleProvider {
    bool FUN_00425fd0();
    void FUN_0054ee80(CellHandle* handle);
    void FUN_0054e640(CellTypedHandle* result);
};
void CellHandleProvider::FUN_0054e640(CellTypedHandle* result)
{
    CellTypedHandle current(0);
    current.typeData = &DAT_0102f024;
    if (!FUN_00425fd0()) {
        CellHandle child(0);
        FUN_0054ee80(&child);
        current.FUN_0066b0d0(child.FUN_00559450(0)->FUN_004bc320());
        child.FUN_00559450()->FUN_0054e710();
    }
    result->FUN_006e5cc0(&current);
}