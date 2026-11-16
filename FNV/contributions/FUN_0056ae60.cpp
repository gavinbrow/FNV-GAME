
struct SceneObject : FUN_0056af20_Class {
    int FUN_00401170();
};
struct FUN_0056ae60_Class {
    bool FUN_0056ae60();
    bool FUN_0056af40();
    SceneObject* FUN_007af430();
};
bool FUN_0056ae60_Class::FUN_0056ae60()
{
    bool result = false;
    if (!FUN_0056af40()) {
        if (FUN_007af430()) {
            switch (FUN_007af430()->FUN_00401170()) {
            case 0x2a:
            case 0x2b:
                {
                    SceneObject* object = FUN_007af430();
                    if (object) {
                        result = reinterpret_cast<ABD_005f92d0*>(reinterpret_cast<char*>(object) + 0x30)->FUN_0056af00();
                    }
                }
                break;
            case 0x1b:
                {
                    SceneObject* object = FUN_007af430();
                    if (object) {
                        result = object->FUN_0056af20();
                    }
                }
                break;
            }
        }
    }
    return result;
}
