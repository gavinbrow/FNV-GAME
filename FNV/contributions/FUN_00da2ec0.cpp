extern "C" void __cdecl FUN_00cb1280(void*, int, unsigned int);
extern "C" void __cdecl FUN_00cb1260(void*, const void*, unsigned int);
extern "C" int __stdcall FUN_00ee6d74(int);
extern "C" int __stdcall FUN_00ee6d6e(const char*);
extern "C" int __stdcall FUN_00ee6d68(const char*);
extern "C" int __stdcall FUN_00ee6d62(int, void*, int);
extern "C" int __cdecl FUN_00ee6d50(void);

static __declspec(noinline) bool* FUN_00da2eb0(int c, bool* out)
{
    *out = false;
    if (c >= '0' && c <= '9')
        *out = true;
    return out;
}

struct IPv4SocketAddress {
    unsigned short family;
    unsigned short port;
    unsigned int address;
    unsigned int sin_zero_low;
    unsigned int sin_zero_high;
};
struct HostEntry {
    char* name;
    char** aliases;
    short address_type;
    short address_length;
    char** addresses;
};
struct SocketConnector {
    virtual void onInitialize();
    virtual void onConnected();
    virtual void onClose();
    virtual void onRead();
    virtual void onConnectionFailure();
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int socket;
    int FUN_00da2de0();
    int FUN_00da2ec0(const char* host, int port);
};

int SocketConnector::FUN_00da2ec0(const char* host, int port)
{
    IPv4SocketAddress target;
    FUN_00cb1280(&target, 0, sizeof(target));
    target.family = 2;
    target.port = (unsigned short)FUN_00ee6d74(port);

    if (*FUN_00da2eb0(host[0], (bool*)&port))
    {
        target.address = FUN_00ee6d6e(host);
    }
    else
    {
        HostEntry* entry = (HostEntry*)FUN_00ee6d68(host);
        if (!entry) return 1;
        FUN_00cb1260(&target.address, entry->addresses[0], entry->address_length);
    }

    if (socket == -1 && FUN_00da2de0()) return 1;
    int connection = FUN_00ee6d62(socket, &target, sizeof(target));
    if (connection != -1) goto success;
    if (FUN_00ee6d50() == 0x2733) goto success;
    onConnectionFailure();
    return 1;
success: return 0;
}