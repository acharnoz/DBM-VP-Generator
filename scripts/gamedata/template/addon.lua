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

    local DBMEA = LibStub("AceAddon-3.0"):GetAddon("DBMEA")

    local KEY_VOICEPACK_VAR = DBMEA:createEAVoicePack("KEY_VOICEPACK_NAME", KEY_EXPANSION_KEY, KEY_INSTANCE_KEY, "KEY_LANG")

KEY_SPELLS_LINES

    DBMEA:addEAVoicePack(KEY_VOICEPACK_VAR)

end
