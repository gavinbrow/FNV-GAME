struct CollisionMemoryRouter {
    int unk00, unk04, unk08, unk0c;
    void* allocator;
};
extern "C" int __stdcall FUN_00ca94c0(void* object);
extern "C" CollisionMemoryRouter* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void* allocator, void* array, int elementSize);

struct FUN_00d1f690_Member : hkpSimpleShapePhantom {
    void FUN_00d1f690(void* object);
};

void FUN_00d1f690_Member::FUN_00d1f690(void* object)
{
    if (*reinterpret_cast<void**>(object) != 0) {
        if (FUN_00ca94c0(object) == 0) {
            hkArray<hkpSimpleShapePhantomCollisionDetail>* details = &m_collisionDetails;
            CollisionMemoryRouter* router = FUN_00c85750();
            if (details->m_size == (details->m_capacityAndFlags & 0x3fffffff)) {
                FUN_00c90940(router->allocator, details, 4);
            }
            void** slot = reinterpret_cast<void**>(details->m_data) + details->m_size;
            ++details->m_size;
            *slot = object;
            m_orderDirty = 1;
        }
    }
}
