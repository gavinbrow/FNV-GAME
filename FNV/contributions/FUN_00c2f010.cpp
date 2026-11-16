// Reworked from another contributor's supplied best attempt; credit retained.

struct ParticleInfo { float x,y,z,age,lifespan,lastUpdate,variance; };
struct ParticleSystem {
 virtual void v00();
 virtual void v01();
 virtual void v02();
 virtual void v03();
 virtual void v04();
 virtual void v05();
 virtual void v06();
 virtual void v07();
 virtual void v08();
 virtual void v09();
 virtual void v10();
 virtual void v11();
 virtual void v12();
 virtual void v13();
 virtual void v14();
 virtual void v15();
 virtual void v16();
 virtual void v17();
 virtual void v18();
 virtual void v19();
 virtual void v20();
 virtual void v21();
 virtual void v22();
 virtual void v23();
 virtual void v24();
 virtual void v25();
 virtual void v26();
 virtual void v27();
 virtual void v28();
 virtual void v29();
 virtual void v30();
 virtual void v31();
 virtual void v32();
 virtual void v33();
 virtual void v34();
 virtual void v35();
 virtual void v36();
 virtual void v37();
 virtual void v38();
 virtual void v39();
 virtual void v40();
 virtual void RemoveParticle(unsigned short);
 int unk04;
 int unk08;
 int unk0c;
 int unk10;
 int unk14;
 int unk18;
 int unk1c;
 int unk20;
 int unk24;
 int unk28;
 int unk2c;
 int unk30;
 int unk34;
 int unk38;
 int unk3c;
 int unk40;
 int unk44;
 int unk48;
 int unk4c;
 unsigned short count; unsigned short capacity;
 int unk54;
 int unk58;
 int unk5c;
 int unk60;
 int unk64;
 int unk68;
 int unk6c;
 ParticleInfo* info;
};
struct SpawnModifier {
 virtual void v00();
 virtual void v01();
 virtual void v02();
 virtual void v03();
 virtual void v04();
 virtual void v05();
 virtual void v06();
 virtual void v07();
 virtual void v08();
 virtual void v09();
 virtual void v10();
 virtual void v11();
 virtual void v12();
 virtual void v13();
 virtual void v14();
 virtual void v15();
 virtual void v16();
 virtual void v17();
 virtual void v18();
 virtual void v19();
 virtual void v20();
 virtual void v21();
 virtual void v22();
 virtual void v23();
 virtual void v24();
 virtual void v25();
 virtual void v26();
 virtual void v27();
 virtual void v28();
 virtual void v29();
 virtual void v30();
 virtual void v31();
 virtual void v32();
 virtual void v33();
 virtual void v34();
 virtual void v35();
 virtual void v36();
 virtual void v37();
 virtual void v38();
 virtual void v39();
 virtual void v40();
 virtual void SpawnParticles(float,float,unsigned short,ParticleSystem*);
};
struct AgeDeath {
 virtual ~AgeDeath();
 int unk04,unk08,unk0c; ParticleSystem* system; int unk14; bool spawnOnDeath; SpawnModifier* spawn;
 void FUN_00c2f010(float time, ParticleSystem* particles);
};
void AgeDeath::FUN_00c2f010(float time, ParticleSystem* particles) {
 if (spawnOnDeath && spawn) {
  unsigned short info = particles->count;
  while (info > 0) {
   unsigned short index = info - 1;
   ParticleInfo* age = &particles->info[index];
   float r;
   r = time - age->lastUpdate + age->age;
   age->age = r;
   if (age->lifespan < r) {
    spawn->SpawnParticles(time, age->lifespan + time - r, index, system);
    particles->RemoveParticle(index);
   }
   --info;
  }
 } else {
  unsigned short info = particles->count;
  while (info > 0) {
   unsigned short index = info - 1;
   ParticleInfo* age = &particles->info[index];
   float r = time - age->lastUpdate + age->age;
   age->age = r;
   if (r > age->lifespan) particles->RemoveParticle(index);
   --info;
  }
 }
}
