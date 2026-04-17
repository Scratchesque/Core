from dataclasses import dataclass


@dataclass(frozen=True)
class BlockSpec:
    id: str
    label: str
    action: str
    x: int = 0
    y: int = 0


DEFAULT_BLOCK_LIBRARY = (
    BlockSpec("up", "Move Up", "up", y=-1),
    BlockSpec("down", "Move Down", "down", y=1),
    BlockSpec("left", "Move Left", "left", x=-1),
    BlockSpec("right", "Move Right", "right", x=1),
    BlockSpec("jump", "Jump", "jump"),
    BlockSpec("jump_left", "Jump Left", "jump", x=-2),
    BlockSpec("jump_right", "Jump Right", "jump", x=2),
    BlockSpec("jump_up", "Jump Up", "jump", y=-2),
    BlockSpec("jump_down", "Jump Down", "jump", y=2),
)


def get_block_library(allowed_block_ids=None):
    if not allowed_block_ids:
        return list(DEFAULT_BLOCK_LIBRARY)

    allowed_ids = set(allowed_block_ids)
    return [spec for spec in DEFAULT_BLOCK_LIBRARY if spec.id in allowed_ids]
