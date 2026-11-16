struct NiFileAccessRequest { unsigned int value0, operation, reserved0, name, value10, reserved1, result; };
void __cdecl CompleteJob(NiFileAccessRequest* request);
// @fnv 0x00aa8610
unsigned int __cdecl FUN_00aa8610(unsigned int param1, unsigned int param2, unsigned int param3, unsigned int param4)
{
    NiFileAccessRequest request;
    request.value0 = 0;
    request.operation = 0;
    request.name = 0;
    request.reserved1 = 0;
    request.operation = 2;
    request.value0 = param4;
    request.name = param1;
    request.value10 = param3;
    CompleteJob(&request);
    return request.result;
}