bool __cdecl FUN_005accb0(void*,void*,void*,void*,void*,void*,void*,float*,float*,float*,unsigned int*);
void __cdecl FUN_007e4fe0(float,float,float);
bool __cdecl FUN_005bb4f0(void* context,void* scriptData,void* firstValue,void* secondValue,void* thirdValue,void* fourthValue,void* unusedArgument,void* lastArgument)
{
    float a;
    float c;
    float d;
    unsigned int b;
    a = 0.0f;
    d = 0.0f;
    c = 1.0f;
    if (!FUN_005accb0(context,scriptData,lastArgument,firstValue,secondValue,thirdValue,fourthValue,&a,&d,&c,&b)) return false;
    FUN_007e4fe0(a,d,c);
    return true;
}