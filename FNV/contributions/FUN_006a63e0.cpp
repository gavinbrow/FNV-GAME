struct FNVValue {
    int data;
    void __thiscall FUN_0045cec0();
    __forceinline ~FNVValue() { FUN_0045cec0(); }
};

struct FNVEmbedded {
    void __thiscall FUN_006e5cc0(FNVValue* value);
};

struct FNVDestination {
    int unk00;
    int unk04;
    FNVEmbedded embedded;
};

struct FNVHost {
    void __thiscall FUN_006a63e0(FNVDestination* destination, int value, FNVValue extra);
};

void FNVHost::FUN_006a63e0(FNVDestination* destination, int value, FNVValue extra)
{
    destination->unk04 = value;
    destination->embedded.FUN_006e5cc0(&extra);
}
