struct OperationPacket {
    unsigned char operation;
    void* target;
    unsigned int value;
};
struct CommandTarget {
    virtual void Reserved0();
    virtual void Reserved1();
    virtual void Reserved2();
    virtual void Receive(unsigned int value);
};
struct CommandDispatcher {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    void FUN_00c91160(OperationPacket* packet);
    CommandTarget* FUN_00c92a30(CommandTarget* target, unsigned int value);
};
CommandTarget* CommandDispatcher::FUN_00c92a30(CommandTarget* target, unsigned int value)
{
    if (unk94) {
        OperationPacket packet;
        packet.operation = 0x24;
        packet.target = target;
        packet.value = value;
        FUN_00c91160(&packet);
    } else {
        target->Receive(value);
    }
    return target;
}
