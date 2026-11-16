
#include <string.h>

struct FUN_006815c0 {
    float x, y, z;
    FUN_006815c0();
};

struct FUN_004a7800 {
    float x, y, z, w;
    FUN_004a7800();
};

struct Resource {
    void* FUN_00544c30();
    void* FUN_00544c60();
};

struct FUN_005405a0 {
    void* unknown00;
    FUN_006815c0** positions;
    FUN_006815c0** normals;
    FUN_004a7800** transforms;
    unsigned char** tags;
    int unknown14;
    int unknown18;
    int unknown1c;
    void* resources[4];
    void* metadata[4];
    float** vertexRows[4];
    int unknown50, unknown54, unknown58, unknown5c;
    int unknown60, unknown64, unknown68, unknown6c;
    int unknown70, unknown74, unknown78, unknown7c;
    int unknown80, unknown84, unknown88, unknown8c;
    int unknown90, unknown94;
    void* initialValue98;
    void* initialValue9c;
    int unknownA0;
    FUN_005405a0();
};

struct GeometryOwner {
    int unknown00, unknown04, unknown08, unknown0c;
    int unknown10, unknown14, unknown18, unknown1c;
    Resource* resource;
    int unknown24;
    FUN_005405a0* geometry;
    float FUN_0053a550();
    bool FUN_00539500(GeometryOwner* source);
};

extern void* DAT_011c9ed4[4];
extern void* DAT_011c9eec;
extern void* DAT_011c9ef0;
extern void* DAT_011c9ef8;
extern float DAT_0102dcc4;

bool GeometryOwner::FUN_00539500(GeometryOwner* source)
{
    if (geometry != 0 && geometry->positions != 0)
        return false;

    geometry = new FUN_005405a0;
    geometry->initialValue98 = resource->FUN_00544c30();
    geometry->initialValue9c = resource->FUN_00544c60();

    geometry->positions = new FUN_006815c0*[4];
    geometry->transforms = new FUN_004a7800*[4];
    geometry->normals = new FUN_006815c0*[4];
    geometry->tags = new unsigned char*[4];

    float height = FUN_0053a550();
    for (int i = 0; i < 4; ++i) {
        geometry->positions[i] = new FUN_006815c0[0x121];
        geometry->transforms[i] = new FUN_004a7800[0x121];
        geometry->normals[i] = new FUN_006815c0[0x121];
        geometry->tags[i] = new unsigned char[0x121];
        geometry->vertexRows[i] = new float*[0x121];
        geometry->resources[i] = (void*)FUN_00535ae0();
        geometry->metadata[i] = new unsigned char[0x18];

        if (!source || !source->geometry) {
            memcpy(geometry->positions[i], DAT_011c9ed4[i], 0xd8c);
            memcpy(geometry->transforms[i], DAT_011c9eec, 0x1210);
            memcpy(geometry->normals[i], DAT_011c9ef0, 0xd8c);
            memcpy(geometry->tags[i], DAT_011c9ef8, 0x121);

            if (height != DAT_0102dcc4) {
                for (int j = 0; j < 0x121; ++j)
                    geometry->positions[i][j].z = height;
            }

            float* vertexData = new float[0x121 * 8];
            memset(vertexData, 0, 0x2420);
            for (int k = 0; k < 0x121; ++k)
                geometry->vertexRows[i][k] = vertexData + k * 8;
            memset(geometry->metadata[i], 0, 0x18);
        }
    }
    return true;
}