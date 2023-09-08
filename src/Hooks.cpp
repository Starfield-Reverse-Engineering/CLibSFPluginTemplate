#include "Hooks.h"

namespace Hooks
{
    void Install()
    {
        stl::write_thunk_call<MainUpdate>();
        logger::info("Installed main update hook");
    }

    std::int32_t MainUpdate::thunk()
    {
        return func();
    }
} // namespace Hooks
