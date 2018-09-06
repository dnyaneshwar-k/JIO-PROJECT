# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: scenewise.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='scenewise.proto',
  package='tutorial',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0fscenewise.proto\x12\x08tutorial\"9\n\x07Objects\x12\x12\n\nclass_name\x18\x01 \x01(\t\x12\x0c\n\x04\x63onf\x18\x02 \x01(\x02\x12\x0c\n\x04\x62\x62ox\x18\x03 \x01(\t\"9\n\x05\x46rame\x12\x0f\n\x07\x66rameno\x18\x01 \x01(\x05\x12\x1f\n\x04objs\x18\x02 \x03(\x0b\x32\x11.tutorial.Objects\"m\n\x05Scene\x12\x10\n\x08video_id\x18\x01 \x01(\t\x12\x0c\n\x04s_no\x18\x02 \x01(\x05\x12\x10\n\x08str_time\x18\x03 \x01(\t\x12\x11\n\tstop_time\x18\x04 \x01(\t\x12\x1f\n\x06\x66rames\x18\x05 \x03(\x0b\x32\x0f.tutorial.Frame\"-\n\nScene_list\x12\x1f\n\x06scenes\x18\x01 \x03(\x0b\x32\x0f.tutorial.Sceneb\x06proto3')
)




_OBJECTS = _descriptor.Descriptor(
  name='Objects',
  full_name='tutorial.Objects',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_name', full_name='tutorial.Objects.class_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conf', full_name='tutorial.Objects.conf', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bbox', full_name='tutorial.Objects.bbox', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=86,
)


_FRAME = _descriptor.Descriptor(
  name='Frame',
  full_name='tutorial.Frame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='frameno', full_name='tutorial.Frame.frameno', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='objs', full_name='tutorial.Frame.objs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=88,
  serialized_end=145,
)


_SCENE = _descriptor.Descriptor(
  name='Scene',
  full_name='tutorial.Scene',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='video_id', full_name='tutorial.Scene.video_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='s_no', full_name='tutorial.Scene.s_no', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='str_time', full_name='tutorial.Scene.str_time', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop_time', full_name='tutorial.Scene.stop_time', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='frames', full_name='tutorial.Scene.frames', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=256,
)


_SCENE_LIST = _descriptor.Descriptor(
  name='Scene_list',
  full_name='tutorial.Scene_list',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='scenes', full_name='tutorial.Scene_list.scenes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=258,
  serialized_end=303,
)

_FRAME.fields_by_name['objs'].message_type = _OBJECTS
_SCENE.fields_by_name['frames'].message_type = _FRAME
_SCENE_LIST.fields_by_name['scenes'].message_type = _SCENE
DESCRIPTOR.message_types_by_name['Objects'] = _OBJECTS
DESCRIPTOR.message_types_by_name['Frame'] = _FRAME
DESCRIPTOR.message_types_by_name['Scene'] = _SCENE
DESCRIPTOR.message_types_by_name['Scene_list'] = _SCENE_LIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Objects = _reflection.GeneratedProtocolMessageType('Objects', (_message.Message,), dict(
  DESCRIPTOR = _OBJECTS,
  __module__ = 'scenewise_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.Objects)
  ))
_sym_db.RegisterMessage(Objects)

Frame = _reflection.GeneratedProtocolMessageType('Frame', (_message.Message,), dict(
  DESCRIPTOR = _FRAME,
  __module__ = 'scenewise_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.Frame)
  ))
_sym_db.RegisterMessage(Frame)

Scene = _reflection.GeneratedProtocolMessageType('Scene', (_message.Message,), dict(
  DESCRIPTOR = _SCENE,
  __module__ = 'scenewise_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.Scene)
  ))
_sym_db.RegisterMessage(Scene)

Scene_list = _reflection.GeneratedProtocolMessageType('Scene_list', (_message.Message,), dict(
  DESCRIPTOR = _SCENE_LIST,
  __module__ = 'scenewise_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.Scene_list)
  ))
_sym_db.RegisterMessage(Scene_list)


# @@protoc_insertion_point(module_scope)