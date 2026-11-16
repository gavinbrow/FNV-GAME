struct FUN_00872780_Class {
    int unk00;
    int unk04;
    int unk08;
    FUN_008727b0_Class* callback;
    char FUN_00872780();
};
char FUN_00872780_Class::FUN_00872780() {
    return callback ? callback->FUN_008727b0() : static_cast<char>(0);
}