struct Point3 {float x;float y;float z;};
struct Bound {Point3 center;float radius;};
struct FUN_00a8a920 {
 virtual void GetRTTI();
 unsigned int refCount;
 unsigned short vertices;
 unsigned short geometryId;
 unsigned short dataFlags;
 unsigned short dirtyFlags;
 Bound bounds;
 void* vertexData;
 void* normalData;
 void* colors;
 void* textures;
 void* additionalData;
 void* rendererData;
 unsigned char keepFlags;
 unsigned char compressFlags;
 unsigned char vertexLocked;
 unsigned char vertexWriteLocked;
 unsigned char saveVertexData;
 unsigned char reserved3d0;
 unsigned char reserved3d1;
 unsigned char reserved3d2;
 unsigned short triangles;
 FUN_00a8a920(int a1,int a2,int a3,int a4,int a5,int a6,int a7,int a8);
};
struct FUN_00a75dc0 : FUN_00a8a920 {
 unsigned short strips;
 unsigned short* stripLengths;
 unsigned short* stripLists;
 virtual void GetRTTI();
 FUN_00a75dc0(int a1,int a2,int a3,int a4,int a5,int a6,int a7,int a8,
 unsigned short stripCount,unsigned short* lengths,unsigned short* lists);
};
FUN_00a75dc0::FUN_00a75dc0(int a1,int a2,int a3,int a4,int a5,int a6,int a7,int a8,
 unsigned short stripCount,unsigned short* lengths,unsigned short* lists)
 : FUN_00a8a920(a1,a2,a3,a4,a5,a6,a7,a8), strips(stripCount), stripLengths(lengths), stripLists(lists) {}