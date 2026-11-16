struct E58E80Object {
    void FUN_00e58df0(int setting);
};
E87E0Matrix* __fastcall FUN_00e58e80(int setting, int unused, E58E80Object* object, const E87E0Matrix& right) {
    object->FUN_00e58df0(setting);
    E87E0Matrix* matrix = reinterpret_cast<E87E0Matrix*>(object);
    matrix->FUN_00e587e0(right);
    return matrix;
}