extern volatile long DAT_011f4400;
extern const char* _EmptyFS;
struct FixedStringBase { virtual void Release(); unsigned int m_unknown04; FixedStringBase(); };
FixedStringBase::FixedStringBase() : m_unknown04(0) { InterlockedIncrement(&DAT_011f4400); }
struct StringValue { const char* value; StringValue():value(_EmptyFS){} };
struct MemberCount { unsigned int m_size; unsigned int m_capacity; unsigned int m_flags; MemberCount():m_size(0),m_capacity(0),m_flags(0){} };
struct FUN_00eea580 : FixedStringBase {
 StringValue m_first,m_second,m_third,m_fourth,m_fifth;
 unsigned int m_initialized;
 MemberCount m_counts;
 FUN_00eea580();
 virtual void Release();
};
FUN_00eea580::FUN_00eea580() { m_initialized=1; }
