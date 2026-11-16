struct Child { unsigned int unk00; unsigned int unk04; };
struct Owner { unsigned int unk00; unsigned int unk04; Child* child; unsigned int FUN_00d9e000(); };
unsigned int Owner::FUN_00d9e000() { return child->unk04; }
