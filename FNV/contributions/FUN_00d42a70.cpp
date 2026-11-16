
extern char DAT_010cf280[];
struct Header {
    const char* tag;
    unsigned short byteCount;
    unsigned short format;
    int userValue;
    int result;
};
struct Allocator {
    virtual void* unknown();
    virtual Header* allocate(int size);
};
struct Resource { int unk00;int unk04;int unk08;int unk0c; Allocator* allocator; };
Resource* __cdecl FUN_00c85750();

struct Meta {int unk00; int unk04; int unk08; int sequence;};
struct Root {
    int unk00; int unk04; int unk08; int unk0c; int unk10;
    Meta* volatile meta;
    int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c;
    int portion30;
};
struct DataHandle{int handle;DataHandle(int n):handle(n) {}};
struct InputA { Root* root; int unk04; int data; };
struct Path {int unk00; int unk04; int unk08; int subIndex;};
struct InputB {Path* path;};
struct InputC {unsigned char* state; int unk04;int unk08;int unk0c;int unk10;int tableFlag;};
__declspec(align(16)) struct WorkArea {
    void* entries[44];
    void FUN_00d431b0(struct DataHandle data);
    void FUN_00cb2240(struct DataHandle data, int* portion);
};
struct CallbackArgs {
    Meta* meta;
    int zero;
    WorkArea* workspace;
    InputA* source;
};
typedef int (__cdecl *Handler)(CallbackArgs*,InputB*,InputC*,int);
struct HandlerEntry {
    Handler handler;
    int unk04; int unk08; int unk0c; int unk10;
};
Header* __cdecl FUN_00d42a70(InputA* a,InputB* b,InputC* c,int value) {
    Resource* resource = FUN_00c85750();
    Header* header = resource->allocator->allocate(16);
    header->byteCount=16;
    header->format=1;
    header->userValue=value;
    header->tag=DAT_010cf280;
    Root* root=a->root;
    Meta* meta=root->meta;
    WorkArea workspace;
    workspace.FUN_00d431b0(DataHandle(a->data));
    workspace.FUN_00cb2240(DataHandle(a->data),&root->portion30);
    CallbackArgs args = {meta,0,&workspace,a};
    Path* path=b->path;
    bool flag=c->tableFlag!=0;
    unsigned char* data=c->state;
    int subIndex=path->subIndex;
    int seq=meta->sequence;
    unsigned char* table=flag ? data+0x5a0 : data+0x1a0;
    unsigned char kind=table[(seq<<5)+subIndex];
    Handler handler=((HandlerEntry*)(data+0x9a0))[kind].handler;
    header->result=handler(&args,b,c,value);
    return header;
}
