struct PacketEntry {
    unsigned int identifier;
    unsigned int state;
    unsigned int offset;
    unsigned int length;
    unsigned int mode;
    unsigned int flags;
    PacketEntry();
    ~PacketEntry();
};
struct PacketScope {
    unsigned int key;
    unsigned int state;
    unsigned int start;
    unsigned int end;
    unsigned int flags;
    unsigned int context;
    unsigned int owner;
    PacketScope(unsigned int selector);
    ~PacketScope();
};
void __cdecl FUN_00ab2640(PacketScope* scope, void* owner, PacketEntry* begin, PacketEntry* next);
struct FUN_00659670 {
    unsigned int mode;
    PacketEntry entries[2];
    FUN_00659670(unsigned int selector);
};
FUN_00659670::FUN_00659670(unsigned int selector) {
    PacketScope scope(selector);
    FUN_00ab2640(&scope, this, &entries[0], &entries[1]);
}