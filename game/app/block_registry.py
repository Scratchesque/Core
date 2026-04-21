from dataclasses import dataclass


@dataclass(frozen=True)
class BlockSpec:
    id: str
    label: str
    object_id: str
    action: str
    x: int = 0
    y: int = 0


DEFAULT_BLOCK_LIBRARY = (
    BlockSpec("up", "Move Up", "#motion_block", "up", y=-1),
    BlockSpec("down", "Move Down", "#motion_block", "down", y=1),
    BlockSpec("left", "Move Left", "#motion_block", "left", x=-1),
    BlockSpec("right", "Move Right", "#motion_block", "right", x=1),
    BlockSpec("jump", "Jump", "#motion_block", "jump"),
    BlockSpec("jump_left", "Jump Left", "#motion_block", "jump", x=-2),
    BlockSpec("jump_right", "Jump Right", "#motion_block", "jump", x=2),
    BlockSpec("jump_up", "Jump Up", "#motion_block", "jump", y=-2),
    BlockSpec("jump_down", "Jump Down", "#motion_block", "jump", y=2),
    BlockSpec("loop","Loop", "#loop_block","")
)


def get_block_library(allowed_block_ids=None):
    if not allowed_block_ids:
        return list(DEFAULT_BLOCK_LIBRARY)

    allowed_ids = set(allowed_block_ids)
    return [spec for spec in DEFAULT_BLOCK_LIBRARY if spec.id in allowed_ids]
