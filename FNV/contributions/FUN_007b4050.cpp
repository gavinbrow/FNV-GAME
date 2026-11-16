struct FUN_007b4050_shell {
int unknown00,unknown04,unknown08,currentValue,previousValue; TGF* control;
void FUN_007b4050(FUN_007b4050_shell* other);
};
void FUN_007b4050_shell::FUN_007b4050(FUN_007b4050_shell* other) {
previousValue = (unsigned int)other->control->GetFloat(0x1004);
other->currentValue = (unsigned int)control->GetFloat(0x1004);
}