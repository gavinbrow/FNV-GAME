struct FaceGenCoordElement {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    ~FaceGenCoordElement();
};

struct FaceGenVectorMember {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    ~FaceGenVectorMember();
};

struct FaceGenFinalMember {
    unsigned int unk00;
    ~FaceGenFinalMember();
};

struct FUN_00651760 {
    unsigned int unk00;
    unsigned int unk04;
    FaceGenCoordElement m_coordinates[4];
    FaceGenVectorMember m_secondary;
    FaceGenFinalMember m_final;
    ~FUN_00651760();
};

FUN_00651760::~FUN_00651760()
{
}
