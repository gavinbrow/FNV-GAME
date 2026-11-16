struct Wrapper {
    void __thiscall FUN_00dc3bd0(int first, int count);
    void __thiscall FUN_00dc39b0(int, int);
};
void __thiscall Wrapper::FUN_00dc3bd0(int first, int count) {
    int needed = count + count;
    int capacity = 8;
    while (capacity < needed)
        capacity += capacity;
    FUN_00dc39b0(first, capacity);
}
