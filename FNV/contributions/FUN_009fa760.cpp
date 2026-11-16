int __stdcall FUN_009fa760(void* obj, int* current, int* stop)
{
    if (!(((unsigned char*)obj)[4] & 0x20))
        return 0x80040251;

    int* p = (int*)obj;
    *(__int64*)current = *(__int64*)(p + 12);
    *(__int64*)stop = (__int64)p[14] + *(__int64*)(p + 12);
    return 0;
}
