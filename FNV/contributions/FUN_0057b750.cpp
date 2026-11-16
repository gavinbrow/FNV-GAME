struct Prefix_0057b750 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
};
struct SearchBase_0057b750 {
    int unk10;
    SearchBase_0057b750* FUN_0057c400(int key);
};
struct FUN_0057b750_owner : Prefix_0057b750, SearchBase_0057b750 {
    FUN_0057b750_owner* FUN_0057b750(int key);
};
FUN_0057b750_owner* FUN_0057b750_owner::FUN_0057b750(int key) {
    return static_cast<FUN_0057b750_owner*>(SearchBase_0057b750::FUN_0057c400(key));
}