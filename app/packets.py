import struct
from uuid import UUID

# struct.unpack("<I", )

# sends user id as I32
# packet id = 5 (LOGIN REPLY)| length = 4 | user id = 1
# read case login reply handler for length

class ServerPackets:
    USER_ID = 5
    SEND_MESSAGE = 7
    PONG = 8
    HANDLE_IRC_CHANGE_USERNAME = 9  # unused
    HANDLE_IRC_QUIT = 10
    USER_STATS = 11
    USER_LOGOUT = 12
    SPECTATOR_JOINED = 13
    SPECTATOR_LEFT = 14
    SPECTATE_FRAMES = 15
    VERSION_UPDATE = 19
    SPECTATOR_CANT_SPECTATE = 22
    GET_ATTENTION = 23
    NOTIFICATION = 24
    UPDATE_MATCH = 26
    NEW_MATCH = 27
    DISPOSE_MATCH = 28
    LOBBY_JOIN_UNUSED = 34  # unused
    MATCH_JOIN_SUCCESS = 36
    MATCH_JOIN_FAIL = 37
    FELLOW_SPECTATOR_JOINED = 42
    FELLOW_SPECTATOR_LEFT = 43
    ALL_PLAYERS_LOADED = 45  # unused
    MATCH_START = 46
    MATCH_SCORE_UPDATE = 48
    MATCH_TRANSFER_HOST = 50
    MATCH_ALL_PLAYERS_LOADED = 53
    MATCH_PLAYER_FAILED = 57
    MATCH_COMPLETE = 58
    MATCH_SKIP = 61
    UNAUTHORIZED = 62  # unused
    CHANNEL_JOIN_SUCCESS = 64
    CHANNEL_INFO = 65
    CHANNEL_KICK = 66
    CHANNEL_AUTO_JOIN = 67
    BEATMAP_INFO_REPLY = 69
    PRIVILEGES = 71
    FRIENDS_LIST = 72
    PROTOCOL_VERSION = 75
    MAIN_MENU_ICON = 76
    MONITOR = 80  # unused
    MATCH_PLAYER_SKIPPED = 81
    USER_PRESENCE = 83
    RESTART = 86
    MATCH_INVITE = 88
    CHANNEL_INFO_END = 89
    MATCH_CHANGE_PASSWORD = 91
    SILENCE_END = 92
    USER_SILENCED = 94
    USER_PRESENCE_SINGLE = 95
    USER_PRESENCE_BUNDLE = 96
    USER_DM_BLOCKED = 100
    TARGET_IS_SILENCED = 101
    VERSION_UPDATE_FORCED = 102
    SWITCH_SERVER = 103
    ACCOUNT_RESTRICTED = 104
    RTX = 105  # unused
    MATCH_ABORT = 106
    SWITCH_TOURNAMENT_SERVER = 107


def write_string(value: str) -> bytes:
    # TODO x0b for multiplayer
    data = value.encode()
    data_len = len(data)
    output = bytearray([11 if data_len else 0])
    while data_len:
        b = data_len & 0b1111111
        data_len >>= 7
        if data_len != 0:
            b |= 0b10000000

        output.append(b)

    output += data
    return output


def login_reply_packet(user_id: int) -> bytes:
    return struct.pack("<HxIi", ServerPackets.USER_ID, 4, user_id)


def user_presence_packet(
    user_id: int,
    username: str,
    timezone: int,
    country: int,
    permission: int,
    longitude: float,
    latitude: float,
    rank: int,
    gamemode: int,
) -> bytes:
    packet_data = struct.pack(
        "<i",
        user_id,
    )
    packet_data += write_string(username)
    packet_data += struct.pack("<B", timezone + 24)
    packet_data += struct.pack("<B", country)
    packet_data += struct.pack("<B", (permission & 0x1F) | ((gamemode & 0x7) << 5))
    packet_data += struct.pack("<f", longitude)
    packet_data += struct.pack("<f", latitude)
    packet_data += struct.pack("<i", rank)

    return (
        struct.pack("<HxI", ServerPackets.USER_PRESENCE, len(packet_data)) + packet_data
    )


def user_stats_packet(
    user_id: int,
    status: int,
    ranked_score: int,
    accuracy: float,
    play_count: int,
    total_score: int,
    rank: int,
    performance: int,
    status_text: str,
    beatmap_checksum: str,
    current_mods: int,
    play_mode: int,
    beatmap_id: int,
) -> bytes:
    packet_data = struct.pack(
        "<i",
        user_id,
    )
    packet_data += struct.pack("<B", status)
    packet_data += write_string(status_text)
    packet_data += write_string(beatmap_checksum)
    packet_data += struct.pack("<I", current_mods)
    packet_data += struct.pack("<B", play_mode)
    packet_data += struct.pack("<i", beatmap_id)

    packet_data += struct.pack("<Q", ranked_score)
    packet_data += struct.pack("<f", accuracy)
    packet_data += struct.pack("<i", play_count)
    packet_data += struct.pack("<q", total_score)
    packet_data += struct.pack("<i", rank)
    packet_data += struct.pack("<i", performance)


# userId = sr.ReadInt32();
#
# status = sr.ReadByte();
# beatmapChecksum = sr.ReadString();
# currentMods = sr.ReadInt32();
# playMode = sr.ReadByte();
# beatmapId = sr.ReadInt32();
#
# rankedScore = sr.ReadInt64();
# accuracy = sr.ReadSingle();
# playcount = sr.ReadInt32();
# totalScore = sr.ReadInt64();
# rank = sr.ReadInt32();
# performance = sr.ReadInt16();


    return struct.pack("<HxI", ServerPackets.USER_STATS, len(packet_data)) + packet_data
