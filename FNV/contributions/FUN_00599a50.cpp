struct LayerInfo {
    BSStringT<char> Name;
    float Attenuation;
    float Percent;

    const char* __thiscall FUN_00559450(unsigned int index);
    int __thiscall FUN_00408a80(const char* text);
    bool __thiscall FUN_00599a50(LayerInfo other);
};
bool LayerInfo::FUN_00599a50(LayerInfo other)
{
    if (Attenuation != other.Attenuation)
        return true;
    if (Percent != other.Percent)
        return true;
    if (FUN_00408a80(other.FUN_00559450(0)))
        return false;
    return true;
}