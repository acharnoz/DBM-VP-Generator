local addonName, addon = ...
addon = LibStub("AceAddon-3.0"):NewAddon(addon, addonName)

-- called by AceAddon when Addon is fully loaded
function addon:OnInitialize()
    addon:registerSounds()
end

function addon:OnEnable()
    -- Called when the addon is enabled
end

function addon:OnDisable()
    -- Called when the addon is disabled
end

function addon:registerSounds()

    local BAA = LibStub("AceAddon-3.0"):GetAddon("BAA")

    local KEY_VOICEPACK_VAR = BAA:createEAVoicePack("KEY_VOICEPACK_NAME", KEY_EXPANSION_KEY, KEY_INSTANCE_KEY, "KEY_LANG")

KEY_SPELLS_LINES

    BAA:addEAVoicePack(KEY_VOICEPACK_VAR)

end
