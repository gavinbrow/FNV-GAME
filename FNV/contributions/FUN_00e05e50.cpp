namespace std {
template <class T>
inline void swap(T& a, T& b)
{
    T temp = a;
    a = b;
    b = temp;
}
}

void __cdecl FUN_00e05de0(unsigned char* p);

void __cdecl FUN_00e05e50(unsigned char* p)
{
    std::swap(p[4], p[7]);
    std::swap(p[5], p[6]);
    std::swap(p[8], p[11]);
    std::swap(p[9], p[10]);
    std::swap(p[12], p[15]);
    std::swap(p[13], p[14]);

    return FUN_00e05de0(p + 16);
}