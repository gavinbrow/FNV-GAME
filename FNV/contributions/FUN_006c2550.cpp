struct FNVNode;
struct FNVNodeList { unsigned int FUN_00453470(); FNVNode* func_0x0043b4a0(unsigned int index); };
struct FNVNode {
    virtual void Unknown0(); virtual void Unknown1(); virtual void Unknown2(); virtual FNVNodeList* GetChildren();
};
struct FNVType { int FUN_0043b4d0(); };
struct FNVData { FNVType* func_0x0043b4f0(int* value); };
struct FNVObject { FNVData* func_0x006fa820(); };
FNVObject* __cdecl func_0x0043b610(FNVNode* node);
struct FNVResultMember { void func_0x0066b0d0(FNVData* data); };
struct FNVResult { int unk00; int unk04; int unk08; FNVResultMember record; };
void __cdecl func_0x006c2650(FNVResult* result);
bool __cdecl FUN_006c2550(FNVNode* node, FNVResult* result) {
    FNVNodeList* children5;
    FNVObject* object5 = func_0x0043b610(node);
    FNVData* data;
    int type_2;
    unsigned int indexVal;
    int value7;
    if (object5) {
        data = object5->func_0x006fa820();
        if (data) {
            type_2 = data->func_0x0043b4f0(&value7)->FUN_0043b4d0();
            if (type_2 == 2 || type_2 == 1 || type_2 == 4 || type_2 == 10 || type_2 == 20 || type_2 == 28) {
                result->unk08 = 0;
                result->record.func_0x0066b0d0(data);
                func_0x006c2650(result);
                return true;
            }
        }
    }
    children5 = node->GetChildren();
    if (children5) {
        for (indexVal = 0; indexVal < children5->FUN_00453470(); ++indexVal) {
            if (children5->func_0x0043b4a0(indexVal)) {
                if (FUN_006c2550(children5->func_0x0043b4a0(indexVal), result))
                    return true;
            }
        }
    }
    return false;
}
