struct ScalarDeletingObject {
    void FUN_00e89560();
    void* FUN_00e89440(unsigned char flags);
};
void* ScalarDeletingObject::FUN_00e89440(unsigned char flags) {
    FUN_00e89560();
    if (flags & 1)
        g_memoryManager.Deallocate(this);
    return this;
}