extern "C" void* __cdecl FUN_00aa13e0(unsigned int bytes);
struct FUN_006e3850 {
    void* begin;
    void* end;
    void* reservedEnd;
    unsigned int capacity;
    unsigned int count;
    unsigned int flags;
    static __forceinline void* __cdecl operator new(unsigned int bytes) { return FUN_00aa13e0(bytes); }
    FUN_006e3850();
    int __thiscall FUN_0044ddc0();
    void __thiscall FUN_006e3ad0(int newCount, int preserve);
    void* __thiscall FUN_006a1400(int index);
};
struct ThreatItem_009f8570 { void __thiscall FUN_009f6f30(void* element); };
struct FUN_009f8570_class { FUN_006e3850* __thiscall FUN_009f8570(); };
FUN_006e3850* __thiscall FUN_009f8570_class::FUN_009f8570() {
    FUN_006e3850* output = new FUN_006e3850;
    int total = reinterpret_cast<ThreatList*>(reinterpret_cast<char*>(this) + 0xa0)->FUN_0044ddc0();
    for (int index = 0; index < total; ++index) {
        int used;
        ThreatItem_009f8570* item;
        item = reinterpret_cast<ThreatItem_009f8570*>(reinterpret_cast<ThreatList*>(reinterpret_cast<char*>(this) + 0xa0)->FUN_009f8a80(index));
        used = output->FUN_0044ddc0();
        output->FUN_006e3ad0(used + 1, 1);
        item->FUN_009f6f30(output->FUN_006a1400(used));
    }
    return output;
}
