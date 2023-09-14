#pragma once

#define SFSEPluginVersion extern "C" __declspec(dllexport) constinit SFSE::PluginVersionData SFSEPlugin_Version

namespace Plugin
{
    using namespace std::string_view_literals;

    static constexpr auto Name{ "PluginName"sv };
    static constexpr auto Author{ "AuthorName"sv };
    static constexpr auto Version{
        REL::Version{0, 0, 1, 0}
    };
} // namespace Plugin

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
