#include "Hooks.h"
#include "Logging.h"
#include "Settings.h"

void Listener(SFSE::MessagingInterface::Message* message) noexcept
{
    if (message->type <=> SFSE::MessagingInterface::kPostPostLoad == 0)
    {
        Settings::LoadSettings();
        Hooks::Install();
    }
}

SFSEPluginLoad(const SFSE::LoadInterface* sfse)
{
    InitializeLogging();

    logger::info("{} {} is loading...", Plugin::Name, Plugin::Version);

    Init(sfse);

    if (const auto messaging{ SFSE::GetMessagingInterface() }; !messaging->RegisterListener(Listener))
        return false;

    logger::info("{} has finished loading.", Plugin::Name);

    return true;
}

SFSEPluginVersion = []() noexcept {
    SFSE::PluginVersionData data{};

    data.PluginVersion(Plugin::Version);
    data.PluginName(Plugin::Name);
    data.AuthorName(Plugin::Author);
    data.UsesSigScanning(false);
    data.HasNoStructUse(true);
    data.CompatibleVersions({ SFSE::RUNTIME_LATEST });

    return data;
}();
