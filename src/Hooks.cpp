#include "Hooks.h"

namespace Hooks
{
    void Install() noexcept
    {
        REL::Relocation target{ REL::ID(151616), 0x22f };
        stl::write_thunk_call<GetFactionFightReaction>(target.address());
    }
} // namespace Hooks
