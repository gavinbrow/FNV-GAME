struct Crux53_HkRouter {int unk00,unk04,unk08,unk0c;void* heap;};
void* FUN_00c85750();
void __cdecl FUN_00c856c0(void* heap, void* ptr);
char* __cdecl FUN_00cb1410(const char* src);
inline void Crux53_FreeName(char* existing) {
    Crux53_HkRouter* router=(Crux53_HkRouter*)FUN_00c85750();
    FUN_00c856c0(router->heap,existing);
}
struct Crux53_Named {int unk00,unk04,unk08;char* name;void FUN_00e05110(const char* newName);};
void Crux53_Named::FUN_00e05110(const char* newName) {
    Crux53_FreeName(name);
    name=FUN_00cb1410(newName);
}