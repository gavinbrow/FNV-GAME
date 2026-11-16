struct SearchNode {
    SearchNode* next;
    SearchNode* previous;
    char* item;
};
struct SearchList {
    void* unused00;
    void* unused04;
    SearchNode* first;
};
struct ProcessArgs { unsigned int a; unsigned int b; unsigned int c; };
struct SearchObject {
    unsigned char FUN_00c47150(ProcessArgs args, char* target, char* item);
};
struct ShadowProcessor {
    void FUN_00b5bbe0(SearchObject* source, ProcessArgs args, char* target);
};
typedef unsigned char (__thiscall *TestCallback)(void*, char*);
void ShadowProcessor::FUN_00b5bbe0(SearchObject* source, ProcessArgs args, char* target) {
    char* subobject = *(char**)((char*)source + 0xac);
    void* object = *(void**)(subobject + 0xc);
    unsigned int type = *(unsigned int*)(target + 0x90);
    unsigned int state = *(unsigned int*)((char*)object + 8);
    if (type != 1 && type != 3 && state == 0 && *(unsigned short*)((char*)source + 0xa8) > (unsigned short)state) {
        unsigned char accepted = (*(TestCallback*)((char*)*(void**)object + 0x9c))(object, target + 0x2c);
        *(unsigned int*)(*(char**)(*(char**)((char*)source + 0xac) + 0xc) + 8) = (accepted == 0) + 1;
        if (accepted) {
            SearchList* list = *(SearchList**)((char*)this + 0x1e0);
            if (list) {
                SearchNode* position = list->first;
                while (position) {
                    char** itemRef = &position->item;
                    position = position->next;
                    char* item = *itemRef;
                    if (item && *(unsigned int*)(item + 0x40) == 1) {
                        if (!source->FUN_00c47150(args, target, item))
                            break;
                    }
                }
            }
        }
    }
}