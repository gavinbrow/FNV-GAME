struct AdjacentObjects {
    FUN_00cb0c00_class first;
    __declspec(align(4)) FUN_00cb0c00_class second;
};

void __cdecl FUN_00dfdab0(AdjacentObjects* objects)
{
    objects->second.FUN_00cb0c00();
    objects->first.FUN_00cb0c00();
}