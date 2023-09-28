#include "Settings.h"

void Settings::LoadSettings() noexcept
{
    logger::info("Loading settings");

    CSimpleIniA ini;

    ini.SetUnicode();
    if (ini.LoadFile(R"(.\Data\SFSE\Plugins\PluginName.ini)") <=> 0 < 0) {
        logger::error("ERROR: Failed to load ini");
        return;
    }

    debug_logging = ini.GetBoolValue("Log", "Debug");

    if (debug_logging) {
        spdlog::set_level(spdlog::level::level_enum::debug);
        logger::debug("Debug logging enabled");
    }

    // Load settings (see simpleini readme: https://github.com/brofield/simpleini)

    logger::info("Loaded settings");
}
