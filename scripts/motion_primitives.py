"""Original deterministic motion/layout helpers; no renderer or third-party assets.

All timeline values are seconds. Evaluate at frame_time = frame_index / fps,
never by accumulating frame deltas. Positions/sizes use one caller-chosen unit.
Spring values can overshoot: use them for transforms, not opacity or clipping.
"""

from dataclasses import dataclass
import math
import random
from typing import Sequence


def _number(name: str, value: float, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} must be finite") from exc
    if not math.isfinite(value) or (minimum is not None and value < minimum):
        raise ValueError(f"{name} must be finite and >= {minimum}")
    return value


def _positive(name: str, value: float) -> float:
    value = _number(name, value, 0)
    if value == 0:
        raise ValueError(f"{name} must be > 0")
    return value


def _integer(name: str, value: int, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def progress(time: float, start: float, duration: float) -> float:
    """Clamped 0..1 progress; positive duration prevents accidental hard cuts."""
    time, start = _number("time", time), _number("start", start)
    duration = _positive("duration", duration)
    end = _number("end", start + duration)
    if end <= start:
        raise ValueError("duration is below the time coordinate's precision")
    if time <= start:
        return 0.0
    if time >= end:
        return 1.0
    return (time - start) / duration


def ease(p: float, curve: str = "smooth") -> float:
    """Bounded easing: linear, smooth, smoother, out_cubic, in_out_cubic."""
    p = min(1.0, max(0.0, _number("p", p)))
    if curve == "linear":
        return p
    if curve == "smooth":
        return p * p * (3 - 2 * p)
    if curve == "smoother":
        return min(1.0, max(0.0, p * p * p * (p * (p * 6 - 15) + 10)))
    if curve == "out_cubic":
        return 1 - (1 - p) ** 3
    if curve == "in_out_cubic":
        return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2
    raise ValueError(f"unknown easing curve: {curve}")


def spring(p: float, damping: float = 6.0, cycles: float = 1.1) -> float:
    """Damped oscillation with exact 0/1 endpoints and zero endpoint velocity.

    A cosine-squared taper settles the response by p=1. This is an art-directed
    easing curve, not a physical simulation. Overshoot is intentional.
    """
    p = min(1.0, max(0.0, _number("p", p)))
    damping, cycles = _number("damping", damping, 0), _positive("cycles", cycles)
    if damping > 100 or not 0.01 <= cycles <= 20:
        raise ValueError("use damping 0..100 and cycles 0.01..20")
    if p in (0.0, 1.0):
        return p
    w = 2 * math.pi * cycles
    response = math.cos(w * p) + damping / w * math.sin(w * p)
    return 1 - math.exp(-damping * p) * response * math.cos(math.pi * p / 2) ** 2


@dataclass(frozen=True)
class Cue:
    index: int
    start: float
    end: float


def stagger(count: int, start: float = 0.0, duration: float = 0.45,
            step: float = 0.08, order: str = "forward", seed: int = 0,
            allow_overlap: bool = True, end: float | None = None) -> list[Cue]:
    """Return cues in original item order, with starts assigned in chosen order.

    Orders: forward, reverse, center_out, edges_in, random (local seeded RNG).
    Overlap is normal for glyph reveals; disable it for exclusive text beats.
    Optional end is a hard budget with a small floating-point rounding tolerance.
    """
    count, seed = _integer("count", count), _integer("seed", seed)
    start, duration = _number("start", start), _positive("duration", duration)
    step = _number("step", step, 0)
    if not isinstance(allow_overlap, bool):
        raise ValueError("allow_overlap must be bool")
    if not allow_overlap and count > 1 and step < duration:
        raise ValueError("step must be >= duration when overlap is disabled")
    indices = list(range(count))
    if order == "reverse":
        indices.reverse()
    elif order in ("center_out", "edges_in"):
        indices.sort(key=lambda i: (abs(i - (count - 1) / 2), i))
        if order == "edges_in":
            indices.sort(key=lambda i: (-abs(i - (count - 1) / 2), i))
    elif order == "random":
        random.Random(seed).shuffle(indices)
    elif order != "forward":
        raise ValueError(f"unknown stagger order: {order}")
    if end is not None:
        end = _number("end", end)
    if not count:
        return []
    finish = _number("finish", start + max(0, count - 1) * step + duration)
    if end is not None:
        tolerance = 8 * max(math.ulp(finish), math.ulp(end))
        if finish - end > tolerance:
            raise ValueError(f"stagger finishes at {finish:g}s, past end={end:g}s")
    cues = []
    for rank, index in enumerate(indices):
        begin = start + rank * step
        if begin + duration <= begin:
            raise ValueError("duration is below the time coordinate's precision")
        cues.append(Cue(index, begin, begin + duration))
    return sorted(cues, key=lambda cue: cue.index)


@dataclass(frozen=True)
class Phase:
    name: str
    progress: float
    visibility: float


def in_hold_out(time: float, start: float = 0.0, in_duration: float = 0.4,
                hold: float = 1.0, out_duration: float = 0.3,
                curve: str = "smooth") -> Phase:
    """Return phase-local progress and a bounded visibility envelope.

    Phases are before/in/hold/out/after. in/out must be positive; hold may be 0.
    In/out progress drives distinct transforms; visibility is suitable for alpha.
    """
    time, start = _number("time", time), _number("start", start)
    in_duration, out_duration = _positive("in_duration", in_duration), _positive("out_duration", out_duration)
    hold = _number("hold", hold, 0)
    entered, leaving = start + in_duration, start + in_duration + hold
    end = _number("end", leaving + out_duration)
    if entered <= start or end <= leaving or (hold > 0 and leaving <= entered):
        raise ValueError("phase duration is below the time coordinate's precision")
    ease(0, curve)  # Validate even outside the active interval.
    if time < start:
        return Phase("before", 0.0, 0.0)
    if time < entered:
        p = progress(time, start, in_duration)
        return Phase("in", p, ease(p, curve))
    if time < leaving:
        return Phase("hold", progress(time, entered, hold), 1.0)
    if time < end:
        p = progress(time, leaving, out_duration)
        return Phase("out", p, 1 - ease(p, curve))
    return Phase("after", 1.0, 0.0)


@dataclass(frozen=True)
class CarouselPose:
    index: int
    relative: float
    x: float
    scale: float
    depth: float
    yaw_degrees: float
    visible: bool


def carousel(count: int, focus: float, spacing: float, card_width: float,
             viewport_width: float, depth_falloff: float = 0.12,
             max_tilt: float = 12.0) -> list[CarouselPose]:
    """Centered cyclic poses; focus is a continuous item coordinate.

    Draw visible cards in increasing depth order. Wrap is discontinuous by
    design and MUST occur offscreen; reject rings too short to hide the seam.
    Supply card_width including shadows/effects, or use padded clipping. Add
    duplicate items to lengthen a short ring. No perspective renderer is implied.
    """
    count, focus = _integer("count", count, 2), _number("focus", focus)
    spacing, card_width = _positive("spacing", spacing), _positive("card_width", card_width)
    viewport_width = _positive("viewport_width", viewport_width)
    depth_falloff, max_tilt = _number("depth_falloff", depth_falloff, 0), _number("max_tilt", max_tilt, 0)
    if max_tilt > 60 or depth_falloff > 100:
        raise ValueError("max_tilt must be <= 60; depth_falloff must be <= 100")
    ring_width = _number("ring_width", count * spacing)
    if ring_width < _number("required_width", viewport_width + card_width):
        raise ValueError("wrap seam would be visible: increase count or spacing")
    poses = []
    focus %= count
    for index in range(count):
        relative = (index - focus + count / 2) % count - count / 2
        x = relative * spacing
        scale = 1 / (1 + depth_falloff * abs(relative))
        poses.append(CarouselPose(index, relative, x, scale, 1 / (1 + abs(relative)),
                                  -max_tilt * min(1, max(-1, relative)),
                                  abs(x) < (viewport_width + card_width * scale) / 2))
    return poses


@dataclass(frozen=True)
class StackCard:
    index: int
    y: float
    height: float


def notification_stack(heights: Sequence[float], origin: float = 0.0,
                       gap: float = 12.0, anchor: str = "top") -> list[StackCard]:
    """Lay out measured card heights without overlap; y is always the top edge.

    Item 0 is nearest origin. For top anchor, origin is the top edge; for bottom
    anchor it is the bottom edge. Include effects in heights. This is endpoint
    layout, not collision avoidance for arbitrary independently animated paths.
    """
    origin, gap = _number("origin", origin), _number("gap", gap, 0)
    if anchor not in ("top", "bottom"):
        raise ValueError("anchor must be top or bottom")
    cards, cursor = [], origin
    for index, height in enumerate(heights):
        height = _positive(f"height[{index}]", height)
        y = cursor if anchor == "top" else cursor - height
        next_cursor = y + height + gap if anchor == "top" else y - gap
        if _number("card bottom", y + height) <= y:
            raise ValueError("height is below the position coordinate's precision")
        cards.append(StackCard(index, _number("y", y), height))
        cursor = _number("cursor", next_cursor)
    return cards
