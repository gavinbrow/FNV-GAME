void __cdecl FUN_00e592a0(float* p, unsigned int n)
{
    float sum = *p;
    float* q = p + 1;
    unsigned int i = 1;

    if ((int)(n - 1) >= 4)
    {
        unsigned int blocks = ((n - 5) >> 2) + 1;
        i = blocks * 4 + 1;
        do
        {
            float u0 = *q + sum;
            q += 4;
            q[-4] = u0;
            float u1 = q[-3] + u0;
            q[-3] = u1;
            float u2 = q[-2] + u1;
            q[-2] = u2;
            float u3 = q[-1] + u2;
            q[-1] = u3;
            sum = u3;
        } while (--blocks != 0);
    }

    if (i < n)
    {
        unsigned int rem = n - i;
        do
        {
            float t = *q + sum;
            *q = t;
            sum = t;
            ++q;
        } while (--rem != 0);
    }
}