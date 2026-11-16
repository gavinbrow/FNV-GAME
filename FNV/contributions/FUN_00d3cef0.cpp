struct Conversion {
    void (*convert)();
    void (*create)();
    void (*copy)();
    void (*destroy)();
    bool enabled;
    bool supported;
};
struct Registry { void FUN_00cfbbe0(Conversion*, int, int); };
void FUN_00d3c400(); void FUN_00d3cfc0(); void FUN_00d3d040(); void FUN_00d3ac80();
void FUN_00d3c380(); void FUN_00d3c440(); void FUN_00d3cc00(); void FUN_00daf8e0();
void __cdecl FUN_00d3cef0(Registry* registry) {
    Conversion conversion;
    conversion.convert = FUN_00d3c400;
    conversion.create = FUN_00d3cfc0;
    conversion.copy = FUN_00d3d040;
    conversion.destroy = FUN_00d3ac80;
    conversion.enabled = true;
    conversion.supported = false;
    registry->FUN_00cfbbe0(&conversion, 4, 1);
    conversion.convert = FUN_00d3c380;
    conversion.create = FUN_00d3c440;
    conversion.copy = FUN_00d3cc00;
    conversion.destroy = FUN_00daf8e0;
    conversion.enabled = false;
    conversion.supported = false;
    registry->FUN_00cfbbe0(&conversion, 1, 4);
}
