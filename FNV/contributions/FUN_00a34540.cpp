
extern void* DAT_011f36dc;
extern char DAT_01044a7c, DAT_01096678, DAT_0105ac84, DAT_0109666c;
extern char DAT_01096664, DAT_01044c94, DAT_01044c90, DAT_0109665c;
extern char DAT_01096654, DAT_010477f4, DAT_01096648, DAT_0109663c;
extern char DAT_01096630, DAT_01096624;

struct OutputArray {
    void* unk00;
    void** data;
    unsigned short capacity;
    unsigned short length;
    unsigned short populated;
    unsigned short growth;
    void FUN_0096ad30(unsigned int capacity);
    void FUN_0096ae90(unsigned int index, void** value);
    void Append(void* value) {
        unsigned int index = length;
        if (index >= capacity)
            FUN_0096ad30(index + growth);
        FUN_0096ae90(index, &value);
    }
};

struct ControlItem {
    void* unk00;
    void* unk04;
    void* unk08;
    unsigned char unk0c;
    unsigned char priority;
    unsigned short unk0e;
};
struct TagItem {
    const char* first;
    const char* second;
    const char* third;
    const char* fourth;
    const char* fifth;
};

void* __cdecl FUN_00a7d330(void*);
void* __cdecl FUN_00a31140(const char*,void*);
void* __cdecl FUN_00a7d510(const char*, unsigned int);
void* __cdecl FUN_00a7d550(const char*, float);
void* __cdecl FUN_00a6d190(const char*,void*);
int __cdecl FUN_00a305b0(char*,unsigned int,const char*,...);
void* __cdecl FUN_00a7d5e0(const char*,const char*);

struct Position { unsigned int i; unsigned int tagOffset; };
struct Sequence {
    void* unk00;
    void* unk04;
    void* unk08;
    unsigned int itemCount;
    void* unk10;
    ControlItem* controls;
    TagItem* tags;
    float mainWeight;
    void* unk20;
    void* interp;
    float fadeIn;
    float fadeOut;
    float duration;
    float offset;
    float rate;
    float extra3c;
    void* unk40;
    void* name;
    float start;
    float end;
    float total;
    void FUN_00a5d6e0(OutputArray*);
    void FUN_00a34540(OutputArray* output);
};

void Sequence::FUN_00a34540(OutputArray* output) {
    FUN_00a5d6e0(output);
    output->Append(FUN_00a7d330(DAT_011f36dc));
    output->Append(FUN_00a31140(&DAT_01044a7c,name));
    output->Append(FUN_00a7d510(&DAT_01096678,itemCount));
    output->Append(FUN_00a7d550(&DAT_0105ac84,mainWeight));
    output->Append(FUN_00a6d190(&DAT_0109666c,interp));
    output->Append(FUN_00a7d550(&DAT_01096664,fadeIn));
    output->Append(FUN_00a7d550(&DAT_01044c94,fadeOut));
    output->Append(FUN_00a7d550(&DAT_01044c90,duration));
    output->Append(FUN_00a7d550(&DAT_0109665c,offset));
    output->Append(FUN_00a7d550(&DAT_01096654,start));
    output->Append(FUN_00a7d550(&DAT_010477f4,end));
    output->Append(FUN_00a7d550(&DAT_01044c90,total));
    output->Append(FUN_00a7d550(&DAT_01096648,rate));
    output->Append(FUN_00a7d550(&DAT_0109663c,extra3c));
    Position pos;
    pos.i = 0;
    if (pos.i < itemCount) {
        char key[128];
        char val[256];
        unsigned int ctrlOffset = 0;
        pos.tagOffset = 0;
        do {
            TagItem* tag = (TagItem*)((char*)tags + pos.tagOffset);
            ControlItem* ctrl = (ControlItem*)((char*)controls + ctrlOffset);
            FUN_00a305b0(key, sizeof(key), &DAT_01096630, pos.i);
            FUN_00a305b0(val, sizeof(val), &DAT_01096624,
                tag->first,tag->third,ctrl->priority);
            void* entry=FUN_00a7d5e0(key,val);
            unsigned int index=output->length;
            if(index >= output->capacity)
                output->FUN_0096ad30(index+output->growth);
            if(index >= output->length) {
                output->length=index+1;
                if(entry) output->populated++;
            } else if(entry) {
                if (!output->data[index]) output->populated++;
            } else if(output->data[index]) {
                output->populated--;
            }
            output->data[index]=entry;
            pos.tagOffset += sizeof(TagItem);
            ctrlOffset += sizeof(ControlItem);
            ++pos.i;
        } while (pos.i < itemCount);
    }
}
