struct Allocator { virtual void reserved(); virtual void* allocate(unsigned int); };
struct BSAudio { int unk00, unk04, unk08, unk0c; Allocator* allocator; };
void* __cdecl FUN_00c85750();
struct FUN_00d657d0_class { FUN_00d657d0_class* FUN_00d657d0(int); };
void* __cdecl FUN_00d65910(void* context) {
    BSAudio* audio = (BSAudio*)FUN_00c85750();
    FUN_00d657d0_class* result = (FUN_00d657d0_class*)audio->allocator->allocate(0x74);
    *(unsigned short*)((char*)result + 4) = 0x74;
    result = result->FUN_00d657d0((int)context);
    if (result)
        return (char*)result + 8;
    return 0;
}
