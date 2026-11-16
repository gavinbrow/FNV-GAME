struct Callee : UnkHolder {
    void __thiscall FUN_00dbec60(UnkRet*, int);
};
void __thiscall UnkHolder::FUN_00dbedb0(UnkRet* value, int count) {
    int needed = count + count;
    int capacity = 8;
    while (capacity < needed)
        capacity += capacity;
    ((Callee*)this)->FUN_00dbec60(value, capacity);
}
