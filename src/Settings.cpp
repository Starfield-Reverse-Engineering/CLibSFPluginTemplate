#include "Settings.h"

void Settings::LoadSettings()
{
    logger::info("Loading settings");

    CSimpleIniA ini;

    ini.SetUnicode();
    ini.LoadFile(R"(.\Data\SFSE\Plugins\PluginName.ini)");

    debug_logging = ini.GetBoolValue("Log", "Debug");

    if (debug_logging)
    {
        spdlog::get("Global")->set_level(spdlog::level::level_enum::debug);
        logger::debug("Debug logging enabled");
    }

    // Load settings

    logger::info("Loaded settings");
}
