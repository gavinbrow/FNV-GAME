struct PlaneInput { NiPoint3 normal; float distance; };
struct NormalProxy { float x,y,z; float FUN_00457910(); };
struct HalfSpaceProxy : NiHalfSpaceBV { NormalProxy normal; float distance; void FUN_00e9cbb0(const PlaneInput* source); };
void HalfSpaceProxy::FUN_00e9cbb0(const PlaneInput* source) {
NormalProxy normalized = *reinterpret_cast<const NormalProxy*>(&source->normal);
 const double originalDistance = source->distance;
 float adjustedDistance = static_cast<float>(originalDistance / normalized.FUN_00457910());
 normal = normalized;
 distance = adjustedDistance;}