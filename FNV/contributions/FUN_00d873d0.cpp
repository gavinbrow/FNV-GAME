struct Pair
{
    int first;
    int second;
    Pair& FUN_00d873d0(const Pair& other);
};

Pair& Pair::FUN_00d873d0(const Pair& other)
{
    first = other.first;
    second = other.second;
    return *this;
}
