
struct FNV_006ef920_Vertex {
    unsigned int unk00,unk04,unk08;
    NiPoint3 position;
};
struct FNV_006ef920_Nodes {
    FNV_006ef920_Vertex* first;
    FNV_006ef920_Vertex* second;
};
struct FNV_006ef920_Temporary {
    unsigned int handle;
    FNV_006ef920_Temporary() { FUN_0042fb00(); }
    ~FNV_006ef920_Temporary() { FUN_0042fa40(); }
    void FUN_0042fb00();
    void FUN_0042fa40();
    void* FUN_00559450();
};
struct FNV_006ef920_Serializer {
    bool FUN_0069ad00(FNV_006ef920_Temporary*);
};
struct FNV_006ef920_Entry {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    FNV_006ef920_Serializer* serializer;
    unsigned short identifier;
    unsigned short unk42;
    void* extra;
    unsigned int unk48;
    FNV_006ef920_Nodes* sideA;
    FNV_006ef920_Nodes* sideB;
};
struct FNV_006ef920_Record { unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c; unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1c; unsigned int unk20; void FUN_006efd50(); };
struct FNV_006ef920_RecordFields {
    void* handle;
    unsigned short identifier;
    unsigned short unk06;
    void* extra;
};
struct FNV_006ef920_Receiver {
    void FUN_006cf4c0(FNV_006ef920_Record*);
};
struct FNV_006ef920 {
    FNV_006ef920_Receiver* receiver;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    IndexCollection edges;
    bool FUN_006efd80(FNV_006ef920_Nodes*, FNV_006ef920_Nodes*, bool);
    bool FUN_006ef920();

};
bool FNV_006ef920::FUN_006ef920() {
    FNV_006ef920_Nodes* prevA = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(0))->sideA;
    FNV_006ef920_Nodes* prevB = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(0))->sideB;
    for (unsigned int index = 1; index < edges.FUN_0044ddc0(); ++index) {
        FNV_006ef920_Nodes* nextA = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->sideA;
        FNV_006ef920_Nodes* nextB = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->sideB;
        if (nextA == prevA && !FUN_006efd80(nextB,nextA,false)) {
            if (receiver)
                {
        FNV_006ef920_Record record; record.FUN_006efd50();
        FNV_006ef920_Temporary temp;
        if (reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->serializer->FUN_0069ad00(&temp)) {
            
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).handle = temp.FUN_00559450();
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).identifier = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->identifier;
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).extra = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->extra;
            receiver->FUN_006cf4c0(&record);
        }
    }
            return false;
        }
        if (nextB == prevB && !FUN_006efd80(nextA,nextB,true)) {
            if (receiver)
                {
        FNV_006ef920_Record record; record.FUN_006efd50();
        FNV_006ef920_Temporary temp;
        if (reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->serializer->FUN_0069ad00(&temp)) {
            
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).handle = temp.FUN_00559450();
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).identifier = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->identifier;
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).extra = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->extra;
            receiver->FUN_006cf4c0(&record);
        }
    }
            return false;
        }
        prevA = nextA;
        prevB = nextB;
    }
    for (unsigned int index = 0; index < edges.FUN_0044ddc0(); ++index) {
        FNV_006ef920_Nodes* nodesA = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->sideA;
        FNV_006ef920_Nodes* nodesB = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->sideB;
        if (FUN_00696540(&nodesA->first->position,
                          &nodesA->second->position,
                          &nodesB->first->position,
                          &nodesB->second->position)) {
            if (receiver)
                {
        FNV_006ef920_Record record; record.FUN_006efd50();
        FNV_006ef920_Temporary temp;
        if (reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->serializer->FUN_0069ad00(&temp)) {
            
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).handle = temp.FUN_00559450();
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).identifier = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->identifier;
            reinterpret_cast<FNV_006ef920_RecordFields&>(record).extra = reinterpret_cast<FNV_006ef920_Entry*>(*edges.FUN_00877a30(index))->extra;
            receiver->FUN_006cf4c0(&record);
        }
    }
            return false;
        }
    }
    return true;
}
