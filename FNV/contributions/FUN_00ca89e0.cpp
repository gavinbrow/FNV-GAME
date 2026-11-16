struct PositionCommand {
    unsigned char opcode;
    void* sender;
    float x;
    float y;
    float z;
};

struct PositionQueue {
    void FUN_00c91160(PositionCommand* command);
};

struct PositionOwner {
    int unk00;
    int unk04;
    PositionQueue* queue;

    void FUN_005616d0(float* position);
    void FUN_00ca89e0(float* position);
};

void PositionOwner::FUN_00ca89e0(float* position)
{
    PositionQueue* active = queue;
    if (active && *(int*)((char*)active + 0x94)) {
        PositionCommand command;
        command.sender = this;
        command.opcode = 0x19;
        command.x = position[0];
        command.y = position[1];
        command.z = position[2];
        active->FUN_00c91160(&command);
    } else {
        FUN_005616d0(position);
    }
}