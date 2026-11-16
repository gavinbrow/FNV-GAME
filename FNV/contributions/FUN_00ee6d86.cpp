extern "C" __declspec(dllimport) int __stdcall WSAStartup(unsigned short version, void* data);
int __stdcall FUN_00ee6d86(unsigned short version, void* data) {
    return WSAStartup(version, data);
}
