#pragma once

// Define your hook classes here
namespace Hooks
{
    void Install() noexcept;

    enum class FIGHT_REACTION
    {
        kNeutral = 0,
        kEnemy,
        kAlly,
        kFriend
    };

    // Example hook from https://github.com/powerof3/SimpleOffenceSuppressionSFSE
    class GetFactionFightReaction : public Singleton<GetFactionFightReaction>
    {
    public:
        static FIGHT_REACTION thunk(RE::Actor* a_subject, RE::Actor* a_player)
        {
            const auto fightReaction{ func(a_subject, a_player) };

            return fightReaction;
        }

        inline static REL::Relocation<decltype(thunk)> func;
    };
} // namespace Hooks
