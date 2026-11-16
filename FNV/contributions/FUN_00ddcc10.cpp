struct Process;
struct Allocator { virtual void First(); virtual void Second(); virtual void Release(Process*, unsigned short); };
struct ProcessServices { int a,b,c,d; Allocator* allocator; };
ProcessServices* __cdecl FUN_00c85750();
struct Process {
    int unk00; unsigned short unk04; unsigned short unk06; int unk08;
    void FUN_00ddcb50();
    Process* FUN_00ddcc10(unsigned char flags);
};
Process* Process::FUN_00ddcc10(unsigned char flags)
{
    FUN_00ddcb50();
    if (flags & 1) {
        ProcessServices* services = FUN_00c85750();
        unsigned short size = unk04;
        Allocator* allocator = services->allocator;
        allocator->Release(this, size);
    }
    return this;
}
