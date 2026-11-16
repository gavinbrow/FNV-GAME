struct ResourceKey { int first; int second; };
struct SoundEntry { void* sound; };
struct Receiver {
    void __thiscall FUN_009ba760(void* sound);
    void __thiscall FUN_009ba780(void* description);
};
struct Description {
    int __thiscall FUN_009ba980();
    void __thiscall FUN_009ba810(ResourceKey* key);
};
struct ResourceLookup {
    int unk00;
    int unk04;
    int unk08;
    int __thiscall FUN_009be8c0(int first, int second, int flags);
};
struct AudioResourceState {
    void* active;
    ResourceLookup lookup;
    SoundEntry** entries;
    void* __thiscall FUN_00dbebe0(Receiver* receiver, Description* description);
};
void* AudioResourceState::FUN_00dbebe0(Receiver* receiver, Description* description) {
    ResourceKey key;
    if (active && !description->FUN_009ba980()) {
        description->FUN_009ba810(&key);
        int index = lookup.FUN_009be8c0(key.first, key.second, -1);
        if (index != -1) {
            receiver->FUN_009ba760(entries[index]->sound);
            return receiver;
        }
    }
    receiver->FUN_009ba780(description);
    return receiver;
}



