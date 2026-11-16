extern int DAT_0102e388;
struct Object {
    int* vtable;
    void FUN_00e03160();
};
void Object::FUN_00e03160() {
    vtable = &DAT_0102e388;
}
