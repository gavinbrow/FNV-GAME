struct CheckInterface {virtual void unused();virtual unsigned char* evaluate(int*,int,int,int,int,int);};
struct FilterDelegate {int unk00; int unk04; int unk08; CheckInterface callback;};
struct FilterResult {bool value; FilterResult(bool v):value(v){} };
struct ConstraintFilter{int unk00,unk04,unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24;FilterDelegate* delegate;
FilterResult FUN_00e46cf0(int,int,int,int,int);};
FilterResult ConstraintFilter::FUN_00e46cf0(int a2,int a3,int a4,int a5,int a6){
 FilterDelegate* const& ref = delegate;
 return FilterResult(ref == 0 || *delegate->callback.evaluate(&a6,a2,a3,a4,a5,a6) !=0);}