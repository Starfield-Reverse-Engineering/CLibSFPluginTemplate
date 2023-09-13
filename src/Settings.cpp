#include "Settings.h"

void Settings::LoadSettings() noexcept
{
    logger::info("Loading settings");

    CSimpleIniA ini;

    ini.SetUnicode();
    if (ini.LoadFile(R"(.\Data\SFSE\Plugins\PluginName.ini)") <=> 0 < 0)
    {
        logger::error("ERROR: Failed to load ini");
        return;
    }

    debug_logging = ini.GetBoolValue("Log", "Debug");

    if (debug_logging)
    {
        spdlog::get("Global")->set_level(spdlog::level::level_enum::debug);
        logger::debug("Debug logging enabled");
    }

    // Load settings

    logger::info("Loaded settings");
}
