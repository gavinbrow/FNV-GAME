#include <typeinfo>
type_info::~type_info() { _Type_info_dtor(this); }
