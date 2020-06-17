# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: steammessages_chat.proto
# plugin: python-betterproto

from dataclasses import dataclass
from typing import List

import betterproto

from .steammessages_clientserver_friends import CMsgClientPersonaStateFriend


class EChatRoomJoinState(betterproto.Enum):
    Default = 0
    NONE = 1
    Joined = 2
    TestInvalid = 99


class EChatRoomGroupRank(betterproto.Enum):
    Default = 0
    Viewer = 10
    Guest = 15
    Member = 20
    Moderator = 30
    Officer = 40
    Owner = 50
    TestInvalid = 99


class EChatRoomNotificationLevel(betterproto.Enum):
    Invalid = 0
    NONE = 1
    MentionMe = 2
    MentionAll = 3
    AllMessages = 4


class EChatRoomServerMessage(betterproto.Enum):
    Invalid = 0
    RenameChatRoom = 1
    Joined = 2
    Parted = 3
    Kicked = 4
    Invited = 5
    InviteDismissed = 8
    ChatRoomTaglineChanged = 9
    ChatRoomAvatarChanged = 10
    AppCustom = 11


class EChatRoomMemberStateChange(betterproto.Enum):
    Invalid = 0
    Joined = 1
    Parted = 2
    Kicked = 3
    Invited = 4
    RankChanged = 7
    InviteDismissed = 8
    Muted = 9
    Banned = 10
    RolesChanged = 12


@dataclass
class CChat_RequestFriendPersonaStates_Request(betterproto.Message):
    pass


@dataclass
class CChat_RequestFriendPersonaStates_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_CreateChatRoomGroup_Request(betterproto.Message):
    steamid_partner: float = betterproto.fixed64_field(1)
    steamid_invited: float = betterproto.fixed64_field(2)
    name: str = betterproto.string_field(3)
    steamid_invitees: List[float] = betterproto.fixed64_field(4)
    watching_broadcast_accountid: int = betterproto.uint32_field(6)
    watching_broadcast_channel_id: int = betterproto.uint64_field(7)


@dataclass
class CChatRole(betterproto.Message):
    role_id: int = betterproto.uint64_field(1)
    name: str = betterproto.string_field(2)
    ordinal: int = betterproto.uint32_field(3)


@dataclass
class CChatRoleActions(betterproto.Message):
    role_id: int = betterproto.uint64_field(1)
    can_create_rename_delete_channel: bool = betterproto.bool_field(2)
    can_kick: bool = betterproto.bool_field(3)
    can_ban: bool = betterproto.bool_field(4)
    can_invite: bool = betterproto.bool_field(5)
    can_change_tagline_avatar_name: bool = betterproto.bool_field(6)
    can_chat: bool = betterproto.bool_field(7)
    can_view_history: bool = betterproto.bool_field(8)
    can_change_group_roles: bool = betterproto.bool_field(9)
    can_change_user_roles: bool = betterproto.bool_field(10)
    can_mention_all: bool = betterproto.bool_field(11)
    can_set_watching_broadcast: bool = betterproto.bool_field(12)


@dataclass
class CChatPartyBeacon(betterproto.Message):
    app_id: int = betterproto.uint32_field(1)
    steamid_owner: float = betterproto.fixed64_field(2)
    beacon_id: float = betterproto.fixed64_field(3)
    game_metadata: str = betterproto.string_field(4)


@dataclass
class CChatRoomGroupHeaderState(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_name: str = betterproto.string_field(2)
    clanid: int = betterproto.uint32_field(13)
    accountid_owner: int = betterproto.uint32_field(14)
    appid: int = betterproto.uint32_field(21)
    tagline: str = betterproto.string_field(15)
    avatar_sha: bytes = betterproto.bytes_field(16)
    default_role_id: int = betterproto.uint64_field(17)
    roles: List["CChatRole"] = betterproto.message_field(18)
    role_actions: List["CChatRoleActions"] = betterproto.message_field(19)
    watching_broadcast_accountid: int = betterproto.uint32_field(20)
    party_beacons: List["CChatPartyBeacon"] = betterproto.message_field(22)
    watching_broadcast_channel_id: int = betterproto.uint64_field(23)
    active_minigame_id: int = betterproto.uint64_field(24)
    avatar_ugc_url: str = betterproto.string_field(25)


@dataclass
class CChatRoomMember(betterproto.Message):
    accountid: int = betterproto.uint32_field(1)
    state: "EChatRoomJoinState" = betterproto.enum_field(3)
    rank: "EChatRoomGroupRank" = betterproto.enum_field(4)
    time_kick_expire: int = betterproto.uint32_field(6)
    role_ids: List[int] = betterproto.uint64_field(7)


@dataclass
class CChatRoomState(betterproto.Message):
    chat_id: int = betterproto.uint64_field(1)
    chat_name: str = betterproto.string_field(2)
    voice_allowed: bool = betterproto.bool_field(3)
    members_in_voice: List[int] = betterproto.uint32_field(4)
    time_last_message: int = betterproto.uint32_field(5)
    sort_order: int = betterproto.uint32_field(6)
    last_message: str = betterproto.string_field(7)
    accountid_last_message: int = betterproto.uint32_field(8)


@dataclass
class CChatRoomGroupState(betterproto.Message):
    header_state: "CChatRoomGroupHeaderState" = betterproto.message_field(1)
    members: List["CChatRoomMember"] = betterproto.message_field(2)
    default_chat_id: int = betterproto.uint64_field(4)
    chat_rooms: List["CChatRoomState"] = betterproto.message_field(5)
    kicked: List["CChatRoomMember"] = betterproto.message_field(7)


@dataclass
class CUserChatRoomState(betterproto.Message):
    chat_id: int = betterproto.uint64_field(1)
    time_joined: int = betterproto.uint32_field(2)
    time_last_ack: int = betterproto.uint32_field(3)
    desktop_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(4)
    mobile_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(5)
    time_last_mention: int = betterproto.uint32_field(6)
    unread_indicator_muted: bool = betterproto.bool_field(7)
    time_first_unread: int = betterproto.uint32_field(8)


@dataclass
class CUserChatRoomGroupState(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    time_joined: int = betterproto.uint32_field(2)
    user_chat_room_state: List["CUserChatRoomState"] = betterproto.message_field(3)
    desktop_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(4)
    mobile_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(5)
    time_last_group_ack: int = betterproto.uint32_field(6)
    unread_indicator_muted: bool = betterproto.bool_field(7)


@dataclass
class CChatRoom_CreateChatRoomGroup_Response(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    state: "CChatRoomGroupState" = betterproto.message_field(2)
    user_chat_state: "CUserChatRoomGroupState" = betterproto.message_field(3)


@dataclass
class CChatRoom_SaveChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    name: str = betterproto.string_field(2)


@dataclass
class CChatRoom_SaveChatRoomGroup_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_RenameChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    name: str = betterproto.string_field(2)


@dataclass
class CChatRoom_RenameChatRoomGroup_Response(betterproto.Message):
    name: str = betterproto.string_field(1)


@dataclass
class CChatRoom_SetChatRoomGroupTagline_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    tagline: str = betterproto.string_field(2)


@dataclass
class CChatRoom_SetChatRoomGroupTagline_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_SetChatRoomGroupAvatar_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    avatar_sha: bytes = betterproto.bytes_field(2)


@dataclass
class CChatRoom_SetChatRoomGroupAvatar_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_SetChatRoomGroupWatchingBroadcast_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    watching_broadcast_accountid: int = betterproto.uint32_field(2)
    watching_broadcast_channel_id: int = betterproto.uint64_field(3)


@dataclass
class CChatRoom_SetChatRoomGroupWatchingBroadcast_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_JoinMiniGameForChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)


@dataclass
class CChatRoom_JoinMiniGameForChatRoomGroup_Response(betterproto.Message):
    minigame_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_EndMiniGameForChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    minigame_id: int = betterproto.uint64_field(3)


@dataclass
class CChatRoom_EndMiniGameForChatRoomGroup_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_MuteUser_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    steamid: float = betterproto.fixed64_field(2)
    expiration: int = betterproto.int32_field(3)


@dataclass
class CChatRoom_MuteUser_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_KickUser_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    steamid: float = betterproto.fixed64_field(2)
    expiration: int = betterproto.int32_field(3)


@dataclass
class CChatRoom_KickUser_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_SetUserBanState_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    steamid: float = betterproto.fixed64_field(2)
    ban_state: bool = betterproto.bool_field(3)


@dataclass
class CChatRoom_SetUserBanState_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_RevokeInvite_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    steamid: float = betterproto.fixed64_field(2)


@dataclass
class CChatRoom_RevokeInvite_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_CreateRole_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    name: str = betterproto.string_field(2)


@dataclass
class CChatRoom_CreateRole_Response(betterproto.Message):
    actions: "CChatRoleActions" = betterproto.message_field(2)


@dataclass
class CChatRoom_GetRoles_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_GetRoles_Response(betterproto.Message):
    roles: List["CChatRole"] = betterproto.message_field(1)


@dataclass
class CChatRoom_RenameRole_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(2)
    name: str = betterproto.string_field(3)


@dataclass
class CChatRoom_RenameRole_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_ReorderRole_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(2)
    ordinal: int = betterproto.uint32_field(3)


@dataclass
class CChatRoom_ReorderRole_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_DeleteRole_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(2)


@dataclass
class CChatRoom_DeleteRole_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_GetRoleActions_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(2)


@dataclass
class CChatRoom_GetRoleActions_Response(betterproto.Message):
    actions: List["CChatRoleActions"] = betterproto.message_field(1)


@dataclass
class CChatRoom_ReplaceRoleActions_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(2)
    actions: "CChatRoleActions" = betterproto.message_field(4)


@dataclass
class CChatRoom_ReplaceRoleActions_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_AddRoleToUser_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(3)
    steamid: float = betterproto.fixed64_field(4)


@dataclass
class CChatRoom_AddRoleToUser_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_GetRolesForUser_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    steamid: float = betterproto.fixed64_field(3)


@dataclass
class CChatRoom_GetRolesForUser_Response(betterproto.Message):
    role_ids: List[int] = betterproto.uint64_field(1)


@dataclass
class CChatRoom_DeleteRoleFromUser_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    role_id: int = betterproto.uint64_field(3)
    steamid: float = betterproto.fixed64_field(4)


@dataclass
class CChatRoom_DeleteRoleFromUser_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_JoinChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    invite_code: str = betterproto.string_field(2)
    chat_id: int = betterproto.uint64_field(3)


@dataclass
class CChatRoom_JoinChatRoomGroup_Response(betterproto.Message):
    state: "CChatRoomGroupState" = betterproto.message_field(1)
    user_chat_state: "CUserChatRoomGroupState" = betterproto.message_field(3)
    join_chat_id: int = betterproto.uint64_field(4)
    time_expire: int = betterproto.uint32_field(5)


@dataclass
class CChatRoom_InviteFriendToChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    steamid: float = betterproto.fixed64_field(2)
    chat_id: int = betterproto.uint64_field(3)
    skip_friendsui_check: bool = betterproto.bool_field(4)


@dataclass
class CChatRoom_InviteFriendToChatRoomGroup_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_LeaveChatRoomGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_LeaveChatRoomGroup_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_CreateChatRoom_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    name: str = betterproto.string_field(2)
    allow_voice: bool = betterproto.bool_field(3)


@dataclass
class CChatRoom_CreateChatRoom_Response(betterproto.Message):
    chat_room: "CChatRoomState" = betterproto.message_field(1)


@dataclass
class CChatRoom_DeleteChatRoom_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)


@dataclass
class CChatRoom_DeleteChatRoom_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_RenameChatRoom_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    name: str = betterproto.string_field(3)


@dataclass
class CChatRoom_RenameChatRoom_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_ReorderChatRoom_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    move_after_chat_id: int = betterproto.uint64_field(3)


@dataclass
class CChatRoom_ReorderChatRoom_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_SendChatMessage_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    message: str = betterproto.string_field(3)
    echo_to_sender: bool = betterproto.bool_field(4)


@dataclass
class CChatRoom_SendChatMessage_Response(betterproto.Message):
    modified_message: str = betterproto.string_field(1)
    server_timestamp: int = betterproto.uint32_field(2)
    ordinal: int = betterproto.uint32_field(3)
    message_without_bb_code: str = betterproto.string_field(4)


@dataclass
class CChatRoom_JoinVoiceChat_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)


@dataclass
class CChatRoom_JoinVoiceChat_Response(betterproto.Message):
    voice_chatid: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_LeaveVoiceChat_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)


@dataclass
class CChatRoom_LeaveVoiceChat_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_GetMessageHistory_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    last_time: int = betterproto.uint32_field(3)
    last_ordinal: int = betterproto.uint32_field(4)
    start_time: int = betterproto.uint32_field(5)
    start_ordinal: int = betterproto.uint32_field(6)
    max_count: int = betterproto.uint32_field(7)


@dataclass
class ServerMessage(betterproto.Message):
    message: "EChatRoomServerMessage" = betterproto.enum_field(1)
    string_param: str = betterproto.string_field(2)
    accountid_param: int = betterproto.uint32_field(3)


@dataclass
class CChatRoom_GetMessageHistory_Response(betterproto.Message):
    messages: List[
        "CChatRoom_GetMessageHistory_ResponseChatMessage"
    ] = betterproto.message_field(1)
    more_available: bool = betterproto.bool_field(4)


@dataclass
class CChatRoom_GetMessageHistory_ResponseChatMessage(betterproto.Message):
    sender: int = betterproto.uint32_field(1)
    server_timestamp: int = betterproto.uint32_field(2)
    message: str = betterproto.string_field(3)
    ordinal: int = betterproto.uint32_field(4)
    server_message: "ServerMessage" = betterproto.message_field(5)
    deleted: bool = betterproto.bool_field(6)


@dataclass
class CChatRoom_GetMyChatRoomGroups_Request(betterproto.Message):
    pass


@dataclass
class CChatRoom_GetChatRoomGroupSummary_Response(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_group_name: str = betterproto.string_field(2)
    active_member_count: int = betterproto.uint32_field(3)
    active_voice_member_count: int = betterproto.uint32_field(4)
    default_chat_id: int = betterproto.uint64_field(5)
    chat_rooms: List["CChatRoomState"] = betterproto.message_field(6)
    clanid: int = betterproto.uint32_field(7)
    chat_group_tagline: str = betterproto.string_field(8)
    accountid_owner: int = betterproto.uint32_field(9)
    top_members: List[int] = betterproto.uint32_field(10)
    chat_group_avatar_sha: bytes = betterproto.bytes_field(11)
    rank: "EChatRoomGroupRank" = betterproto.enum_field(12)
    default_role_id: int = betterproto.uint64_field(13)
    role_ids: List[int] = betterproto.uint64_field(14)
    role_actions: List["CChatRoleActions"] = betterproto.message_field(15)
    watching_broadcast_accountid: int = betterproto.uint32_field(16)
    appid: int = betterproto.uint32_field(17)
    party_beacons: List["CChatPartyBeacon"] = betterproto.message_field(18)
    watching_broadcast_channel_id: int = betterproto.uint64_field(19)
    active_minigame_id: int = betterproto.uint64_field(20)
    avatar_ugc_url: str = betterproto.string_field(21)


@dataclass
class CChatRoomSummaryPair(betterproto.Message):
    user_chat_group_state: "CUserChatRoomGroupState" = betterproto.message_field(1)
    group_summary: "CChatRoom_GetChatRoomGroupSummary_Response" = betterproto.message_field(2)


@dataclass
class CChatRoom_GetMyChatRoomGroups_Response(betterproto.Message):
    chat_room_groups: List["CChatRoomSummaryPair"] = betterproto.message_field(1)


@dataclass
class CChatRoom_GetChatRoomGroupState_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_GetChatRoomGroupState_Response(betterproto.Message):
    state: "CChatRoomGroupState" = betterproto.message_field(1)


@dataclass
class CChatRoom_GetChatRoomGroupSummary_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_SetAppChatRoomGroupForceActive_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    requesting_app_id: int = betterproto.uint32_field(2)


@dataclass
class CChatRoom_SetAppChatRoomGroupForceActive_Response(betterproto.Message):
    result: int = betterproto.uint32_field(1)
    accounts_in_channel: List[int] = betterproto.uint32_field(2)


@dataclass
class CChatRoom_SetAppChatRoomGroupStopForceActive_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    requesting_app_id: int = betterproto.uint32_field(2)


@dataclass
class CChatRoom_AckChatMessage_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    timestamp: int = betterproto.uint32_field(3)


@dataclass
class CChatRoom_CreateInviteLink_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    seconds_valid: int = betterproto.uint32_field(2)
    chat_id: int = betterproto.uint64_field(3)


@dataclass
class CChatRoom_CreateInviteLink_Response(betterproto.Message):
    invite_code: str = betterproto.string_field(1)
    seconds_valid: int = betterproto.uint32_field(2)


@dataclass
class CChatRoom_GetInviteLinkInfo_Request(betterproto.Message):
    invite_code: str = betterproto.string_field(1)


@dataclass
class CChatRoom_GetInviteLinkInfo_Response(betterproto.Message):
    steamid_sender: float = betterproto.fixed64_field(3)
    time_expires: int = betterproto.uint32_field(4)
    chat_id: int = betterproto.uint64_field(6)
    group_summary: "CChatRoom_GetChatRoomGroupSummary_Response" = betterproto.message_field(
        8
    )
    user_chat_group_state: "CUserChatRoomGroupState" = betterproto.message_field(9)
    time_kick_expire: int = betterproto.uint32_field(10)
    banned: bool = betterproto.bool_field(11)


@dataclass
class CChatRoom_GetInviteInfo_Request(betterproto.Message):
    steamid_invitee: float = betterproto.fixed64_field(1)
    chat_group_id: int = betterproto.uint64_field(2)
    chat_id: int = betterproto.uint64_field(3)
    invite_code: str = betterproto.string_field(4)


@dataclass
class CChatRoom_GetInviteInfo_Response(betterproto.Message):
    group_summary: "CChatRoom_GetChatRoomGroupSummary_Response" = betterproto.message_field(
        1
    )
    time_kick_expire: int = betterproto.uint32_field(2)
    banned: bool = betterproto.bool_field(3)


@dataclass
class CChatRoom_GetInviteLinksForGroup_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_GetInviteLinksForGroup_Response(betterproto.Message):
    invite_links: List[
        "CChatRoom_GetInviteLinksForGroup_ResponseLinkInfo"
    ] = betterproto.message_field(1)


@dataclass
class CChatRoom_GetInviteLinksForGroup_ResponseLinkInfo(betterproto.Message):
    invite_code: str = betterproto.string_field(1)
    steamid_creator: float = betterproto.fixed64_field(2)
    time_expires: int = betterproto.uint32_field(3)
    chat_id: int = betterproto.uint64_field(4)


@dataclass
class CChatRoom_GetBanList_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoom_GetBanList_Response(betterproto.Message):
    bans: List["CChatRoom_GetBanList_ResponseBanInfo"] = betterproto.message_field(1)


@dataclass
class CChatRoom_GetBanList_ResponseBanInfo(betterproto.Message):
    accountid: int = betterproto.uint32_field(1)
    accountid_actor: int = betterproto.uint32_field(2)
    time_banned: int = betterproto.uint32_field(3)
    ban_reason: str = betterproto.string_field(4)


@dataclass
class CChatRoom_GetInviteList_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)


@dataclass
class CChatRoomGroupInvite(betterproto.Message):
    accountid: int = betterproto.uint32_field(1)
    accountid_actor: int = betterproto.uint32_field(2)
    time_invited: int = betterproto.uint32_field(3)


@dataclass
class CChatRoom_GetInviteList_Response(betterproto.Message):
    invites: List["CChatRoomGroupInvite"] = betterproto.message_field(1)


@dataclass
class CChatRoom_DeleteInviteLink_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    invite_code: str = betterproto.string_field(2)


@dataclass
class CChatRoom_DeleteInviteLink_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_SetSessionActiveChatRoomGroups_Request(betterproto.Message):
    chat_group_ids: List[int] = betterproto.uint64_field(1)
    chat_groups_data_requested: List[int] = betterproto.uint64_field(2)
    virtualize_members_threshold: int = betterproto.int32_field(3)


@dataclass
class CChatRoom_SetSessionActiveChatRoomGroups_Response(betterproto.Message):
    chat_states: List["CChatRoomGroupState"] = betterproto.message_field(1)
    virtualize_members_chat_group_ids: List[int] = betterproto.uint64_field(2)


@dataclass
class CChatRoom_SetUserChatGroupPreferences_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_group_preferences: \
        "CChatRoom_SetUserChatGroupPreferences_RequestChatGroupPreferences" = betterproto.message_field(2)
    chat_room_preferences: List[
        "CChatRoom_SetUserChatGroupPreferences_RequestChatRoomPreferences"
    ] = betterproto.message_field(3)


@dataclass
class CChatRoom_SetUserChatGroupPreferences_RequestChatGroupPreferences(
    betterproto.Message
):
    desktop_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(1)
    mobile_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(2)
    unread_indicator_muted: bool = betterproto.bool_field(3)


@dataclass
class CChatRoom_SetUserChatGroupPreferences_RequestChatRoomPreferences(betterproto.Message):
    chat_id: int = betterproto.uint64_field(1)
    desktop_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(2)
    mobile_notification_level: "EChatRoomNotificationLevel" = betterproto.enum_field(3)
    unread_indicator_muted: bool = betterproto.bool_field(4)


@dataclass
class CChatRoom_SetUserChatGroupPreferences_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_DeleteChatMessages_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    messages: List[
        "CChatRoom_DeleteChatMessages_RequestMessage"
    ] = betterproto.message_field(3)


@dataclass
class CChatRoom_DeleteChatMessages_RequestMessage(betterproto.Message):
    server_timestamp: int = betterproto.uint32_field(1)
    ordinal: int = betterproto.uint32_field(2)


@dataclass
class CChatRoom_DeleteChatMessages_Response(betterproto.Message):
    pass


@dataclass
class CChatRoom_UpdateMemberListView_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    view_id: int = betterproto.uint64_field(2)
    start: int = betterproto.int32_field(3)
    end: int = betterproto.int32_field(4)
    client_changenumber: int = betterproto.int32_field(5)
    delete_view: bool = betterproto.bool_field(6)
    persona_subscribe_accountids: List[int] = betterproto.int32_field(7)
    persona_unsubscribe_accountids: List[int] = betterproto.int32_field(8)


@dataclass
class CChatRoom_SearchMembers_Request(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    search_id: int = betterproto.uint64_field(2)
    search_text: str = betterproto.string_field(3)
    max_results: int = betterproto.int32_field(4)


@dataclass
class CChatRoom_SearchMembers_Response(betterproto.Message):
    matching_members: List[
        "CChatRoom_SearchMembers_ResponseMemberMatch"
    ] = betterproto.message_field(1)
    status_flags: int = betterproto.uint32_field(2)


@dataclass
class CChatRoom_SearchMembers_ResponseMemberMatch(betterproto.Message):
    accountid: int = betterproto.int32_field(1)
    persona: "CMsgClientPersonaStateFriend" = betterproto.message_field(2)


@dataclass
class CClanChatRooms_GetClanChatRoomInfo_Request(betterproto.Message):
    steamid: float = betterproto.fixed64_field(1)
    autocreate: bool = betterproto.bool_field(2)


@dataclass
class CClanChatRooms_GetClanChatRoomInfo_Response(betterproto.Message):
    chat_group_summary: "CChatRoom_GetChatRoomGroupSummary_Response" = betterproto.message_field(
        1
    )


@dataclass
class CClanChatRooms_SetClanChatRoomPrivate_Request(betterproto.Message):
    steamid: float = betterproto.fixed64_field(1)
    chat_room_private: bool = betterproto.bool_field(2)


@dataclass
class CClanChatRooms_SetClanChatRoomPrivate_Response(betterproto.Message):
    chat_room_private: bool = betterproto.bool_field(1)


@dataclass
class CChatMentions(betterproto.Message):
    mention_all: bool = betterproto.bool_field(1)
    mention_here: bool = betterproto.bool_field(2)
    mention_accountids: List[int] = betterproto.uint32_field(3)


@dataclass
class CChatRoom_IncomingChatMessage_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    steamid_sender: float = betterproto.fixed64_field(3)
    message: str = betterproto.string_field(4)
    timestamp: int = betterproto.uint32_field(5)
    mentions: "CChatMentions" = betterproto.message_field(6)
    ordinal: int = betterproto.uint32_field(7)
    server_message: "ServerMessage" = betterproto.message_field(8)
    message_no_bbcode: str = betterproto.string_field(9)
    chat_name: str = betterproto.string_field(10)


@dataclass
class CChatRoom_ChatMessageModified_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    chat_id: int = betterproto.uint64_field(2)
    messages: List[
        "CChatRoom_ChatMessageModified_NotificationChatMessage"
    ] = betterproto.message_field(3)


@dataclass
class CChatRoom_ChatMessageModified_NotificationChatMessage(betterproto.Message):
    server_timestamp: int = betterproto.uint32_field(1)
    ordinal: int = betterproto.uint32_field(2)
    deleted: bool = betterproto.bool_field(3)


@dataclass
class CChatRoom_MemberStateChange_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    member: "CChatRoomMember" = betterproto.message_field(2)
    change: "EChatRoomMemberStateChange" = betterproto.enum_field(3)


@dataclass
class CChatRoom_ChatRoomHeaderState_Notification(betterproto.Message):
    header_state: "CChatRoomGroupHeaderState" = betterproto.message_field(1)


@dataclass
class CChatRoom_ChatRoomGroupRoomsChange_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    default_chat_id: int = betterproto.uint64_field(2)
    chat_rooms: List["CChatRoomState"] = betterproto.message_field(3)


@dataclass
class CChatRoom_NotifyShouldRejoinChatRoomVoiceChat_Notification(betterproto.Message):
    chat_id: int = betterproto.uint64_field(1)
    chat_group_id: int = betterproto.uint64_field(2)


@dataclass
class ChatRoomClient_NotifyChatGroupUserStateChanged_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    user_chat_group_state: "CUserChatRoomGroupState" = betterproto.message_field(2)
    group_summary: "CChatRoom_GetChatRoomGroupSummary_Response" = betterproto.message_field(3)
    user_action: "EChatRoomMemberStateChange" = betterproto.enum_field(4)


@dataclass
class ChatRoomClient_NotifyChatRoomDisconnect_Notification(betterproto.Message):
    chat_group_ids: List[int] = betterproto.uint64_field(1)


@dataclass
class CChatRoomMemberListView(betterproto.Message):
    start: int = betterproto.int32_field(3)
    end: int = betterproto.int32_field(4)
    total_count: int = betterproto.int32_field(5)
    client_changenumber: int = betterproto.int32_field(6)
    server_changenumber: int = betterproto.int32_field(7)


@dataclass
class CChatRoomMemberSummaryCounts(betterproto.Message):
    ingame: int = betterproto.int32_field(1)
    online: int = betterproto.int32_field(2)
    offline: int = betterproto.int32_field(3)


@dataclass
class CChatRoomClient_MemberListViewUpdated_Notification(betterproto.Message):
    chat_group_id: int = betterproto.uint64_field(1)
    view_id: int = betterproto.uint64_field(2)
    view: "CChatRoomMemberListView" = betterproto.message_field(3)
    members: List["CChatRoomClient_MemberListViewUpdated_NotificationMemberListViewEntry"] = betterproto.message_field(4)
    status_flags: int = betterproto.uint32_field(5)
    member_summary: "CChatRoomMemberSummaryCounts" = betterproto.message_field(6)
    subscribed_personas: List["CMsgClientPersonaStateFriend"] = betterproto.message_field(7)


@dataclass
class CChatRoomClient_MemberListViewUpdated_NotificationMemberListViewEntry(betterproto.Message):
    rank: int = betterproto.int32_field(1)
    accountid: int = betterproto.uint32_field(2)
    persona: "CMsgClientPersonaStateFriend" = betterproto.message_field(3)


@dataclass
class CChatUsability_ClientUsabilityMetrics_Notification(betterproto.Message):
    metrics_run_id: int = betterproto.uint32_field(1)
    client_build: int = betterproto.uint32_field(2)
    metrics_version: int = betterproto.uint32_field(3)
    in_web: bool = betterproto.bool_field(4)
    settings: "CChatUsability_ClientUsabilityMetrics_NotificationSettings" = betterproto.message_field(10)
    voice_settings: "CChatUsability_ClientUsabilityMetrics_NotificationVoiceSettings" = betterproto.message_field(11)
    ui_state: "CChatUsability_ClientUsabilityMetrics_NotificationUIState" = betterproto.message_field(12)
    metrics: "CChatUsability_ClientUsabilityMetrics_NotificationMetrics" = betterproto.message_field(13)


@dataclass
class CChatUsability_ClientUsabilityMetrics_NotificationSettings(betterproto.Message):
    notifications_show_ingame: bool = betterproto.bool_field(1)
    notifications_show_online: bool = betterproto.bool_field(2)
    notifications_show_message: bool = betterproto.bool_field(3)
    notifications_events_and_announcements: bool = betterproto.bool_field(4)
    sounds_play_ingame: bool = betterproto.bool_field(5)
    sounds_play_online: bool = betterproto.bool_field(6)
    sounds_play_message: bool = betterproto.bool_field(7)
    sounds_events_and_announcements: bool = betterproto.bool_field(8)
    always_new_chat_window: bool = betterproto.bool_field(9)
    force_alphabetic_friend_sorting: bool = betterproto.bool_field(10)
    chat_flash_mode: int = betterproto.int32_field(11)
    remember_open_chats: bool = betterproto.bool_field(12)
    compact_quick_access: bool = betterproto.bool_field(13)
    compact_friends_list: bool = betterproto.bool_field(14)
    notifications_show_chat_room_notification: bool = betterproto.bool_field(15)
    sounds_play_chat_room_notification: bool = betterproto.bool_field(16)
    hide_offline_friends_in_tag_groups: bool = betterproto.bool_field(17)
    hide_categorized_friends: bool = betterproto.bool_field(18)
    categorize_in_game_friends_by_game: bool = betterproto.bool_field(19)
    chat_font_size: int = betterproto.int32_field(20)
    use24hour_clock: bool = betterproto.bool_field(21)
    do_not_disturb_mode: bool = betterproto.bool_field(22)
    disable_embed_inlining: bool = betterproto.bool_field(23)
    sign_into_friends: bool = betterproto.bool_field(24)
    animated_avatars: bool = betterproto.bool_field(25)


@dataclass
class CChatUsability_ClientUsabilityMetrics_NotificationVoiceSettings(
    betterproto.Message
):
    voice_input_gain: float = betterproto.float_field(1)
    voice_output_gain: float = betterproto.float_field(2)
    noise_gate_level: int = betterproto.int32_field(3)
    voice_use_echo_cancellation: bool = betterproto.bool_field(4)
    voice_use_noise_cancellation: bool = betterproto.bool_field(5)
    voice_use_auto_gain_control: bool = betterproto.bool_field(6)
    selected_non_default_mic: bool = betterproto.bool_field(7)
    selected_non_default_output: bool = betterproto.bool_field(8)
    push_to_talk_enabled: bool = betterproto.bool_field(9)
    push_to_mute_enabled: bool = betterproto.bool_field(10)
    play_ptt_sounds: bool = betterproto.bool_field(11)


@dataclass
class CChatUsability_ClientUsabilityMetrics_NotificationUIState(betterproto.Message):
    friends_list_height: int = betterproto.int32_field(1)
    friends_list_width: int = betterproto.int32_field(2)
    friends_list_docked: bool = betterproto.bool_field(3)
    friends_list_collapsed: bool = betterproto.bool_field(4)
    friends_list_group_chats_height: int = betterproto.int32_field(5)
    friends_list_visible: bool = betterproto.bool_field(6)
    chat_popups_opened: int = betterproto.int32_field(7)
    group_chat_tabs_opened: int = betterproto.int32_field(8)
    friend_chat_tabs_opened: int = betterproto.int32_field(9)
    chat_window_width: int = betterproto.int32_field(10)
    chat_window_height: int = betterproto.int32_field(11)
    category_collapse: "CChatUsability_ClientUsabilityMetrics_NotificationUIStateCategoryCollapseState" = betterproto.message_field(12)
    group_chat_left_col_collapsed: int = betterproto.int32_field(13)
    group_chat_right_col_collapsed: int = betterproto.int32_field(14)
    in_one_on_one_voice_chat: bool = betterproto.bool_field(15)
    in_group_voice_chat: bool = betterproto.bool_field(16)


@dataclass
class CChatUsability_ClientUsabilityMetrics_NotificationUIStateCategoryCollapseState(betterproto.Message):
    in_game_collapsed: bool = betterproto.bool_field(1)
    online_collapsed: bool = betterproto.bool_field(2)
    offline_collapsed: bool = betterproto.bool_field(3)
    game_groups_collapsed: int = betterproto.int32_field(4)
    categories_collapsed: int = betterproto.int32_field(5)


@dataclass
class CChatUsability_ClientUsabilityMetrics_NotificationMetrics(betterproto.Message):
    friends_count: int = betterproto.int32_field(1)
    friends_category_count: int = betterproto.int32_field(2)
    friends_categorized_count: int = betterproto.int32_field(3)
    friends_online_count: int = betterproto.int32_field(4)
    friends_in_game_count: int = betterproto.int32_field(5)
    friends_in_game_singleton_count: int = betterproto.int32_field(6)
    game_group_count: int = betterproto.int32_field(7)
    friends_favorite_count: int = betterproto.int32_field(8)
    group_chat_count: int = betterproto.int32_field(9)
    group_chat_favorite_count: int = betterproto.int32_field(10)


@dataclass
class CChatUsability_RequestClientUsabilityMetrics_Notification(betterproto.Message):
    metrics_run_id: int = betterproto.uint32_field(1)
