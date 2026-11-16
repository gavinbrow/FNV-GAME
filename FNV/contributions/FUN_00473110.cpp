struct FUN_00473180_shell {
    unsigned int __thiscall FUN_00473180(void* buffer, unsigned int size);
};

struct FUN_00473110_shell {
    TES_RETURN_CODE m_lastError;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FUN_00473180_shell* m_pFile;

    TES_RETURN_CODE __thiscall FUN_00473110(void* buffer, unsigned int size);
};

unsigned int __thiscall FUN_00473180_shell::FUN_00473180(void* buffer, unsigned int size)
{
    return 0;
}

int* __cdecl FUN_00ec85e3();
void __cdecl FUN_005b5e40(const char* message);
extern const char DAT_0101a174[];

TES_RETURN_CODE __thiscall FUN_00473110_shell::FUN_00473110(void* buffer, unsigned int size)
{
    if (buffer != 0) {
        if (m_pFile->FUN_00473180(buffer, size) < size) {
            int error = *FUN_00ec85e3();
            m_lastError = TES_RETURN_CODE_TES_ERROR_WRITE_FAILURE;
            FUN_005b5e40(DAT_0101a174);
            return m_lastError;
        }
    }

    m_lastError = TES_RETURN_CODE_TES_ERROR_NONE;
    return m_lastError;
}