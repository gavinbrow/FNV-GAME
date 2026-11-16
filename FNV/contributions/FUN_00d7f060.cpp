struct D76940Shell { void FUN_00d76940(); };
struct D7f060Owner;
struct D7f060AudioService {
    virtual void v00();
    virtual void v01();
    virtual void Release(D7f060Owner*, unsigned short);
};
struct BSAudio {
    int unk00; int unk04; int unk08; int unk0C;
    D7f060AudioService* service;
};
BSAudio* __cdecl FUN_00c85750();
struct D7f060Owner {
    int unk00;
    unsigned short soundId;
    D7f060Owner* FUN_00d7f060(unsigned int flags);
};
D7f060Owner* D7f060Owner::FUN_00d7f060(unsigned int flags)
{
    ((D76940Shell*)this)->FUN_00d76940();
    if (flags & 1) {
        BSAudio* audio = FUN_00c85750();
        audio->service->Release(this, soundId);
    }
    return this;
}
