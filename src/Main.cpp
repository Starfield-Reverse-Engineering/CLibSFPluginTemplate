#include "Hooks.h"
#include "Settings.h"

// SFSE message listener, use this to do stuff at specific moments during runtime
void Listener(SFSE::MessagingInterface::Message* message) noexcept
{
    switch (message->type) {
    case SFSE::MessagingInterface::kPostLoad: {
    }
    case SFSE::MessagingInterface::kPostPostLoad: {
    }
    case SFSE::MessagingInterface::kPostDataLoad: {
        Settings::LoadSettings();
        Hooks::Install();
    }
    case SFSE::MessagingInterface::kPostPostDataLoad: {
    }
    default: {
    }
    }
}

// Main SFSE plugin entry point, initialize everything here
SFSEPluginLoad(const SFSE::LoadInterface* sfse)
{
    Init(sfse);

    logger::info("{} {} is loading...", Plugin::Name, Plugin::Version.string());

    if (const auto messaging{ SFSE::GetMessagingInterface() }; !messaging->RegisterListener(Listener))
        return false;

    logger::info("{} has finished loading.", Plugin::Name);

    return true;
}
