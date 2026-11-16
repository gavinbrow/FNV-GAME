
struct FUN_00cb0b80 { char* m_string; FUN_00cb0b80(const char* s) throw(); };
template <typename T> struct hkArrayE466 { T* m_data; int m_size; int m_capacityAndFlags; hkArrayE466() : m_data(0), m_size(0), m_capacityAndFlags(0x80000000) {} };

class hkRefObjE466 {
public:
   virtual ~hkRefObjE466();
   unsigned short m_memSizeAndFlags;
   short m_referenceCount;
   hkRefObjE466() { m_referenceCount = 1; }
};
class FUN_00e46660 : public hkRefObjE466 {
public:
  volatile unsigned char m_type;
  char unk09, unk0A, unk0B;
  FUN_00cb0b80 m_name;
  unsigned char m_keyboardKey;
  char unk11,unk12,unk13;
  hkArrayE466<void*> m_listeners;
  FUN_00e46660();
  virtual ~FUN_00e46660();
};
FUN_00e46660::FUN_00e46660() : m_type(0), m_name(""), m_keyboardKey(0x71) {}
