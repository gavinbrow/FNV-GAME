struct Particle { NiPoint3 velocity; float rotation; float size; float age; float lifetime; };
struct ParticleData {
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
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned short activeCount;
    unsigned short unk52;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    Particle* particles;
};
struct DragFieldFields {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    float damping;
};
void __fastcall FUN_00c2c830(DragFieldFields* self, void*, float deltaTime, ParticleData* data)
{
    for (unsigned short i = 0; i < data->activeCount; ++i) {
        Particle& p = data->particles[i];
        float alpha = (deltaTime - p.age) * self->damping;
        if (alpha < 1.0f) {
            float factor = 1.0f - alpha;
            p.velocity.x *= factor;
            p.velocity.y *= factor;
            p.velocity.z *= factor;
        } else {
            p.velocity = _NiPoint3_ZERO;
        }
    }
}
