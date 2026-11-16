struct Allocator { void* __thiscall FUN_00aa3e40(unsigned int bytes); };
extern Allocator DAT_011f6238;
void* __cdecl operator new[](unsigned int n) {
    return DAT_011f6238.FUN_00aa3e40(n);
}
struct Point { float x, y, z; };
struct GeometryData {
    void* m_00;
    void* m_04;
    unsigned short vertexCount;
    unsigned short m_0a;
    void* m_0c;
    void* m_10;
    void* m_14;
    void* m_18;
    void* m_1c;
    void* m_20;
    void* m_24;
    void* m_28;
    void* m_2c;
    void* m_30;
    void* m_34;
    void* m_38;
    void* m_3c;
    unsigned short geomFlags;
};
struct Geometry {
    void* m_00;
    void* m_04;
    void* m_08;
    void* m_0c;
    void* m_10;
    void* m_14;
    void* m_18;
    void* m_1c;
    void* m_20;
    void* m_24;
    void* m_28;
    void* m_2c;
    void* m_30;
    void* m_34;
    void* m_38;
    void* m_3c;
    void* m_40;
    void* m_44;
    void* m_48;
    void* m_4c;
    void* m_50;
    void* m_54;
    void* m_58;
    void* m_5c;
    void* m_60;
    void* m_64;
    void* m_68;
    void* m_6c;
    void* m_70;
    void* m_74;
    void* m_78;
    void* m_7c;
    void* m_80;
    void* m_84;
    void* m_88;
    void* m_8c;
    void* m_90;
    void* m_94;
    void* m_98;
    void* m_9c;
    void* m_a0;
    void* m_a4;
    void* m_a8;
    void* m_ac;
    void* m_b0;
    void* m_b4;
    GeometryData* geometryData;
};
struct Node {
    virtual void V0(); virtual void V1(); virtual void V2(); virtual void V3();
    virtual void V4(); virtual void V5(); virtual void V6();
    virtual Geometry* GetGeometry();
};
struct Target {
    void* m_00;
    void* m_04;
    Node* node;
    void* m_0c;
    void* m_10;
    void* m_14;
    void* m_18;
    void* m_1c;
    void* m_20;
    void* m_24;
    void* m_28;
    void* m_2c;
    void* m_30;
    void* m_34;
    void* m_38;
    void* m_3c;
    Point* points;
    unsigned int m_44;
    unsigned char hasPoints;
    unsigned char m_49;
    unsigned short pointCount;
    unsigned short geomFlags;
    void FUN_00ead1e0();
};
void Target::FUN_00ead1e0() {
    if (node) {
        Geometry* geometry = node->GetGeometry();
        if (geometry && !points) {
            unsigned short count = geometry->geometryData->vertexCount;
            if (count != 0) {
                pointCount = count;
                points = new Point[count];
                hasPoints = 1;
                geomFlags = geometry->geometryData->geomFlags;
            }
        }
    }
}