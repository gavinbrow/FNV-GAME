#include <math.h>
extern "C" float g_010be824;
struct CollisionVector {
    float x, y, z;
    CollisionVector() {}
    CollisionVector(float a, float b, float c) : x(a), y(b), z(c) {}
    CollisionVector operator-(const CollisionVector& b) const {
        return CollisionVector(x-b.x, y-b.y, z-b.z);
    }
    CollisionVector operator+(const CollisionVector& b) const {
        return CollisionVector(x+b.x, y+b.y, z+b.z);
    }
    CollisionVector operator*(float s) const {
        return CollisionVector(x*s, y*s, z*s);
    }
    float operator*(const CollisionVector& b) const {
        return x*b.x + y*b.y + z*b.z;
    }
    float SquaredLength() const { return (*this) * (*this); }
};
struct CollisionParticle {
    CollisionVector velocity;
    float age, lifespan, lastUpdate, generation;
};
struct CollisionParticles {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    CollisionVector* positions;
    int unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c;
    int unk60, unk64, unk68, unk6c;
    CollisionParticle* particles;
};
struct SphereCollision {
    int unk00, unk04, unk08, unk0c, unk10;
    CollisionVector hitPoint;
    float hitTime;
    ColliderOwner* owner;
    ColliderNext* next;
    ColliderNode* node;
    float radius, scaledRadius, squaredRadius;
    CollisionVector center;
    SphereCollision* FUN_00c32450(float, float&, CollisionParticles*, unsigned short);
    SphereCollision* FUN_00c27b40(float, float&, CollisionParticles*, unsigned short);
};
SphereCollision* SphereCollision::FUN_00c27b40(float time, float& earliest, CollisionParticles* data, unsigned short index) {
    bool hit = false;
    const CollisionVector& position = data->positions[index];
    const CollisionVector& velocity = data->particles[index].velocity;
    CollisionVector difference = position - center;
    float c = difference.SquaredLength() - squaredRadius;
    bool inside = -c > g_010be824;
    if (inside || c > g_010be824) {
        float projection = -(difference * velocity);
        if (inside || projection > 0.0f) {
            float speedSquared = velocity.SquaredLength();
            float t = projection / speedSquared;
            difference = (position + velocity * t) - center;
            const CollisionVector& relative = difference;
            float distanceSquared = relative.SquaredLength();
            if (inside || distanceSquared < squaredRadius) {
                float delta = squaredRadius - distanceSquared;
                if (inside) t += sqrtf(delta / speedSquared);
                else t -= sqrtf(delta / speedSquared);
                if (t < earliest - time) {
                    hit = true;
                    float collisionTime = time + t;
                    hitTime = earliest = collisionTime;
                    hitPoint = position + velocity * t;
                }
            }
        }
    }
    SphereCollision* result = FUN_00c32450(time, earliest, data, index);
    return result ? result : (hit ? this : 0);
}
