struct SearchObject {
    unsigned int field00;
    int FUN_00d87320(unsigned int arg0);
};
int SearchObject::FUN_00d87320(unsigned int arg0)
{
    return (int)((arg0 << (6u & 31u)) + field00);
}
