struct FUN_00cb0a60_Field {
    unsigned int value;
    void initialize();
};
struct FUN_00c90510_Entity {
    void addReference();
};
struct FUN_00d2b260 {
    void* vptr;
    unsigned short memSizeAndFlags;
    short referenceCount;
    void* world;
    void* island;
    unsigned int userData;
    FUN_00cb0a60_Field name;
    FUN_00c90510_Entity* entity;
    FUN_00d2b260(FUN_00c90510_Entity* entity, unsigned int userData);
};
FUN_00d2b260::FUN_00d2b260(FUN_00c90510_Entity* newEntity, unsigned int data)
{
    referenceCount = 1;
    userData = data;
    vptr = &DAT_010cc2fc;
    world = 0;
    island = 0;
    name.initialize();
    vptr = &DAT_010ce528;
    entity = newEntity;
    if (newEntity)
        newEntity->addReference();
}