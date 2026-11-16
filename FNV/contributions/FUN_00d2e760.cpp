void FUN_00d2e680();
void FUN_00d2e970();
void FUN_00d2e9b0();
void FUN_00d2e9f0();
void FUN_00d2df50();

void FUN_00d31110();
void FUN_00d30f50();
struct Conversion { void (*convert)(); void (*create)(); void (*copy)(); void (*destroy)(); bool enabled; bool supported; };
struct Registry { void FUN_00cfbbe0(Conversion*,int,int); };
void FUN_00d2e760(Registry* registry) {
 Conversion conversion;
 conversion.convert=FUN_00d2e680;
 conversion.create=FUN_00d2e970;
 conversion.copy=FUN_00d2e9b0;
 conversion.destroy=FUN_00d2e9f0;
 conversion.enabled=true;
 conversion.supported=true;
 registry->FUN_00cfbbe0(&conversion,8,24);
 conversion.convert=FUN_00d2df50;
 conversion.create=(void(*)())FUN_00d312f0;
 conversion.copy=FUN_00d31110;
 conversion.destroy=FUN_00d30f50;
 conversion.enabled=false;
 conversion.supported=true;
 registry->FUN_00cfbbe0(&conversion,24,8);
}

