# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: s2clientprotocol/debug.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from s2clientprotocol import common_pb2 as s2clientprotocol_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cs2clientprotocol/debug.proto\x12\x0eSC2APIProtocol\x1a\x1ds2clientprotocol/common.proto\"\xbb\x03\n\x0c\x44\x65\x62ugCommand\x12)\n\x04\x64raw\x18\x01 \x01(\x0b\x32\x19.SC2APIProtocol.DebugDrawH\x00\x12\x34\n\ngame_state\x18\x02 \x01(\x0e\x32\x1e.SC2APIProtocol.DebugGameStateH\x00\x12\x36\n\x0b\x63reate_unit\x18\x03 \x01(\x0b\x32\x1f.SC2APIProtocol.DebugCreateUnitH\x00\x12\x32\n\tkill_unit\x18\x04 \x01(\x0b\x32\x1d.SC2APIProtocol.DebugKillUnitH\x00\x12\x38\n\x0ctest_process\x18\x05 \x01(\x0b\x32 .SC2APIProtocol.DebugTestProcessH\x00\x12.\n\x05score\x18\x06 \x01(\x0b\x32\x1d.SC2APIProtocol.DebugSetScoreH\x00\x12\x30\n\x08\x65nd_game\x18\x07 \x01(\x0b\x32\x1c.SC2APIProtocol.DebugEndGameH\x00\x12\x37\n\nunit_value\x18\x08 \x01(\x0b\x32!.SC2APIProtocol.DebugSetUnitValueH\x00\x42\t\n\x07\x63ommand\"\xb5\x01\n\tDebugDraw\x12\'\n\x04text\x18\x01 \x03(\x0b\x32\x19.SC2APIProtocol.DebugText\x12(\n\x05lines\x18\x02 \x03(\x0b\x32\x19.SC2APIProtocol.DebugLine\x12\'\n\x05\x62oxes\x18\x03 \x03(\x0b\x32\x18.SC2APIProtocol.DebugBox\x12,\n\x07spheres\x18\x04 \x03(\x0b\x32\x1b.SC2APIProtocol.DebugSphere\"L\n\x04Line\x12!\n\x02p0\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12!\n\x02p1\x18\x02 \x01(\x0b\x32\x15.SC2APIProtocol.Point\"(\n\x05\x43olor\x12\t\n\x01r\x18\x01 \x01(\r\x12\t\n\x01g\x18\x02 \x01(\r\x12\t\n\x01\x62\x18\x03 \x01(\r\"\xa3\x01\n\tDebugText\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12\x0c\n\x04text\x18\x02 \x01(\t\x12*\n\x0bvirtual_pos\x18\x03 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12(\n\tworld_pos\x18\x04 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12\x0c\n\x04size\x18\x05 \x01(\r\"U\n\tDebugLine\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12\"\n\x04line\x18\x02 \x01(\x0b\x32\x14.SC2APIProtocol.Line\"x\n\x08\x44\x65\x62ugBox\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12\"\n\x03min\x18\x02 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12\"\n\x03max\x18\x03 \x01(\x0b\x32\x15.SC2APIProtocol.Point\"`\n\x0b\x44\x65\x62ugSphere\x12$\n\x05\x63olor\x18\x01 \x01(\x0b\x32\x15.SC2APIProtocol.Color\x12 \n\x01p\x18\x02 \x01(\x0b\x32\x15.SC2APIProtocol.Point\x12\t\n\x01r\x18\x03 \x01(\x02\"k\n\x0f\x44\x65\x62ugCreateUnit\x12\x11\n\tunit_type\x18\x01 \x01(\r\x12\r\n\x05owner\x18\x02 \x01(\x05\x12$\n\x03pos\x18\x03 \x01(\x0b\x32\x17.SC2APIProtocol.Point2D\x12\x10\n\x08quantity\x18\x04 \x01(\r\"\x1c\n\rDebugKillUnit\x12\x0b\n\x03tag\x18\x01 \x03(\x04\"\x80\x01\n\x10\x44\x65\x62ugTestProcess\x12\x33\n\x04test\x18\x01 \x01(\x0e\x32%.SC2APIProtocol.DebugTestProcess.Test\x12\x10\n\x08\x64\x65lay_ms\x18\x02 \x01(\x05\"%\n\x04Test\x12\x08\n\x04hang\x10\x01\x12\t\n\x05\x63rash\x10\x02\x12\x08\n\x04\x65xit\x10\x03\"\x1e\n\rDebugSetScore\x12\r\n\x05score\x18\x01 \x01(\x02\"z\n\x0c\x44\x65\x62ugEndGame\x12:\n\nend_result\x18\x01 \x01(\x0e\x32&.SC2APIProtocol.DebugEndGame.EndResult\".\n\tEndResult\x12\r\n\tSurrender\x10\x01\x12\x12\n\x0e\x44\x65\x63lareVictory\x10\x02\"\xa5\x01\n\x11\x44\x65\x62ugSetUnitValue\x12?\n\nunit_value\x18\x01 \x01(\x0e\x32+.SC2APIProtocol.DebugSetUnitValue.UnitValue\x12\r\n\x05value\x18\x02 \x01(\x02\x12\x10\n\x08unit_tag\x18\x03 \x01(\x04\".\n\tUnitValue\x12\n\n\x06\x45nergy\x10\x01\x12\x08\n\x04Life\x10\x02\x12\x0b\n\x07Shields\x10\x03*\xb2\x01\n\x0e\x44\x65\x62ugGameState\x12\x0c\n\x08show_map\x10\x01\x12\x11\n\rcontrol_enemy\x10\x02\x12\x08\n\x04\x66ood\x10\x03\x12\x08\n\x04\x66ree\x10\x04\x12\x11\n\rall_resources\x10\x05\x12\x07\n\x03god\x10\x06\x12\x0c\n\x08minerals\x10\x07\x12\x07\n\x03gas\x10\x08\x12\x0c\n\x08\x63ooldown\x10\t\x12\r\n\ttech_tree\x10\n\x12\x0b\n\x07upgrade\x10\x0b\x12\x0e\n\nfast_build\x10\x0c')

_DEBUGGAMESTATE = DESCRIPTOR.enum_types_by_name['DebugGameState']
DebugGameState = enum_type_wrapper.EnumTypeWrapper(_DEBUGGAMESTATE)
show_map = 1
control_enemy = 2
food = 3
free = 4
all_resources = 5
god = 6
minerals = 7
gas = 8
cooldown = 9
tech_tree = 10
upgrade = 11
fast_build = 12


_DEBUGCOMMAND = DESCRIPTOR.message_types_by_name['DebugCommand']
_DEBUGDRAW = DESCRIPTOR.message_types_by_name['DebugDraw']
_LINE = DESCRIPTOR.message_types_by_name['Line']
_COLOR = DESCRIPTOR.message_types_by_name['Color']
_DEBUGTEXT = DESCRIPTOR.message_types_by_name['DebugText']
_DEBUGLINE = DESCRIPTOR.message_types_by_name['DebugLine']
_DEBUGBOX = DESCRIPTOR.message_types_by_name['DebugBox']
_DEBUGSPHERE = DESCRIPTOR.message_types_by_name['DebugSphere']
_DEBUGCREATEUNIT = DESCRIPTOR.message_types_by_name['DebugCreateUnit']
_DEBUGKILLUNIT = DESCRIPTOR.message_types_by_name['DebugKillUnit']
_DEBUGTESTPROCESS = DESCRIPTOR.message_types_by_name['DebugTestProcess']
_DEBUGSETSCORE = DESCRIPTOR.message_types_by_name['DebugSetScore']
_DEBUGENDGAME = DESCRIPTOR.message_types_by_name['DebugEndGame']
_DEBUGSETUNITVALUE = DESCRIPTOR.message_types_by_name['DebugSetUnitValue']
_DEBUGTESTPROCESS_TEST = _DEBUGTESTPROCESS.enum_types_by_name['Test']
_DEBUGENDGAME_ENDRESULT = _DEBUGENDGAME.enum_types_by_name['EndResult']
_DEBUGSETUNITVALUE_UNITVALUE = _DEBUGSETUNITVALUE.enum_types_by_name['UnitValue']
DebugCommand = _reflection.GeneratedProtocolMessageType('DebugCommand', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGCOMMAND,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugCommand)
  })
_sym_db.RegisterMessage(DebugCommand)

DebugDraw = _reflection.GeneratedProtocolMessageType('DebugDraw', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGDRAW,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugDraw)
  })
_sym_db.RegisterMessage(DebugDraw)

Line = _reflection.GeneratedProtocolMessageType('Line', (_message.Message,), {
  'DESCRIPTOR' : _LINE,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Line)
  })
_sym_db.RegisterMessage(Line)

Color = _reflection.GeneratedProtocolMessageType('Color', (_message.Message,), {
  'DESCRIPTOR' : _COLOR,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Color)
  })
_sym_db.RegisterMessage(Color)

DebugText = _reflection.GeneratedProtocolMessageType('DebugText', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGTEXT,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugText)
  })
_sym_db.RegisterMessage(DebugText)

DebugLine = _reflection.GeneratedProtocolMessageType('DebugLine', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGLINE,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugLine)
  })
_sym_db.RegisterMessage(DebugLine)

DebugBox = _reflection.GeneratedProtocolMessageType('DebugBox', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGBOX,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugBox)
  })
_sym_db.RegisterMessage(DebugBox)

DebugSphere = _reflection.GeneratedProtocolMessageType('DebugSphere', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGSPHERE,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugSphere)
  })
_sym_db.RegisterMessage(DebugSphere)

DebugCreateUnit = _reflection.GeneratedProtocolMessageType('DebugCreateUnit', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGCREATEUNIT,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugCreateUnit)
  })
_sym_db.RegisterMessage(DebugCreateUnit)

DebugKillUnit = _reflection.GeneratedProtocolMessageType('DebugKillUnit', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGKILLUNIT,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugKillUnit)
  })
_sym_db.RegisterMessage(DebugKillUnit)

DebugTestProcess = _reflection.GeneratedProtocolMessageType('DebugTestProcess', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGTESTPROCESS,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugTestProcess)
  })
_sym_db.RegisterMessage(DebugTestProcess)

DebugSetScore = _reflection.GeneratedProtocolMessageType('DebugSetScore', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGSETSCORE,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugSetScore)
  })
_sym_db.RegisterMessage(DebugSetScore)

DebugEndGame = _reflection.GeneratedProtocolMessageType('DebugEndGame', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGENDGAME,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugEndGame)
  })
_sym_db.RegisterMessage(DebugEndGame)

DebugSetUnitValue = _reflection.GeneratedProtocolMessageType('DebugSetUnitValue', (_message.Message,), {
  'DESCRIPTOR' : _DEBUGSETUNITVALUE,
  '__module__' : 's2clientprotocol.debug_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.DebugSetUnitValue)
  })
_sym_db.RegisterMessage(DebugSetUnitValue)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DEBUGGAMESTATE._serialized_start=1897
  _DEBUGGAMESTATE._serialized_end=2075
  _DEBUGCOMMAND._serialized_start=80
  _DEBUGCOMMAND._serialized_end=523
  _DEBUGDRAW._serialized_start=526
  _DEBUGDRAW._serialized_end=707
  _LINE._serialized_start=709
  _LINE._serialized_end=785
  _COLOR._serialized_start=787
  _COLOR._serialized_end=827
  _DEBUGTEXT._serialized_start=830
  _DEBUGTEXT._serialized_end=993
  _DEBUGLINE._serialized_start=995
  _DEBUGLINE._serialized_end=1080
  _DEBUGBOX._serialized_start=1082
  _DEBUGBOX._serialized_end=1202
  _DEBUGSPHERE._serialized_start=1204
  _DEBUGSPHERE._serialized_end=1300
  _DEBUGCREATEUNIT._serialized_start=1302
  _DEBUGCREATEUNIT._serialized_end=1409
  _DEBUGKILLUNIT._serialized_start=1411
  _DEBUGKILLUNIT._serialized_end=1439
  _DEBUGTESTPROCESS._serialized_start=1442
  _DEBUGTESTPROCESS._serialized_end=1570
  _DEBUGTESTPROCESS_TEST._serialized_start=1533
  _DEBUGTESTPROCESS_TEST._serialized_end=1570
  _DEBUGSETSCORE._serialized_start=1572
  _DEBUGSETSCORE._serialized_end=1602
  _DEBUGENDGAME._serialized_start=1604
  _DEBUGENDGAME._serialized_end=1726
  _DEBUGENDGAME_ENDRESULT._serialized_start=1680
  _DEBUGENDGAME_ENDRESULT._serialized_end=1726
  _DEBUGSETUNITVALUE._serialized_start=1729
  _DEBUGSETUNITVALUE._serialized_end=1894
  _DEBUGSETUNITVALUE_UNITVALUE._serialized_start=1848
  _DEBUGSETUNITVALUE_UNITVALUE._serialized_end=1894
# @@protoc_insertion_point(module_scope)
