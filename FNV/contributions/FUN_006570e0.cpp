struct QueryResult {
    void __thiscall FUN_006147e0();
    void __thiscall FUN_006148f0();
};
struct QueryObject {
    QueryResult* __thiscall FUN_004ac110(QueryObject*, char*);
    QueryResult* __thiscall FUN_004ac110(QueryObject*, char*, char*);
};
extern "C" void __cdecl FUN_00a61fb0(char*);
void __cdecl FUN_006570e0(QueryObject* object) {
    char firstPath[264];
    char secondPath[264];
    object->FUN_004ac110(object, secondPath)->FUN_006147e0();
    object->FUN_004ac110(object, secondPath, firstPath)->FUN_006148f0();
    FUN_00a61fb0(firstPath);
}
