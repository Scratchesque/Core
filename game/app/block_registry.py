from dataclasses import dataclass


@dataclass(frozen=True)
class BlockSpec:
    id: str
    label: str
    object_id: str
    action: str = ""
    x: int = 0
    y: int = 0


DEFAULT_BLOCK_LIBRARY = (
    BlockSpec("up", "Move Up", "#motion_block", "up", y=-1),
    BlockSpec("down", "Move Down", "#motion_block", "down", y=1),
    BlockSpec("left", "Move Left", "#motion_block", "left", x=-1),
    BlockSpec("right", "Move Right", "#motion_block", "right", x=1),
    BlockSpec("jump", "Jump", "#jump_block", "jump"),
    BlockSpec("jump_left", "Jump Left", "#jump_block", "jump", x=-2),
    BlockSpec("jump_right", "Jump Right", "#jump_block", "jump", x=2),
    BlockSpec("jump_up", "Jump Up", "#jump_block", "jump", y=-2),
    BlockSpec("jump_down", "Jump Down", "#jump_block", "jump", y=2),
    BlockSpec("loop","Loop", "#loop_block"),

    BlockSpec("fix_up", "Move Up", "#motion_block", "up", y=1),
    BlockSpec("fix_down", "Move Down", "#motion_block", "down", y=-1),
    BlockSpec("fix_left", "Move Left", "#motion_block", "left", x=1),
    BlockSpec("fix_right", "Move Right", "#motion_block", "right", x=-1),
    BlockSpec("fix_jump_left", "Jump Left", "#jump_block", "jump", x=1),
    BlockSpec("fix_jump_right", "Jump Right", "#jump_block", "jump", x=-1),
    BlockSpec("fix_jump_up", "Jump Up", "#jump_block", "jump", y=1),
    BlockSpec("fix_jump_down", "Jump Down", "#jump_block", "jump", y=-1),
)

def get_block_library(allowed_block_ids=None):
    if not allowed_block_ids:
        return list(DEFAULT_BLOCK_LIBRARY)

    allowed_ids = set(allowed_block_ids)
    return [spec for spec in DEFAULT_BLOCK_LIBRARY if spec.id in allowed_ids]
