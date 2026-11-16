extern const double DAT_010241b0;
BSSimpleList<TESRegionPoint*>* __fastcall FUN_00726070(BSSimpleList<TESRegionPoint*>*);
struct FUN_004f8030_shell : TESRegionPointList { float FUN_004f8030(); };
float FUN_004f8030_shell::FUN_004f8030() {
 float fMaximum = DAT_01015f5c;
 BSSimpleList<TESRegionPoint*>* pkPoint = this;
 if (Maximums.y > DAT_010241b0) return Maximums.y;
 while (pkPoint && _ref_006815c0(pkPoint)) {
  if (fMaximum < _ref_006815c0(pkPoint)->GetY()) fMaximum = _ref_006815c0(pkPoint)->GetY();
  pkPoint = FUN_00726070(pkPoint);
 }
 return fMaximum;
}