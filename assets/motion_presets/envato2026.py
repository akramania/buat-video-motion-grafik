"""120 original implementations informed by 28 inspected public previews.

No Envato template, source photograph, preview clip, audio or stock icon is bundled.
Time uses the normalized 0..5 renderer clock. Each mode has a distinct scene recipe.
"""
import json
from pathlib import Path
from core import *
from envato_common import *
from envato_maps_workflows import maps,workflow,planner
from envato_widgets import counters,widgets
from envato_charts import charts
from envato_infographics import infographics,matches
from envato_effects import effects
from envato_type import typography

PRESETS=json.loads((Path(__file__).parent/'envato_index.json').read_text())
CHARTS={'radar','radar_profile','nested_rings','profile_rings','donut','pie_legend','funnel','rank_bars','rank_steps','social_rank','butterfly','mirror_bars','social_columns','doc_bars','doc_line'}

def render(pid,t,cfg):
    cfg=dict(cfg);cfg['mode']=PRESETS[pid]['mode']
    mode=cfg['mode']
    if mode.startswith('map_'):im=maps(t,cfg)
    elif mode.startswith('workflow_') or mode=='stream_merge':im=workflow(t,cfg)
    elif mode.startswith('planner_') or mode=='agenda':im=planner(t,cfg)
    elif mode.startswith('counter_'):im=counters(t,cfg)
    elif mode.startswith(('glass_','widget_')) or mode in ('kpi_stack','automation_bars'):im=widgets(t,cfg)
    elif mode.startswith('chart_') or mode in CHARTS:im=charts(t,cfg)
    elif mode.startswith('match_'):im=matches(t,cfg)
    elif mode.startswith(('camera_','rip_')):im=effects(t,cfg)
    elif mode.startswith(('type_','hook_')):im=typography(t,cfg)
    elif mode=='doc_headline':
        cfg['mode']='type_marker';im=typography(t,cfg)
    else:im=infographics(t,cfg)
    # Preserve a full clean endpoint for transitions; other components exit gently.
    if not mode.startswith(('camera_','rip_','map_')) and t>4.7:
        im=Image.blend(base(cfg),im,1-smooth(prog(t,4.7,5)))
    return im
