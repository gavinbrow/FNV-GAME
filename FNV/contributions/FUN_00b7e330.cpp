
extern "C" char DAT_010f003c;
struct ShaderMapBase {virtual void BaseVirtual();unsigned int unk04,unk08;ShaderMapBase(unsigned int);~ShaderMapBase();};
struct ShaderMapArray {void* vtable;void* entries;unsigned short capacity,size,count,grow;__forceinline ShaderMapArray():grow(1),capacity(0){size=0;count=0;entries=0;vtable=&DAT_010f003c;}~ShaderMapArray();void FUN_00b799c0();};
struct FUN_00b7e330: ShaderMapBase {
 ShaderMapArray activeEntries,definedEntries;
 unsigned char enabled,unk2d,unk2e,unk2f;
 unsigned int unk30,unk34,unk38,unk3c,unk40;
 FUN_00b7e330(unsigned int,unsigned int);void FUN_00e81d00(unsigned int);virtual void MapVirtual();
};
FUN_00b7e330::FUN_00b7e330(unsigned int mapId,unsigned int initMode):
ShaderMapBase(initMode),activeEntries(),definedEntries(),unk30(0),unk34(0),unk38(0),unk3c(0),unk40(0)
{enabled=1;FUN_00e81d00(mapId);activeEntries.FUN_00b799c0();}
