
struct BasePart : FUN_00b02b70_shell {
 ~BasePart();
};
struct RotationPart : FUN_00b02c90_class {
 ~RotationPart();
};
struct DataPart : FUN_00b02dc0_class {
 ~DataPart();
};
struct FUN_00b029f0 : BasePart {
 float m_38;
 BasePart m_3c;
 float m_74;
 RotationPart m_78;
 RotationPart m_b4;
 DataPart m_f0;
 DataPart m_104;
 DataPart m_118;
 FUN_00b029f0();
};
FUN_00b029f0::FUN_00b029f0() : m_38(-1.0f), m_74(-1.0f) {}
