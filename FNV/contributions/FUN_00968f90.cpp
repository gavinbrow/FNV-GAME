extern unsigned int __cdecl FUN_00487f50();
class DialoguePayload { public: unsigned int* FUN_006815c0(); };
class DialogueEntry { public: DialoguePayload* FUN_00559450(); unsigned int FUN_0044ddc0(unsigned int value,int first,int second); };
class DialogueCollection { public: bool FUN_0076b610(); unsigned int FUN_0044ddc0(); DialogueEntry** FUN_00877a30(unsigned int index); };
class DialoguePlayer { public: unsigned int FUN_00968be0(unsigned int selected); unsigned int FUN_00968f90(); };
unsigned int DialoguePlayer::FUN_00968f90() {
    unsigned int result = 0;
    if (!reinterpret_cast<DialogueCollection*>(reinterpret_cast<unsigned char*>(this)+0xdf4)->FUN_0076b610()) {
        DialogueEntry* entry = *reinterpret_cast<DialogueCollection*>(reinterpret_cast<unsigned char*>(this)+0xdf4)->FUN_00877a30(
              FUN_00487f50() % reinterpret_cast<DialogueCollection*>(reinterpret_cast<unsigned char*>(this)+0xdf4)->FUN_0044ddc0());
        result = FUN_00968be0(entry->FUN_0044ddc0(
            entry->FUN_00559450() ? *entry->FUN_00559450()->FUN_006815c0() : 0,
            1, 1));
    }
    return result;
}