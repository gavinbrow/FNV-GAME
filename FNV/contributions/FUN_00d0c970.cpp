struct Base { void FUN_00cfa430(int*, int, int, unsigned int); };
struct Object : Base {
    void FUN_00d0c290(int*, int);
    void FUN_00d0c3e0(int);
    void FUN_00d0c970(int*, int, int, unsigned int);
};
void Object::FUN_00d0c970(int* entries, int count, int option, unsigned int flags) {
    FUN_00cfa430(entries, count, option, flags);
    if (flags & 1) {
        if (count != 1) FUN_00d0c290(entries, count);
        else FUN_00d0c3e0(*entries);
    }
}
