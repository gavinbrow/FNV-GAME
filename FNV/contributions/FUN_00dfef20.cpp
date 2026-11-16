struct HavokObject {
    void* volatile primaryVtable;
    unsigned int referenceCount;
    void* volatile secondaryVtable;
};
extern unsigned char DAT_010c925c;
extern unsigned char DAT_010debf4;
extern unsigned char DAT_010debe4;

void __cdecl FUN_00dfef20(HavokObject* object)
{
    if (object) {
        object->secondaryVtable = &DAT_010c925c;
        object->primaryVtable = &DAT_010debf4;
        object->secondaryVtable = &DAT_010debe4;
    }
}