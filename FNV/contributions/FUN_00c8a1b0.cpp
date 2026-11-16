extern __declspec(thread) int DAT_tls_field;
struct hkReferencedObject { void removeReference(); };
struct FUN_009ba5f0_shell { void FUN_00c89ac0(int); void FUN_00c8a1b0(hkReferencedObject*, int); };
struct TlsGuard { int old; TlsGuard() : old(DAT_tls_field) { DAT_tls_field = 16; } ~TlsGuard() { DAT_tls_field = old; } };
void FUN_009ba5f0_shell::FUN_00c8a1b0(hkReferencedObject* object, int unused)
{
    TlsGuard guard;
    FUN_00c89ac0((int)object);
    object->removeReference();
}