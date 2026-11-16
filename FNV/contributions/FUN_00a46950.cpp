inline void* operator new(unsigned int, void* storage) throw()
{
    return storage;
}

NiTextureTransformController* __cdecl FUN_00a46950()
{
    void* storage = _NiMalloc(sizeof(NiTextureTransformController));
    if (storage != 0)
        return new (storage) NiTextureTransformController(0, 0, NiTextureTransformController__TransformMember_TT_TRANSLATE_U);
    return 0;
}