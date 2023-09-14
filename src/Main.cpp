#include "Hooks.h"
#include "Settings.h"

// SFSE message listener, use this to do stuff at specific moments during runtime
// NOTE: Currently, only kPostPostLoad is available
void Listener(SFSE::MessagingInterface::Message* message) noexcept
{
    if (message->type <=> SFSE::MessagingInterface::kPostPostLoad == 0)
    {
        Settings::LoadSettings();
        Hooks::Install();
    }
}

// Main SFSE plugin entry point, initialize everything here
SFSEPluginLoad(const SFSE::LoadInterface* sfse)
{
    logger::info("{} {} is loading...", Plugin::Name, Plugin::Version.string("."sv));

    Init(sfse);

    if (const auto messaging{ SFSE::GetMessagingInterface() }; !messaging->RegisterListener(Listener))
        return false;

    logger::info("{} has finished loading.", Plugin::Name);

    return true;
}

// Tell SFSE about this plugin
SFSEPluginVersion = []() noexcept {
    SFSE::PluginVersionData data{};

    data.PluginVersion(Plugin::Version.pack());
    data.PluginName(Plugin::Name);
    data.AuthorName(Plugin::Author);
    data.UsesSigScanning(true);
    data.HasNoStructUse(true);
    data.CompatibleVersions({ SFSE::RUNTIME_LATEST });

    return data;
}();
