struct VehicleStatus {
    void* unk00;
    int unk04;
    int unk08;
    int unk0c;
    unsigned char unk10;
};

struct VehicleOutput {
    float x;
    float y;
    float z;
    unsigned char autoReverse;
    unsigned char buttonPressed;
};

struct ButtonResult {
    unsigned char value;
};

struct VehicleInput {
    virtual void virtual0();
    virtual void virtual1();
    virtual void virtual2();
    virtual void virtual3();
    virtual float calculateX(float timeStep, void* vehicle, VehicleStatus* status, VehicleOutput* output);
    virtual float calculateY(float timeStep, void* vehicle, VehicleStatus* status, VehicleOutput* output);
    virtual ButtonResult calculateButton(float timeStep, void* vehicle, VehicleStatus* status, VehicleOutput* output);
    virtual float calculateZ(float timeStep, void* vehicle, VehicleStatus* status, VehicleOutput* output);
    void FUN_00e435f0(float timeStep, void* vehicle, VehicleStatus* status, VehicleOutput* output);
};

void VehicleInput::FUN_00e435f0(float timeStep, void* vehicle, VehicleStatus* status, VehicleOutput* output) {
    output->x = calculateX(timeStep, vehicle, status, output);
    output->y = calculateY(timeStep, vehicle, status, output);
    output->z = calculateZ(timeStep, vehicle, status, output);
    output->autoReverse = status->unk10;
    output->buttonPressed = calculateButton(timeStep, vehicle, status, output).value;
}