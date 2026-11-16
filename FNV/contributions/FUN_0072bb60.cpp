struct MenuEntryItem { void __thiscall FUN_00700320(int action, unsigned int index); };
struct MenuEntry { MenuEntryItem* m_item; int m_unknown04; unsigned char m_disabled; };
struct EntryNode { int m_data; int m_next; MenuEntry** __thiscall FUN_006815c0(); EntryNode* __thiscall FUN_00726070(); };
struct MenuBody {
 int m_header; EntryNode m_entries; int m_unknown0c; int m_unknown10;
 int m_unknown14; int m_unknown18; unsigned short m_count;
 unsigned short m_unknown1e; float m_value;
 void __thiscall FUN_007269d0(MenuEntryItem*);
 void __thiscall FUN_0072c000(); void __thiscall FUN_0072bce0();
};
void __thiscall FUN_00729fb0_shell::FUN_0072bb60() {
 ((MenuBody*)this)->m_count = 0;
 ((MenuBody*)this)->m_value = 0.0f;
 for (EntryNode* pNode = this != 0 ? &((MenuBody*)this)->m_entries : 0;
      pNode != 0 && *pNode->FUN_006815c0() != 0;
      pNode = pNode->FUN_00726070()) {
  if ((*pNode->FUN_006815c0())->m_disabled == 0) {
   (*pNode->FUN_006815c0())->m_item->FUN_00700320(0xfac, ((MenuBody*)this)->m_count++);
   ((MenuBody*)this)->FUN_007269d0((*pNode->FUN_006815c0())->m_item);
  }
 }
 ((MenuBody*)this)->FUN_0072c000();
 ((MenuBody*)this)->FUN_0072bce0();
}