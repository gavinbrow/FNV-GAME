extern int DAT_010c6ff8;
extern int DAT_010c6fd0;
struct Shape_00c9d990;
void __fastcall FUN_00c90510(Shape_00c9d990*);
struct FUN_00c9d990 {
    void* vtable;
    unsigned short memoryFlags;
    unsigned short referenceCount;
    unsigned int userData;
    unsigned int type;
    Shape_00c9d990* boundingVolume;
    void* containerVtable;
    Shape_00c9d990* child;
    FUN_00c9d990(Shape_00c9d990* bounds, Shape_00c9d990* childShape);
};
FUN_00c9d990::FUN_00c9d990(Shape_00c9d990* bounds, Shape_00c9d990* childShape) {
    referenceCount = 1;
    boundingVolume = bounds;
    userData = 0;
    type = 27;
    vtable = &DAT_010c6ff8;
    containerVtable = &DAT_010c6fd0;
    child = childShape;
    FUN_00c90510(childShape);
    FUN_00c90510(boundingVolume);
}