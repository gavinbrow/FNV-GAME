
struct Stream {
    void* vtable;
    unsigned int* values;
    unsigned short capacity;
    unsigned short length;
    unsigned short active;
    unsigned short growth;
    void FUN_0096ad30(unsigned int required);
    void FUN_0096ae90(unsigned int index, unsigned int* value);
    __forceinline void Add(unsigned int value) {
        unsigned int index = length;
        if (index >= capacity)
            FUN_0096ad30(index + growth);
        FUN_0096ae90(index, &value);
    }
};
struct SerializedField {
    unsigned int state0;
    unsigned int state4;
    unsigned int state8;
    unsigned int stateC;
    unsigned int state10;
    unsigned int state14;
    unsigned int state18;
    unsigned int state1C;
    unsigned int state20;
    unsigned int FUN_00a59af0(const char* name);
    unsigned int FUN_00a598f0(const char* name);
};
struct SmallField {
    unsigned int state0;
    unsigned int state4;
    unsigned int state8;
    unsigned int FUN_00a59af0(const char* name);
    unsigned int FUN_00a598f0(const char* name);
};
struct IndexedElement {
    virtual void f0();
    virtual void f1();
    virtual unsigned int* GetValue();
};
struct IndexedNode {
    IndexedNode* next;
    unsigned int state;
    IndexedElement* element;
};
inline IndexedElement* const& GetNextIndexed(IndexedNode*& pos) {
    IndexedElement* const& element = pos->element;
    pos = pos->next;
    return element;
}
void __stdcall FUN_00a5ca80(Stream* stream);
unsigned int __cdecl FUN_00a7d330(unsigned int source);
unsigned int __cdecl FUN_00a7d370(const char* name, unsigned int value);
unsigned int __cdecl FUN_00a7d550(const char* name, float value);
unsigned int __cdecl FUN_00a7d5a0(unsigned int value, IndexedElement* element);
struct TextSource {
    unsigned int FUN_00a7fb20(const char* name);
};
extern unsigned int DAT_011f4280;
extern char DAT_011f4288;
extern char DAT_0109b204, DAT_0109b1f8, DAT_0109b1e4, DAT_0109b1d4, DAT_0109b1c4, DAT_0109b1b0;
extern char DAT_0109b1a0, DAT_0109b190, DAT_0109b184, DAT_0109b178, DAT_0109b164, DAT_0109b154;
extern char DAT_0109b138, DAT_0109b124, DAT_0109b118, DAT_0109b10c;
struct FUN_00a5ad00_shell {
    unsigned int unknown00,unknown04,unknown08,unknown0C,unknown10,unknown14,unknown18;
    void* propertyObject;
    TextSource* textSource;
    IndexedNode* elements;
    unsigned int elementListState;
    unsigned int elementCount;
    unsigned int flags;
    SerializedField field34;
    SmallField field58;
    float field64;
    SerializedField field68;
    SmallField field8C;
    float field98;
    void FUN_00a5ad00(Stream* stream);
};
void FUN_00a5ad00_shell::FUN_00a5ad00(Stream* stream) {
    FUN_00a5ca80(stream);
    stream->Add(FUN_00a7d330(DAT_011f4280));
    union FlagWord { unsigned int word; unsigned char byte; } firstFlag;
    firstFlag.byte = static_cast<unsigned char>(flags) & 1;
    stream->Add(FUN_00a7d370(&DAT_0109b204, firstFlag.word));
    unsigned char bit11 = static_cast<unsigned char>(flags >> 11) & 1;
    if (bit11) {
        union FlagWord { unsigned int word; unsigned char byte; } flag11;
        flag11.byte = bit11;
        stream->Add(FUN_00a7d370(&DAT_0109b1f8, flag11.word));
    }
    stream->Add(field58.FUN_00a59af0(&DAT_0109b1e4));
    stream->Add(field34.FUN_00a598f0(&DAT_0109b1d4));
    stream->Add(FUN_00a7d550(&DAT_0109b1c4, field64));
    stream->Add(field8C.FUN_00a59af0(&DAT_0109b1b0));
    stream->Add(field68.FUN_00a598f0(&DAT_0109b1a0));
    stream->Add(FUN_00a7d550(&DAT_0109b190, field98));
    stream->Add((textSource ? textSource : reinterpret_cast<TextSource*>(&DAT_011f4288))->FUN_00a7fb20(&DAT_0109b184));
    union FlagWord1 { unsigned int word; unsigned char byte; } flag1;
    flag1.byte = static_cast<unsigned char>(flags >> 1) & 1;
    stream->Add(FUN_00a7d370(&DAT_0109b178, flag1.word));
    union FlagWord2 { unsigned int word; unsigned char byte; } flag2;
    flag2.byte = static_cast<unsigned char>(flags >> 2) & 1;
    stream->Add(FUN_00a7d370(&DAT_0109b164, flag2.word));
    union FlagWord4 { unsigned int word; unsigned char byte; } flag4;
    flag4.byte = static_cast<unsigned char>(flags >> 4) & 1;
    stream->Add(FUN_00a7d370(&DAT_0109b154, flag4.word));
    union FlagWord3 { unsigned int word; unsigned char byte; } flag3;
    flag3.byte = static_cast<unsigned char>(flags >> 3) & 1;
    stream->Add(FUN_00a7d370(&DAT_0109b138, flag3.word));
    if (elementCount) {
        IndexedNode* node = elements;
        while (node != 0) {
            IndexedElement* element = GetNextIndexed(node);
            unsigned int key = *element->GetValue();
            unsigned int next = FUN_00a7d5a0(key, element);
            unsigned int index = stream->length;
            if (index >= stream->capacity)
                stream->FUN_0096ad30(index + stream->growth);
            if (index >= stream->length) {
                stream->length = index + 1;
                if (next != 0)
                    ++stream->active;
            } else if (next != 0) {
                if (stream->values[index] == 0)
                    ++stream->active;
            } else if (stream->values[index] != 0) {
                --stream->active;
            }
            stream->values[index] = next;
        }
    }
    if (propertyObject)
        stream->Add(FUN_00a7d5a0((unsigned int)&DAT_0109b124, reinterpret_cast<IndexedElement*>(propertyObject)));
    unsigned char bit10 = static_cast<unsigned char>(flags >> 10) & 1;
    if (bit10) {
        union FlagWord10 { unsigned int word; unsigned char byte; } flag10;
        flag10.byte = bit10;
        stream->Add(FUN_00a7d370(&DAT_0109b118, flag10.word));
    }
    unsigned char bit13 = static_cast<unsigned char>(flags >> 13) & 1;
    if (bit13) {
        union FlagWord13 { unsigned int word; unsigned char byte; } flag13;
        flag13.byte = bit13;
        stream->Add(FUN_00a7d370(&DAT_0109b10c, flag13.word));
    }
}
