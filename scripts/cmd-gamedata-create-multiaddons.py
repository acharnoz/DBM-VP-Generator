from pathlib import Path
import argparse


from gamedata import cmdgamedata

parser = argparse.ArgumentParser(description="Script to explore wow game data and save the file in the repository db")
parser.add_argument("--lang", "-l", type=str, help="Set the dictionnary lang (e.g. en, fr, de, etc)", required=True)
parser.add_argument("--gamedatadbpath", "-gdbp", type=Path, help="Path to import gamedata db (dir)", required=True)
parser.add_argument("--addondbpath", "-adbp", type=Path, help="Path to export addon(s) (dir)", required=True)
parser.add_argument("--generatesounds", "-gs", type=bool, help="Path to export addon(s) (dir)", required=False, default=False)

args = parser.parse_args()

generate_current_content = True
generate_vault_of_the_incarnates_content = True
generate_shadowlands_content = True
generate_bfa_content = True
generate_legion_content = True
generate_wod_content = True

#langs = [args.lang]
langs = ["EN","FR","DE","IT","ES"]

for lang in langs:

    # BAA-CurrentContent
    # 503:Dragonflight
    # --Dungeon
    # ----1201:Algeth'ar Academy
    # ----1196:Brackenhide Hollow
    # ----1204:Halls of Infusion
    # ----1199:Neltharus
    # ----1202:Ruby Life Pools
    # ----1203:The Azure Vault
    # ----1198:The Nokhud Offensive
    # ----1197:Uldaman: Legacy of Tyr
    # --Raid
    # ----1205:Dragon Isles
    # ----1200:Vault of the Incarnates
    if generate_current_content :
        current_content_dungeon = ["1201","1196","1204","1199","1202","1203","1198","1197","1205"]
        current_content_raid = ["1200"]
        current_content_s1 = ["721", "800", "537", "313"]
        isntance_keys=[]
        isntance_keys.extend(current_content_dungeon)
        isntance_keys.extend(current_content_raid)
        isntance_keys.extend(current_content_s1)
        cmdgamedata.create_addon_from_ids(isntance_keys, lang, args.gamedatadbpath, args.addondbpath,"BAA-CurrentContent","Current Content")

    # BAA-VaultOfTheIncarnates
    # 503:Dragonflight
    # --Raid
    # ----1200:Vault of the Incarnates
    if generate_vault_of_the_incarnates_content:
        cmdgamedata.create_addon_from_ids(["1200"], lang, args.gamedatadbpath, args.addondbpath,"BAA-VaultOfTheIncarnates","Vault of the Incarnates", args.generatesounds)

    # BAA-ShadowlandsDungeons
    # 499:Shadowlands
    # --Dungeon
    # ----1188:De Other Side
    # ----1185:Halls of Atonement
    # ----1184:Mists of Tirna Scithe
    # ----1183:Plaguefall
    # ----1189:Sanguine Depths
    # ----1186:Spires of Ascension
    # ----1194:Tazavesh, the Veiled Market
    # ----1182:The Necrotic Wake
    # ----1187:Theater of Pain
    # --Raid
    # ----1190:Castle Nathria
    # ----1193:Sanctum of Domination
    # ----1195:Sepulcher of the First Ones
    if generate_shadowlands_content:
        shadowlands_content_dungeon=["1188","1185","1184","1183","1189","1186","1194","1182","1187"]
        cmdgamedata.create_addon_from_ids(shadowlands_content_dungeon, lang, args.gamedatadbpath, args.addondbpath,"BAA-ShadowlandsDungeons","Shadowlands Dungeons", args.generatesounds)

    # BAA-BattleForAzerothDungeons
    # 396:Battle for Azeroth
    # --Dungeon
    # ----968:Atal'Dazar
    # ----1001:Freehold
    # ----1041:Kings' Rest
    # ----1178:Operation: Mechagon
    # ----1036:Shrine of the Storm
    # ----1023:Siege of Boralus
    # ----1030:Temple of Sethraliss
    # ----1012:The MOTHERLODE!!
    # ----1022:The Underrot
    # ----1002:Tol Dagor
    # ----1021:Waycrest Manor
    # --Raid
    # ----1031:Uldir
    # ----1176:Battle of Dazar'alor
    # ----1177:Crucible of Storms
    # ----1179:The Eternal Palace
    # ----1180:Ny'alotha, the Waking City
    if generate_bfa_content:
        bfa_content_dungeon=["968","1001","1041","1178","1036","1023","1030","1012","1022","1002","1021"]
        cmdgamedata.create_addon_from_ids(bfa_content_dungeon, lang, args.gamedatadbpath, args.addondbpath,"BAA-BattleForAzerothDungeons","Battle for Azeroth Dungeons", args.generatesounds)

    # BAA-LegionDungeons
    # 395:Legion
    # --Dungeon
    # ----777:Assault on Violet Hold
    # ----740:Black Rook Hold
    # ----900:Cathedral of Eternal Night
    # ----800:Court of Stars
    # ----762:Darkheart Thicket
    # ----716:Eye of Azshara
    # ----721:Halls of Valor
    # ----727:Maw of Souls
    # ----767:Neltharion's Lair
    # ----860:Return to Karazhan
    # ----945:Seat of the Triumvirate
    # ----726:The Arcway
    # ----707:Vault of the Wardens
    # --Raid
    # ----768:The Emerald Nightmare
    # ----861:Trial of Valor
    # ----786:The Nighthold
    # ----875:Tomb of Sargeras
    # ----946:Antorus, the Burning Throne
    # ----959:Invasion Points
    if generate_legion_content:
        legion_content_dungeon=["777","740","900","800","762","716","721","727","767","860","945","726","707"]
        cmdgamedata.create_addon_from_ids(legion_content_dungeon, lang, args.gamedatadbpath, args.addondbpath,"BAA-LegionDungeons","Legion Dungeons", args.generatesounds)

    # BAA-WarlordsOfDraenorDungeons
    # 124:Warlords of Draenor
    # --Dungeon
    # ----547:Auchindoun
    # ----385:Bloodmaul Slag Mines
    # ----536:Grimrail Depot
    # ----558:Iron Docks
    # ----537:Shadowmoon Burial Grounds
    # ----476:Skyreach
    # ----556:The Everbloom
    # ----559:Upper Blackrock Spire
    # --Raid
    # ----477:Highmaul
    # ----457:Blackrock Foundry
    # ----669:Hellfire Citadel
    if generate_wod_content:
        wod_content_dungeon=["547","385","536","558","537","476","476","556","559"]
        cmdgamedata.create_addon_from_ids(wod_content_dungeon, lang, args.gamedatadbpath, args.addondbpath,"BAA-WarlordsOfDraenorDungeons","Warlords of Draenor Dungeons", args.generatesounds)


    # 68:Classic
    # --Dungeon
    # ----227:Blackfathom Deeps
    # ----228:Blackrock Depths
    # ----63:Deadmines
    # ----230:Dire Maul
    # ----231:Gnomeregan
    # ----229:Lower Blackrock Spire
    # ----232:Maraudon
    # ----226:Ragefire Chasm
    # ----233:Razorfen Downs
    # ----234:Razorfen Kraul
    # ----311:Scarlet Halls
    # ----316:Scarlet Monastery
    # ----246:Scholomance
    # ----64:Shadowfang Keep
    # ----236:Stratholme
    # ----238:The Stockade
    # ----237:The Temple of Atal'hakkar
    # ----239:Uldaman
    # ----240:Wailing Caverns
    # ----241:Zul'Farrak
    # --Raid
    # ----741:Molten Core
    # ----742:Blackwing Lair
    # ----743:Ruins of Ahn'Qiraj
    # ----744:Temple of Ahn'Qiraj
    # 70:Burning Crusade
    # --Dungeon
    # ----247:Auchenai Crypts
    # ----248:Hellfire Ramparts
    # ----249:Magisters' Terrace
    # ----250:Mana-Tombs
    # ----251:Old Hillsbrad Foothills
    # ----252:Sethekk Halls
    # ----253:Shadow Labyrinth
    # ----254:The Arcatraz
    # ----255:The Black Morass
    # ----256:The Blood Furnace
    # ----257:The Botanica
    # ----258:The Mechanar
    # ----259:The Shattered Halls
    # ----260:The Slave Pens
    # ----261:The Steamvault
    # ----262:The Underbog
    # --Raid
    # ----745:Karazhan
    # ----746:Gruul's Lair
    # ----747:Magtheridon's Lair
    # ----748:Serpentshrine Cavern
    # ----749:The Eye
    # ----750:The Battle for Mount Hyjal
    # ----751:Black Temple
    # ----752:Sunwell Plateau
    # 72:Wrath of the Lich King
    # --Dungeon
    # ----271:Ahn'kahet: The Old Kingdom
    # ----272:Azjol-Nerub
    # ----273:Drak'Tharon Keep
    # ----274:Gundrak
    # ----275:Halls of Lightning
    # ----276:Halls of Reflection
    # ----277:Halls of Stone
    # ----278:Pit of Saron
    # ----279:The Culling of Stratholme
    # ----280:The Forge of Souls
    # ----281:The Nexus
    # ----282:The Oculus
    # ----283:The Violet Hold
    # ----284:Trial of the Champion
    # ----285:Utgarde Keep
    # ----286:Utgarde Pinnacle
    # --Raid
    # ----753:Vault of Archavon
    # ----754:Naxxramas
    # ----755:The Obsidian Sanctum
    # ----756:The Eye of Eternity
    # ----759:Ulduar
    # ----757:Trial of the Crusader
    # ----760:Onyxia's Lair
    # ----758:Icecrown Citadel
    # ----761:The Ruby Sanctum
    # 73:Cataclysm
    # --Dungeon
    # ----66:Blackrock Caverns
    # ----63:Deadmines
    # ----184:End Time
    # ----71:Grim Batol
    # ----70:Halls of Origination
    # ----186:Hour of Twilight
    # ----69:Lost City of the Tol'vir
    # ----64:Shadowfang Keep
    # ----67:The Stonecore
    # ----68:The Vortex Pinnacle
    # ----65:Throne of the Tides
    # ----185:Well of Eternity
    # ----77:Zul'Aman
    # ----76:Zul'Gurub
    # --Raid
    # ----75:Baradin Hold
    # ----73:Blackwing Descent
    # ----72:The Bastion of Twilight
    # ----74:Throne of the Four Winds
    # ----78:Firelands
    # ----187:Dragon Soul
    # 74:Mists of Pandaria
    # --Dungeon
    # ----303:Gate of the Setting Sun
    # ----321:Mogu'shan Palace
    # ----311:Scarlet Halls
    # ----316:Scarlet Monastery
    # ----246:Scholomance
    # ----312:Shado-Pan Monastery
    # ----324:Siege of Niuzao Temple
    # ----302:Stormstout Brewery
    # ----313:Temple of the Jade Serpent
    # --Raid
    # ----317:Mogu'shan Vaults
    # ----330:Heart of Fear
    # ----320:Terrace of Endless Spring
    # ----362:Throne of Thunder
    # ----369:Siege of Orgrimmar






