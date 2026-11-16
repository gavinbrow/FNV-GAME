inline void SwapByte(unsigned char& left, unsigned char& right)
{
    unsigned char temporary = left;
    left = right;
    right = temporary;
}
void __cdecl FUN_00e53000(unsigned char* bytes)
{
    SwapByte(bytes[0], bytes[1]);
    SwapByte(bytes[2], bytes[3]);
    SwapByte(bytes[4], bytes[5]);
}