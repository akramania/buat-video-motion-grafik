"""Timing helpers for persistent scenes, using seconds rather than a 0..5 clock.

cue(cfg, key, default) changes *when* an action starts. progress(t, start,
length, cfg) changes *how fast* it moves. Increasing tempo shortens only the
movement length; it never compresses cue spacing, scene duration or reading
holds. All functions are deterministic and safe for random frame rendering.
"""
import math
from core import clamp, ease, smooth


def cue(cfg, key, default):
    """Return an absolute cue time in output seconds."""
    value = cfg.get('cues', {}).get(key, default)
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError('cue ' + str(key) + ' must be a finite, nonnegative time')
    return value


def progress(t, start, length, cfg):
    """Linear 0..1 action progress; tempo changes length, never start time."""
    tempo = float(cfg.get('tempo', 1))
    if not math.isfinite(tempo) or not .5 <= tempo <= 2:
        raise ValueError('tempo must be between 0.5 and 2')
    if length <= 0:
        return float(t >= start)
    return clamp((t - start) / (length / tempo))


def lifecycle(t, start, end, cfg, in_length=.42, out_length=.34):
    """Return eased visibility for an object whose exit begins at end.

    Explicit start/end cues remain fixed when tempo changes. Renderers can use
    this alpha for a layer and animate position with the same progress helper.
    """
    return ease(progress(t, start, in_length, cfg)) * (1 - smooth(progress(t, end, out_length, cfg)))


def action(t, cfg, key, default, length=.42, easing=ease):
    """Convenience combination: a named cue followed by an eased action."""
    return easing(progress(t, cue(cfg, key, default), length, cfg))
