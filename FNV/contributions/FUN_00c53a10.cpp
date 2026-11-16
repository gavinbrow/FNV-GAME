struct RefList { unsigned int* elements; unsigned int unk04; unsigned int count; };
struct BinaryStream { unsigned int FUN_00a63430(); };
struct ControllerObject {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c;
    unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2c;
    unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3c;
    RefList** lists; unsigned short unk44; unsigned short listCount;
    void FUN_00a6d500(BinaryStream*);
    void FUN_00c53a10(BinaryStream*);
};
void ControllerObject::FUN_00c53a10(BinaryStream* stream) {
    FUN_00a6d500(stream);
    for (unsigned int i = 0; i < listCount; ++i) {
        RefList* list = lists[i];
        if (list != 0) {
            unsigned int value = 0;
            unsigned int size;
            unsigned int j;
            for (; value < (j = list->count); ++value) {
                size = stream->FUN_00a63430();
                if (value >= list->count) {
                } else {
                    list->elements[value] = size;
                }
            }
        }
    }
}