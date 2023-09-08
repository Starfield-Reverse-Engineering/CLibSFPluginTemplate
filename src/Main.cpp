#include "Events.h"
#include "Hooks.h"
#include "Logging.h"
#include "Settings.h"

#include "SFSE/Interfaces.h"

void Listener(SFSE::MessagingInterface::Message* message)
{
    if (message->type <=> SFSE::MessagingInterface::kDataLoaded == 0)
    {
        Settings::LoadSettings();
        Hooks::Install();
    }
}

SFSEPluginLoad(const SFSE::LoadInterface* skse)
{
    InitializeLogging();

    const auto plugin{ SFSE::PluginDeclaration::GetSingleton() };
    const auto version{ plugin->GetVersion() };

    logger::info("{} {} is loading...", plugin->GetName(), version);

    Init(skse);

    if (const auto messaging{ SFSE::GetMessagingInterface() }; !messaging->RegisterListener(Listener))
        return false;

    logger::info("{} has finished loading.", plugin->GetName());

    return true;
}
