#pragma once

#include <RE/Starfield.h>
#include <REL/Relocation.h>
#include <SFSE/Interfaces.h>
#include <SFSE/SFSE.h>
#include <algorithm>
#include <any>
#include <array>
#include <atomic>
#include <barrier>
#include <bit>
#include <bitset>
#include <cassert>
#include <cctype>
#include <cerrno>
#include <cfenv>
#include <cfloat>
#include <charconv>
#include <chrono>
#include <cinttypes>
#include <climits>
#include <clocale>
#include <cmath>
#include <compare>
#include <complex>
#include <concepts>
#include <condition_variable>
#include <csetjmp>
#include <csignal>
#include <cstdarg>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cuchar>
#include <cwchar>
#include <cwctype>
#include <deque>
#include <exception>
#include <execution>
#include <filesystem>
#include <forward_list>
#include <fstream>
#include <functional>
#include <future>
#include <initializer_list>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <iterator>
#include <latch>
#include <limits>
#include <locale>
#include <map>
#include <memory>
#include <memory_resource>
#include <mutex>
#include <new>
#include <numbers>
#include <numeric>
#include <optional>
#include <ostream>
#include <queue>
#include <random>
#include <ranges>
#include <ratio>
#include <regex>
#include <scoped_allocator>
#include <semaphore>
#include <set>
#include <shared_mutex>
#include <source_location>
#include <span>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <streambuf>
#include <string>
#include <string_view>
#include <syncstream>
#include <system_error>
#include <thread>
#include <tuple>
#include <type_traits>
#include <typeindex>
#include <typeinfo>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <valarray>
#include <variant>
#include <vector>
#include <version>

// clang-format off
#include <ShlObj_core.h>
#include <Psapi.h>
#include <Windows.h>
// clang-format on

#include "Plugin.h"

#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/msvc_sink.h>

using namespace std::literals;
using namespace REL::literals;

namespace logger = SFSE::log;

template <typename T>
class Singleton
{
protected:
    constexpr Singleton() noexcept  = default;
    constexpr ~Singleton() noexcept = default;

public:
    constexpr Singleton(const Singleton&)      = delete;
    constexpr Singleton(Singleton&&)           = delete;
    constexpr auto operator=(const Singleton&) = delete;
    constexpr auto operator=(Singleton&&)      = delete;

    static constexpr T* GetSingleton() noexcept
    {
        static T singleton;
        return std::addressof(singleton);
    }
};

namespace stl
{
    using namespace SFSE::stl;

    template <typename T>
    constexpr void write_thunk_call() noexcept
    {
        SFSE::AllocTrampoline(14);
        auto& trampoline{ SFSE::GetTrampoline() };
        T::func = trampoline.write_call<5>(T::address, T::Thunk);
    }

    template <typename TDest, typename TSource>
    constexpr void write_vfunc() noexcept
    {
        REL::Relocation vtbl{ TDest::VTABLE[0] };
        TSource::func = vtbl.write_vfunc(TSource::idx, TSource::Thunk);
    }

    // template <typename T>
    // constexpr void write_vfunc(const REL::VariantID variant_id) noexcept
    //{
    //     REL::Relocation<std::uintptr_t> vtbl{ variant_id };
    //     T::func = vtbl.write_vfunc(T::idx, T::Thunk);
    // }
} // namespace stl

#define SFSEPluginVersion extern "C" __declspec(dllexport) constinit SFSE::PluginVersionData SFSEPlugin_Version
