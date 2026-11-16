void FUN_00a62150(void* buffer, int words);
struct Vector3 { float x; float y; float z; };
void __cdecl FUN_00cf0930(void* buffer, int bytes, Vector3* vector)
{
 int words = bytes / 4;
 FUN_00a62150(buffer, words);
 char savedBytes[sizeof(Vector3)];
 Vector3* saved = reinterpret_cast<Vector3*>(savedBytes);
 *saved = *vector;
 FUN_00a62150(buffer, words);
 *vector = *saved;
}

