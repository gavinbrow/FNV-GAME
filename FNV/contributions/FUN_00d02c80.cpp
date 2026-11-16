struct Registry {void* unk00;void* unk04;void* unk08;void* unk0C;void* unk10;void* unk14;void* unk18;void* unk1C;void* unk20;void* unk24;void* unk28;void* unk2C;void* unk30;void* unk34;void* unk38;void* unk3C;void* unk40;void* unk44;void* unk48;void* unk4C;void* unk50;void* unk54;void* unk58;void* unk5C;void* unk60;void* unk64;void* unk68;void* unk6C;};
struct World {int unk00;int unk04;int unk08;int unk0C;int unk10;int unk14;int unk18;int unk1C;int unk20;int unk24;int unk28;int unk2C;int unk30;int unk34;int unk38;int unk3C;int unk40;int unk44;int unk48;int unk4C;int unk50;int unk54;int unk58;int unk5C;int unk60;Registry* registry;};
struct Reserve {void FUN_00d97070(int);};
struct Owner {int unk00;int unk04;int unk08;int unk0C;int unk10;int unk14;int unk18;int unk1C;int unk20;int unk24;int unk28;int unk2C;int unk30;int unk34;int unk38;int unk3C;int unk40;int unk44;int unk48;int unk4C;int unk50;int unk54;Reserve* reserve;};
struct FUN_00d0d020 {virtual void method0();int unk04,unk08;Owner* volatile owner;int unk10;int unk14;int unk18;int unk1C;int unk20;int unk24;int unk28;int unk2C;int unk30;int unk34;int unk38;int unk3C;int unk40;int unk44;int unk48;int unk4C;__declspec(nothrow) FUN_00d0d020(World*);};
struct ListenerA {virtual void method0();void* context;ListenerA():context(0){} };
struct ListenerB {virtual void method0();void* context;ListenerB():context(0){} };
struct ListenerC {virtual void method0();void* context;ListenerC():context(0){} };
struct Array {void* data;int count;unsigned capacity;Array():data(0),count(0),capacity(0x80000000){} };
struct FUN_00cf6da0 {int debugInfo,lockCount,recursionCount;void* owningThread;void* semaphore;unsigned spinCount;__declspec(nothrow) FUN_00cf6da0(int);};
struct FUN_00c90f30 {int value;__declspec(nothrow) FUN_00c90f30();};
struct FUN_00d02c80:FUN_00d0d020 {
 virtual void method0();ListenerA a;ListenerB b;ListenerC c;volatile bool enabled;Array first;FUN_00cf6da0 firstLock;Array second;FUN_00cf6da0 secondLock;FUN_00c90f30 counter;int unkB8,unkBC;volatile int active;int unkC4;int unkC8;int unkCC;int unkD0;int unkD4;int unkD8;int unkDC;int unkE0;int unkE4;int unkE8;int unkEC;int unkF0;int unkF4;int unkF8;int unkFC;FUN_00cf6da0 queueLock;int unk118;int unk11C;int unk120;int unk124;int unk128;int unk12C;int unk130;int unk134;int unk138;int unk13C;FUN_00cf6da0 workLock;
 FUN_00d02c80(World*);
};
FUN_00d02c80::FUN_00d02c80(World* world):FUN_00d0d020(world),firstLock(4000),secondLock(4000),queueLock(4000),workLock(4000)
{

 active=0;enabled=false;owner->reserve->FUN_00d97070(10000);
 a.context=this;b.context=&workLock;
 world->registry->unk24=&a;world->registry->unk44=&b;world->registry->unk28=&b;world->registry->unk48=&b;
 c.context=&workLock;
 world->registry->unk2C=&c;world->registry->unk64=&c;world->registry->unk4C=&c;world->registry->unk68=&c;world->registry->unk6C=&c;
}



