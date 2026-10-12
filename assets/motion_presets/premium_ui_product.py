"""100 original UI/product motion recipes PX201--PX300.

Envato listing descriptions inform category choice only. This module contains
original Pillow geometry, layouts and choreography; no Envato files or frames.
Perspective devices are 2.5D planes, not a 3D renderer. Input images are contained
in their screen/product windows, preserving the complete source aspect ratio.
Public clock is normalized 0..5; atlas clips use duration=6 seconds.
"""
from core import *
from PIL import ImageOps
import json

SOURCES={
 'workflow':'https://elements.envato.com/ai-workflow-dashboard-LMEXHCD',
 'glass':'https://elements.envato.com/glassmorphism-saas-ui-kit-FMYXDXU',
 'widget':'https://elements.envato.com/liquid-glass-widgets-XDX2XW7',
 'data':'https://elements.envato.com/liquid-glass-ui-widgets-2YNLYSD',
 'mobile':'https://elements.envato.com/glass-liquid-app-promo-4G9SSF6',
 'phone':'https://elements.envato.com/app-promo-phone-13-blue-Y55LXFL',
 'shop':'https://elements.envato.com/shopping-and-sales-website-for-furniture-desktop-a-L33YHY2',
 'product':'https://elements.envato.com/product-promo-ZXVZVNR',
 'hardware':'https://elements.envato.com/hardware-store-B5DW8TA',
}

# Each row is a separate choreography and interaction, not a colour preset.
RECIPES=[
 ('workflow','AI Parallel Branches','Trigger divides into research and media branches, then converges.','Branch edges reveal sequentially; two independently travelling packets converge.','parallel-fork-join'),
 ('workflow','Human Approval Gate','Execution pauses at an approval card before release to delivery.','Diamond gate expands; pending card docks; approval unlocks downstream edge.','approval-gate'),
 ('workflow','Workflow Retry Loop','A failed processing node reconnects through a corrective retry path.','Failure flash, three-segment loop trace and second-pass success state.','retry-loop'),
 ('workflow','Source Fan-In','Three data inputs merge into a single structured output bundle.','Staggered source ingestion, collection node and output payload expansion.','source-fan-in'),
 ('workflow','Prompt Instruction Stack','Role, task and format cards assemble into one prompt workspace.','Three instruction strips dock in ordered slots and a run button activates.','instruction-stack'),
 ('workflow','Prompt Variable Binding','Named input variables connect to highlighted placeholders.','Variable chips travel to template sockets; final prompt resolves bindings.','variable-binding'),
 ('workflow','Prompt Source Attach','Reference documents attach beside a prompt and enter the context meter.','Document tiles dock; context capacity fills; prompt run becomes ready.','context-attachment'),
 ('workflow','Prompt Rewrite Compare','A rough instruction is refined into a structured prompt.','Before/after panes; selected fragments convert into three constrained rows.','prompt-rewrite'),
 ('workflow','AI Token Stream','Response lines arrive in readable blocks with an active cursor.','Timed line growth, cursor blink and completed answer footer.','response-stream'),
 ('workflow','AI Citation Answer','An answer builds while source chips resolve to evidence cards.','Sentence reveal with numbered reference chips and matching source-side highlights.','citation-resolve'),
 ('workflow','AI Agent Consensus','Three agents generate concise findings which settle into a summary.','Independent response progress strips, vote convergence and consensus panel.','agent-consensus'),
 ('workflow','AI Chat Refinement','A follow-up query revises a previous assistant answer.','Conversation bubble entry followed by replacement answer rows and change markers.','chat-refine'),
 ('glass','Predictive Search','Typed text produces a ranked suggestion dropdown.','Character reveal, suggestion rows and keyboard focus travelling between options.','predictive-search'),
 ('glass','Facet Result Filtering','Result tiles reduce as filter chips switch on.','Filter toggles reflow a six-item grid into three selected results.','facet-reflow'),
 ('glass','Command Palette Launch','A keyboard command opens actions and launches the chosen workspace.','Compact shortcut expands into command list then a selected destination panel.','command-launch'),
 ('glass','Semantic Search Matches','A query matches meaning across three differently worded results.','Query-to-result connecting lines and progressively filling relevance bars.','semantic-results'),
 ('glass','Notification Inbox Cascade','New alerts dock in an inbox with unread markers.','Staggered alert translation, stack compression and unread count update.','inbox-cascade'),
 ('widget','Background Task Toast','An upload task moves from progress to a completed notification.','Progress pill elongates; completion tick replaces spinner and action appears.','progress-toast'),
 ('glass','Notification Digest Group','Related alerts gather into one expandable digest.','Individual alerts converge into grouped summary then child cards open beneath.','digest-group'),
 ('glass','Notification Priority Triage','An urgent notification rises above routine status messages.','Priority message lifts into focus while routine rows settle into a quiet stack.','priority-triage'),
 ('workflow','Kanban Drag Commit','A task card moves from planned to active and finally completed.','Pointer-driven curved drag, target lane highlight and completed status badge.','kanban-drag'),
 ('workflow','Kanban Dependency Merge','Two dependent task cards merge into a delivery card.','Parallel lanes fill; prerequisite cards join a central review slot.','dependency-merge'),
 ('workflow','Kanban Team Assignment','A task acquires an owner then joins an assigned work queue.','Avatar chip docks, assignment border activates and queue card inserts.','owner-assign'),
 ('workflow','Kanban Status Split','A completed task produces separate review and publish cards.','Main card opens into two linked child tasks with independent progress states.','status-split'),
 ('data','Dashboard Bento Assemble','Analytics widgets gather into a balanced dashboard.','Metric, graph, task and activity panels enter with separate depth offsets.','bento-assemble'),
 ('data','Dashboard Live Monitor','A live monitoring screen updates performance and event feed.','Scrolling heartbeat path, numeric samples and staggered log-row activation.','live-monitor'),
 ('data','Dashboard Detail Drill','A selected metric expands into a detailed report pane.','One tile morphs into a split report with chart and table revelation.','detail-drill'),
 ('data','Dashboard KPI Spotlight','A key metric gains focus while supporting widgets settle beside it.','Hero counter scales into focus; context sparkline and compact comparison appear.','kpi-spotlight'),
 ('shop','Checkout Step Completion','A customer proceeds from details through payment to confirmation.','Step nodes progress, input fields validate and completion card lifts.','checkout-steps'),
 ('shop','Cart Summary Drawer','Product cards collect into a checkout summary drawer.','Items transfer into cart rows, subtotal recalculates and checkout button unlocks.','cart-drawer'),
 ('product','Invoice Payment Receipt','Invoice rows consolidate into a paid receipt.','Ledger rows enter, total emphasis and payment-stamp outline draw.','invoice-receipt'),
 ('product','Coupon Price Resolve','A coupon is applied and the product price updates clearly.','Coupon chip docks, price comparison resolves and discounted total slides in.','coupon-resolve'),
 ('glass','Settings Toggle Rack','Three software features turn on with dependent status updates.','Sequential toggle travel and accompanying live status chip replacements.','toggle-rack'),
 ('glass','Precision Slider Controls','Three sliders alter an associated visual preview.','Slider knobs move to distinct targets while preview geometry changes in response.','precision-sliders'),
 ('glass','Theme Mode Split','A design panel transitions between light and dark themes.','Clipped theme boundary moves across a shared layout and controls synchronise.','theme-split'),
 ('glass','Permissions Access Matrix','Role permissions are enabled in a structured matrix.','Permission cells light in column order; selected role summary updates.','access-matrix'),
 ('glass','Audio Wave Player','An audio player runs with a progress waveform and transport controls.','Wave segments activate against playhead, elapsed time updates and pause docks.','wave-player'),
 ('glass','Playlist Track Handoff','Three tracks rotate through an active playback queue.','Selected track elevation, album tile swap and active row progress.','playlist-handoff'),
 ('glass','Video Chapter Navigator','A video interface highlights chapters along a timeline.','Chapter tabs progress; screen content changes with a moving playhead.','chapter-nav'),
 ('widget','Voice Record Capture','A voice recorder captures waveform energy then exports a clip.','Recording pulse, live amplitude trace and export-ready file panel.','record-capture'),
 ('mobile','Calendar Week Booking','An open weekly slot is selected and turns into a booked event.','Day columns reveal, slot highlight grows and confirmation card attaches.','week-booking'),
 ('mobile','Schedule Time Track','Tasks settle into a horizontal schedule with a current-time marker.','Duration blocks stretch into time slots; current-time line crosses the day.','time-track'),
 ('mobile','Event Invitation Card','An event invitation opens with attendee responses.','Invitation card unfolds, attendee badges pop and RSVP confirmation completes.','event-invitation'),
 ('mobile','Calendar Date Range','A date range selection extends across a monthly grid.','Start/end markers sweep over dates and range summary updates beneath.','date-range'),
 ('workflow','Drag File Attachment','A document is dropped into a dashed upload area.','File follows a curved path into a highlighted drop zone then becomes attached.','drag-file'),
 ('workflow','Batch Transfer Queue','Several files upload with independent progress then complete.','Three queue rows progress at staggered rates and switch to checked state.','batch-transfer'),
 ('workflow','Cloud Sync Compare','Local and cloud file lists reconcile changes.','Changed rows bridge two panes, sync packets travel and matched status appears.','sync-compare'),
 ('workflow','Export Format Picker','A design export selects a format and generates a downloadable file.','Format chips expand, selected option compresses into export progress and file tile.','format-export'),
 ('phone','Phone 2.5D Orbit','A contained mobile screen tilts through a shallow camera-like orbit.','Perspective-warped plane changes yaw with a fixed readable screen and feature callouts.','phone-orbit-2.5d'),
 ('mobile','Phone Feature Unpack','App feature cards separate from a phone screen into a clear diagram.','Phone holds center; three screen-derived feature tiles fan into labelled side positions.','phone-feature-unpack'),
 ('phone','Phone Screen Handoff','Two phone interfaces hand off content between devices.','Paired phones enter; message token crosses bridge; destination screen status changes.','phone-screen-handoff'),
 ('phone','Phone Scroll Reveal','A smartphone scrolls a list while one selected feature enlarges outside it.','Clipped list scroll, selected-row match and linked magnification callout.','phone-scroll-reveal'),
 ('shop','Responsive Device Triad','One UI adapts from desktop to tablet and mobile.','Three device planes settle; content reorganises for their aspect ratios.','responsive-triad'),
 ('shop','Device Content Relay','A selected product moves from desktop view to mobile continuation.','Desktop highlight launches a contained image token which docks into phone screen.','device-content-relay'),
 ('shop','Browser Window Cascade','Three browser panels stack into a website feature presentation.','Window depth cascade followed by foreground feature-tab activation.','browser-cascade'),
 ('shop','Tablet Split Workspace','A tablet displays two coordinated working panels.','Tablet plane stabilises; split divider moves and active pane expands.','tablet-split'),
 ('hardware','Product Specification Pins','A product hero receives numbered specification callouts.','Contained product silhouette reveals; pin stems trace to clear specification cards.','specification-pins'),
 ('product','Product Colour Options','A product display responds to selected finish chips.','Finish selectors activate; schematic surface changes and selected label updates.','finish-options'),
 ('hardware','Product Layer Explode','A schematic product separates into functional layers.','Three original geometric layers separate vertically with connector stems and labels.','layer-explode'),
 ('product','Product Feature Inspection','A focused feature window tracks detail on a complete product image.','Product stays contained; inspection frame and separate linked detail panel travel.','feature-inspection'),
 ('product','Gallery Filmstrip Select','A filmstrip selection promotes one image into a hero panel.','Thumbnails populate, selector travels and selected image appears in contained hero window.','filmstrip-select'),
 ('product','Gallery Masonry Focus','A varied-size product gallery consolidates around a chosen image.','Masonry cells enter; selected tile expands while supporting thumbnails dock.','masonry-focus'),
 ('product','Gallery Comparison Slider','Two product windows compare options across a shared frame.','Clipped compare boundary sweeps across contained views with labelled option chips.','comparison-slider'),
 ('product','Gallery Collection Fan','A product collection fans out from a central hero.','Three contained photo cards radiate into stable viewing slots with staggered captions.','collection-fan'),
 ('workflow','Code Build Console','A build console progresses from command input to successful output.','Command typing, ordered log growth and build-state banner activation.','build-console'),
 ('workflow','Code Deploy Stages','A release moves through test, package and deployment stages.','Stage cards fill independently then connect to a released version tile.','deploy-stages'),
 ('workflow','Code Diff Merge','Two code fragments combine into a reviewed result.','Original and modified rows align; added lines converge into a merge pane.','diff-merge'),
 ('workflow','API Request Response','An API request crosses a server bridge and returns structured data.','Request packet trace, response JSON growth and status badge reveal.','request-response'),
 ('glass','Security Access Unlock','A login card validates fields then opens a protected workspace.','Field checks, lock shackle lift and dashboard card emergence.','access-unlock'),
 ('glass','Security Device Verify','A new device joins a verified account session.','Device token pairs with account card; verification code cells fill and trust state activates.','device-verify'),
 ('glass','Security Shield Scan','A structured security scan checks three categories.','Scanner line travels over shield; check rows complete with separate category progress.','shield-scan'),
 ('glass','Security Passkey Connect','A passkey card connects a device to a secure session.','Biometric ring trace, token bridge and protected-session panel reveal.','passkey-connect'),
 ('glass','Team Cursor Collaboration','Multiple team cursors contribute to a shared board.','Distinct named cursors travel toward edits; selected blocks animate and comments dock.','cursor-collaboration'),
 ('glass','Team Review Thread','A design comment thread gains replies and resolves.','Pinned comment opens, two replies dock and resolved chip attaches.','review-thread'),
 ('glass','Team Presence Grid','A workspace introduces online collaborators and shared tasks.','Presence avatars join independently; associated task chips populate beneath.','presence-grid'),
 ('glass','Team File Handoff','A completed file passes from one collaborator to another.','Source/destination profile cards, curved file transfer and receipt confirmation.','file-handoff'),
 ('mobile','Onboarding Progress Route','A new user proceeds through three meaningful setup steps.','Stepper progresses while each configuration panel swaps into the focus slot.','onboarding-route'),
 ('mobile','Onboarding Feature Tour','A feature guide highlights sections of a working interface.','Spotlight outline moves between three regions with context-specific explanatory card.','feature-tour'),
 ('mobile','Onboarding Profile Setup','A new profile gains an avatar, role and preferences.','Profile fields populate in order; preview card grows and ready state completes.','profile-setup'),
 ('mobile','Onboarding Import Choice','A user chooses an import source and builds a starter workspace.','Source cards appear; chosen source docks into a starter-board tile grid.','import-choice'),
 ('glass','Support Chat Escalation','A support conversation transitions into a human handover.','User bubble, assistant answer and specialist card enter in distinct timed beats.','support-escalate'),
 ('glass','Support Ticket Route','A ticket is classified and routed into the correct queue.','Issue card acquires category chips; route bridge draws and queue card receives ticket.','ticket-route'),
 ('glass','Support FAQ Expand','An FAQ accordion opens a detailed answer and useful action.','Selected row expands, answer lines reveal and next-step button appears.','faq-expand'),
 ('glass','Support Resolution Proof','A resolved ticket presents a short evidence trail.','Incident timeline, fix summary and completion badge assemble in separate panels.','resolution-proof'),
 ('mobile','Package Delivery Track','A package progresses through delivery checkpoints.','Route nodes fill, package token advances and destination card confirms delivery.','delivery-track'),
 ('mobile','Journey Booking Pass','A booking selection becomes a clean travel pass.','Trip option selection, pass card lift and boarding-code schematic reveal.','booking-pass'),
 ('mobile','Route ETA Focus','A schematic route advances while arrival information stays legible.','Moving route token, adaptive ETA counter and linked destination info card.','route-eta'),
 ('mobile','Travel Itinerary Stack','Three scheduled stops assemble into a time-ordered itinerary.','Stop cards settle, connector line draws and current destination rises into focus.','itinerary-stack'),
 ('product','Pricing Plan Selection','Three pricing plans appear and one gains a detailed feature summary.','Plan cards rise; chosen plan expands while adjacent cards hold supporting values.','pricing-select'),
 ('product','Billing Cycle Compare','A billing switch changes displayed recurring totals.','Toggle activation, aligned monthly/annual values and savings chip replacement.','billing-cycle'),
 ('product','Pricing Feature Matrix','Plan features reveal as a comparison matrix.','Feature rows draw; check cells activate by plan and chosen column becomes emphasized.','pricing-matrix'),
 ('product','Subscription Upgrade Path','A current plan upgrades to a higher-capacity plan.','Current capacity bars grow, plan bridge fills and upgraded allowance cards dock.','upgrade-path'),
 ('shop','Store Add To Cart','A chosen product docks into a shopping cart.','Hero image shrinks into cart row; quantity increases and checkout affordance activates.','add-to-cart'),
 ('shop','Store Product Quickview','A product tile expands into a detailed quickview window.','Tile expansion, contained hero reveal, specification rows and purchase button entry.','product-quickview'),
 ('shop','Store Bundle Assemble','Three complementary products assemble into a bundle.','Product cards dock into a shared bundle panel; combined total and bundle chip appear.','bundle-assemble'),
 ('shop','Store Review Highlights','A product display is joined by clearly labelled review summary cards.','Product hero entry, sample rating reveal and three attribute score bars.','review-highlights'),
 ('hardware','Design Layer Stack','A visual composition splits into named editable layers.','Layer planes separate, side layer list highlights and connector stems trace.','design-layer-stack'),
 ('hardware','Design Component Library','A UI component library builds a coherent interface.','Buttons, input and card pieces travel from library slots into a preview canvas.','component-library'),
 ('hardware','Design Inspector Focus','Selecting a layout element opens its design inspector.','Selection bounds trace, inspector properties reveal and preview geometry updates.','inspector-focus'),
 ('hardware','Design Version Timeline','A design evolves through three archived states.','Version thumbnails enter, scrubber progresses and active canvas swaps to selected state.','version-timeline'),
]

PRESETS={}
for i,(source,name,desc,mechanism,recipe) in enumerate(RECIPES):
 pid=f'PX{i+201:03d}'
 PRESETS[pid]={'name':name,'description':desc,'genre':'saas','text':name,'subtitle':desc,
  'family':'premium-ui-product','duration':6,'source_url':SOURCES[source],
  'observation_basis':'listing-description','mechanism':mechanism,'variant_basis':'adapted',
  'asset_types':['editable text','UI labels','product images','app screenshots','original vector schematics'],
  'use_cases':['SaaS demo','app promo','product feature explanation','business presentation'],
  'parameters':{'text':'Hero heading','subtitle':'Short supporting copy','labels':'List of UI labels',
   'values':'List of displayed numeric or price values','image_path':'Optional full image, safely contained',
   'image_paths':'Optional list of full product/screen images, safely contained','genre':'Atlas palette',
   'accent':'#RRGGBB accent','duration':'Output duration 0.5--120 seconds','tempo':'0.5--2 action rate'},
  'adaptation_status':'original-demo','recipe':recipe,'recipe_group':i//4,'recipe_variant':i%4,
  'perspective':'2.5D plane' if i//4 in (12,13) else '2D original geometry'}
assert len(PRESETS)==100

# Exact implementation notes override broader category inspiration. These avoid
# promising physically simulated glass/3D or transitions that the demo does not
# perform. They do not change rendered visuals.
IMPLEMENTED_MECHANISMS={
 'PX204':'Staggered source progress states, traced collection links and final output status.',
 'PX215':'Keyboard shortcut badge, selected-command focus and timed destination overlay.',
 'PX220':'Urgent top card is framed over quiet routine rows and gains a review action.',
 'PX222':'Parallel prerequisite cards connect by traced dependency stems to a central delivery slot.',
 'PX225':'Bento dashboard reveal with hero count-up, graph growth, progress and supporting status widgets.',
 'PX227':'Detail report bar heights grow beside a legible metric table and separating rule.',
 'PX228':'Large hero count-up and two supporting comparison panels enter as one hierarchy.',
 'PX230':'Product and price rows appear in staggered order beside a checkout drawer, then action becomes ready.',
 'PX232':'Offer status chip changes as a secondary price resolves beneath the original value.',
 'PX237':'Wave segments activate with an underlying progress track, elapsed counter and transport pill.',
 'PX238':'Selected playlist row receives focus and a filling progress strip beside contained artwork.',
 'PX239':'Chapter buttons change active state alongside a contained screen and continuous progress track.',
 'PX240':'Live amplitude trace and recording pulse switch to a clip-ready export action.',
 'PX241':'Week slots appear; pointer targets a highlighted slot and the booked confirmation pill activates.',
 'PX243':'Event information panel, staggered attendee arrivals and RSVP confirmation.',
 'PX248':'Format selection highlight, export progress growth and download action state.',
 'PX258':'Finish selectors activate; original schematic finish changes and selected option updates. Supplied images stay unchanged.',
 'PX267':'Original and modified code rows reveal side by side, traced stems meet at a merge-review pane.',
 'PX280':'Import-source selection highlight and timed starter-workspace tile population.',
 'PX286':'Trip option selection emphasises an adjacent travel pass with a schematic boarding code.',
 'PX293':'Contained product token moves into a cart row; quantity text appears and checkout is enabled.',
 'PX294':'Contained product image holds while detail rows fade in and the purchase action activates.',
 'PX300':'Version tiles select in sequence and the canvas adds blocks to reflect the selected design state.',
}
for _pid,_mechanism in IMPLEMENTED_MECHANISMS.items():PRESETS[_pid]['mechanism']=_mechanism

def tx(im,s,x,y,size=25,p=None,color=None,w=500,face='bold',anchor='left',opacity=1):
 p=p or PALETTES['saas']; s=str(s)
 text(im,s,x,y,fit_size(s,w,size,face),color or p['text'],face,anchor=anchor,opacity=opacity)

def lbl(cfg,defaults):
 custom=cfg.get('labels',[])
 if isinstance(custom,str):custom=[custom]
 return [str(custom[i]) if isinstance(custom,list) and i<len(custom) else value for i,value in enumerate(defaults)]

def val(cfg,i,default):
 v=cfg.get('values',[])
 return str(v[i]) if isinstance(v,list) and i<len(v) else str(default)

@lru_cache(maxsize=160)
def glass_panel(w,h,fill,border):
 """Local-size frosted panel; cached gradient and soft rim highlights."""
 w,h=int(w),int(h); out=layer(w+22,h+22)
 sh=layer(w+22,h+22);rr(sh,(11,15,w+11,h+15),(0,0,0,115),22)
 out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
 yy,xx=np.mgrid[0:h,0:w]; a=(.08+.09*np.exp(-((xx-w*.2)/(w*.85))**2-((yy-h*.08)/max(1,h))**2))[:,:,None]
 c=np.asarray(rgb(fill)); b=np.asarray(rgb(border)); data=np.uint8(c[None,None,:]*(1-a)+b[None,None,:]*a)
 body=Image.fromarray(data).convert('RGBA');mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),22,255)
 body.putalpha(mask);out.alpha_composite(body,(11,11))
 ImageDraw.Draw(out).rounded_rectangle((11,11,w+10,h+10),22,outline=rgba(border,100),width=1)
 line(out,[(32,12),(w-10,12)],rgba('#FFFFFF',52),1)
 return out

def card(im,x,y,w,h,p,head='',small='',accent=False):
 paste(im,glass_panel(round(w),round(h),p['panel'],p['secondary']),x-11,y-11,anchor='topleft')
 if accent:rr(im,(x,y,x+w,y+h),None,22,p['accent'],2)
 if head:tx(im,head,x+22,y+31,25,p,w=w-44)
 if small:tx(im,small,x+22,y+62,18,p,p['muted'],w-44,face='sans')

def pill(im,s,x,y,w,p,on=False):
 rr(im,(x,y,x+w,y+39),p['accent'] if on else p['panel'],18,p['accent'] if on else p['muted'])
 tx(im,s,x+w/2,y+19,19,p,p['bg'] if on else p['text'],w-18,anchor='center')

def progress(im,x,y,w,p,q,h=10):
 rr(im,(x,y,x+w,y+h),p['bg'],h/2)
 if q>0:rr(im,(x,y,x+max(h,w*clamp(q)),y+h),p['accent'],h/2)

def check(im,x,y,p,q=1):
 circle(im,x,y,14,p['accent'] if q>=1 else p['panel'],p['accent'],2)
 if q>=1:line(im,[(x-7,y),(x-2,y+5),(x+8,y-6)],p['bg'],3)

def cursor(im,x,y,p,label=''):
 ImageDraw.Draw(im).polygon([(x,y),(x+8,y+25),(x+14,y+17),(x+25,y+12)],fill=p['accent'],outline=p['bg'])
 if label:pill(im,label,x+16,y+22,110,p,True)

def wave(im,x,y,w,h,p,t,filled=False):
 for i in range(44):
  a=.12+.75*abs(math.sin(i*.53+t*2.4)*math.cos(i*.18-t*.7)); xx=x+i*w/44
  line(im,[(xx,y-a*h/2),(xx,y+a*h/2)],p['accent'] if not filled or i/44<prog(t,.8,3.8) else p['muted'],4)

@lru_cache(maxsize=48)
def loaded_image(path,w,h):
 try:
  src=Image.open(path).convert('RGBA'); src=ImageOps.contain(src,(int(w),int(h)),Image.Resampling.LANCZOS)
  out=layer(int(w),int(h));paste(out,src,w/2,h/2);return out
 except (OSError,ValueError,TypeError):return None

def path_for(cfg,i=0):
 paths=cfg.get('image_paths',[])
 if isinstance(paths,str):paths=[paths]
 return paths[i%len(paths)] if isinstance(paths,list) and paths else cfg.get('image_path','')

def asset(im,cfg,x,y,w,h,p,i=0,kind='product'):
 path=path_for(cfg,i); image=loaded_image(str(path),round(w),round(h)) if path else None
 if image is not None:paste(im,image,x,y,anchor='topleft');return
 # Original vector stand-ins keep the renderer useful without supplied assets.
 cx,cy=x+w/2,y+h/2
 if kind=='screen':
  margin=min(18,w*.08,h*.08)
  rr(im,(x+margin,y+margin,x+w-margin,y+h-margin),p['bg'],min(16,h*.1),p['muted'])
  rr(im,(x+margin*2,y+h*.15,x+w-margin*2,y+h*.27),p['accent'],min(9,h*.05))
  for j in range(3):
   yy=y+h*(.36+j*.18)
   rr(im,(x+margin*2,yy,x+w-margin*2,yy+h*.13),p['panel'],min(8,h*.035))
   circle(im,x+margin*2.7,yy+h*.065,min(5,h*.025),p['secondary'])
 else:
  # A watch-like product schematic, deliberately named as a schematic.
  sw,sh=min(w*.39,135),min(h*.56,170)
  rr(im,(cx-sw*.34,cy-sh*.85,cx+sw*.34,cy+sh*.85),p['muted'],15)
  rr(im,(cx-sw*.6+6,cy-sh*.54+6,cx+sw*.6+6,cy+sh*.54+6),p['bg'],25)
  rr(im,(cx-sw*.6,cy-sh*.54,cx+sw*.6,cy+sh*.54),p['secondary'],25,p['text'],2)
  rr(im,(cx-sw*.48,cy-sh*.42,cx+sw*.48,cy+sh*.42),p['bg'],17)
  circle(im,cx,cy,min(sw*.31,sh*.27),p['panel'],p['accent'],3)
  line(im,[(cx,cy-sh*.18),(cx,cy),(cx+sw*.17,cy)],p['accent'],4)
  if w>160 and h>100:tx(im,'PRODUCT SCHEMATIC',cx,y+h-14,13,p,p['muted'],w-20,'mono','center')

def title(im,cfg,p):
 tx(im,cfg.get('text',''),64,163,35,p,w=1152)
 tx(im,cfg.get('subtitle',''),64,203,19,p,p['muted'],1152,face='sans')

def trace(im,pts,q,p,width=3):
 line(im,pts,p['muted'],2)
 lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(pts,pts[1:])]
 remaining=sum(lengths)*clamp(q);active=[pts[0]]
 for a,b,le in zip(pts,pts[1:],lengths):
  if remaining>=le:active.append(b);remaining-=le
  else:active.append((mix(a[0],b[0],remaining/max(1,le)),mix(a[1],b[1],remaining/max(1,le))));break
 if len(active)>1:line(im,active,p['accent'],width)
 if q>0:circle(im,*active[-1],5,p['accent'])

def pipeline(im,t,cfg,p,v):
 labels=lbl(cfg,['SOURCE','PROCESS','REVIEW','DELIVER'])
 if v==0:
  nodes=[(80,366,labels[0]),(435,265,'RESEARCH'),(435,472,'MEDIA'),(825,366,labels[3])]
  for a,b in [(0,1),(0,2),(1,3),(2,3)]:
   xa,ya,_=nodes[a];xb,yb,_=nodes[b];trace(im,[(xa+240,ya+48),(xa+282,ya+48),(xb-35,yb+48),(xb,yb+48)],prog(t,.5+a*.35,2.2+a*.35),p)
 elif v==1:
  nodes=[(85,357,labels[0]),(460,357,'APPROVAL'),(840,357,labels[3])]
  trace(im,[(325,405),(460,405)],prog(t,.5,1.5),p)
  trace(im,[(700,405),(840,405)],prog(t,2.4,3.5),p)
  pill(im,'APPROVED' if t>2.4 else 'AWAITING REVIEW',461,499,238,p,t>2.4)
 elif v==2:
  nodes=[(85,322,labels[0]),(460,322,labels[1]),(840,322,labels[3])]
  trace(im,[(325,370),(460,370)],prog(t,.45,1.2),p)
  trace(im,[(580,418),(580,530),(725,530),(725,300),(580,300),(580,322)],prog(t,1.3,3),p)
  trace(im,[(700,370),(840,370)],prog(t,3,4),p)
  pill(im,'RETRY 01' if t<3 else 'RECOVERED',817,487,263,p,t>3)
 else:
  nodes=[(65,257,'DOCUMENT'),(65,387,'DATA'),(65,517,'MEDIA'),(470,385,'COLLECT'),(865,385,'RESULT')]
  for j in range(3):trace(im,[(305,nodes[j][1]+48),(384,nodes[j][1]+48),(384,433),(470,433)],prog(t,.5+j*.3,1.7+j*.3),p)
  trace(im,[(710,433),(865,433)],prog(t,2.3,3.4),p)
 for j,(x,y,name) in enumerate(nodes):
  yy=y+28*(1-ease(prog(t,.2+j*.13,.9+j*.13)))
  card(im,x,yy,240,96,p,name,('CONNECTED' if t>1+j*.4 else 'WAITING'),accent=t>1+j*.4)

def composer(im,t,cfg,p,v):
 if v==0:
  card(im,80,248,1120,349,p,'PROMPT WORKSPACE')
  labs=lbl(cfg,['ROLE  /  Analyst','TASK  /  Summarise the source','FORMAT  /  Three useful points'])
  for j,s in enumerate(labs):
   q=ease(prog(t,.5+j*.5,1.1+j*.5));xx=mix(95,119,q);yy=321+j*69
   rr(im,(xx,yy,xx+910*q,yy+52),p['bg'],12)
   tx(im,s,xx+19,yy+25,24,p,w=850,opacity=q)
  pill(im,'RUN PROMPT',994,526,168,p,t>2.4)
 elif v==1:
  card(im,448,255,732,320,p,'TEMPLATE')
  for j,s in enumerate(lbl(cfg,['[TOPIC]','[AUDIENCE]','[OUTPUT]'])):
   y=325+j*73;q=ease(prog(t,.55+j*.45,1.3+j*.45));xx=mix(80,480,q)
   pill(im,s,xx,y,230,p,q>=.9)
   tx(im,['Research summary','Medical students','Three key points'][j],735,y+19,24,p,w=405,opacity=q)
  tx(im,'INPUT VARIABLES',80,283,21,p,p['muted'],320)
 elif v==2:
  card(im,90,251,590,351,p,'Create a concise report','Use the attached source material')
  for j,s in enumerate(lbl(cfg,['Source A.pdf','Reference B.txt','Image C.png'])):
   q=ease(prog(t,.55+j*.45,1.3+j*.45));card(im,746+90*(1-q),283+j*97,398,78,p,s,accent=q>=.99)
  tx(im,'CONTEXT CAPACITY',123,441,20,p,p['muted'],510)
  progress(im,123,477,511,p,prog(t,.8,2.8),15)
  pill(im,'READY TO RUN',124,526,238,p,t>2.8)
 else:
  card(im,75,261,463,319,p,'ROUGH INSTRUCTION')
  tx(im,'Make a useful report.',104,351,29,p,w=405)
  tx(im,'Add context and constraints.',104,402,22,p,p['muted'],405,'sans')
  arrow(im,615,420,p['accent'],2)
  card(im,686,261,516,319,p,'STRUCTURED PROMPT')
  for j,s in enumerate(lbl(cfg,['Audience: students','Scope: key evidence','Output: 3 concise actions'])):
   q=prog(t,.6+j*.55,1.45+j*.55);tx(im,s,718,355+j*64,27,p,w=450,opacity=q)

def response(im,t,cfg,p,v):
 lines=lbl(cfg,['Start with the main finding.','Explain why it matters.','Offer a practical next step.'])
 if v==0:
  card(im,100,253,1080,346,p,'ASSISTANT RESPONSE')
  for j,s in enumerate(lines):
   n=round(len(s)*prog(t,.55+j*.75,1.5+j*.75));tx(im,s[:n],140,347+j*73,32,p,w=968)
   if .55+j*.75<t<1.5+j*.75 and int(t*5)%2==0:line(im,[(140+measure(s[:n],32),330+j*73),(140+measure(s[:n],32),360+j*73)],p['accent'],3)
  pill(im,'COMPLETE' if t>3 else 'WRITING',933,274,203,p,t>3)
 elif v==1:
  card(im,78,258,680,338,p,'ANSWER WITH EVIDENCE')
  for j,s in enumerate(lines):
   q=prog(t,.5+j*.6,1.25+j*.6);tx(im,s,108,348+j*78,27,p,w=536,opacity=q)
   pill(im,str(j+1),674,331+j*78,49,p,q>.9)
   card(im,824,294+j*97,373,78,p,f'SOURCE {j+1}',f'Reference material {j+1}',accent=q>.9)
 elif v==2:
  for j,s in enumerate(['RESEARCH','WRITING','REVIEW']):
   x=72+j*385;card(im,x,255,365,176,p,s)
   progress(im,x+23,333,319,p,prog(t,.5+j*.3,2+j*.25),13)
   tx(im,['Sources checked','Draft prepared','Clarity checked'][j],x+23,380,23,p,w=320)
   trace(im,[(x+183,431),(x+183,473),(640,473),(640,494)],prog(t,1.8,2.8),p)
  card(im,293,495,694,109,p,'CONSENSUS SUMMARY','A clear answer from coordinated steps',accent=t>2.8)
 else:
  card(im,85,250,762,122,p,'USER FOLLOW-UP','Make the next step more specific.')
  card(im,388,408,790,188,p,'REFINED ANSWER')
  for j,s in enumerate(lines):
   q=prog(t,1+j*.5,1.8+j*.5);tx(im,s,421,486+j*40,25,p,w=710,opacity=q)
  pill(im,'UPDATED',986,428,152,p,t>2.6)

def search(im,t,cfg,p,v):
 q=prog(t,.3,1.5);s=lbl(cfg,['Find useful resources','Project planning','Design assets','Research notes'])
 if v==0:
  card(im,218,247,844,90,p);tx(im,s[0][:round(len(s[0])*q)],253,289,31,p,w=744)
  for j,a in enumerate(s[1:]):
   yy=357+j*77;active=j==min(2,int(max(0,t-1.5)*1.5));rr(im,(219,yy,1061,yy+63),p['panel'],14,p['accent'] if active else p['muted'])
   tx(im,a,254,yy+31,28,p,w=734,opacity=prog(t,1+j*.25,1.6+j*.25))
 elif v==1:
  labs=lbl(cfg,['ALL','DOCUMENTS','IMAGES']);selected=t>1.5
  for j,a in enumerate(labs):pill(im,a,76+j*194,245,174,p,j==(1 if selected else 0))
  count=3 if selected else 6
  for j in range(count):
   x=76+(j%3)*385;y=322+(j//3)*145
   card(im,x,y,360,121,p,f'RESULT {j+1}',['Useful document','Reference material','Project resource'][j%3],accent=selected)
  if selected:pill(im,'3 MATCHING DOCUMENTS',428,538,425,p,True)
 elif v==2:
  ee=ease(prog(t,.25,1));card(im,244,247,792,339,p,'COMMAND PALETTE')
  for j,a in enumerate(lbl(cfg,['Open workspace','Find a file','Create project'])):
   yy=328+j*72;rr(im,(276,yy,1004,yy+57),p['bg'],12,p['accent'] if j==1 and t>1.4 else None)
   tx(im,a,298,yy+28,28,p,w=650)
  pill(im,'WORKSPACE OPEN' if t>3 else 'CTRL + K',789,264,211,p,t>3)
  if t>3:card(im,342,470,599,126,p,'PROJECT WORKSPACE','Selected command is ready',True)
 else:
  card(im,84,250,417,343,p,'MEANING SEARCH')
  tx(im,'Improve team workflow',113,353,30,p,w=358)
  tx(im,'Match concepts, not spelling',113,419,21,p,p['muted'],360,'sans')
  for j,a in enumerate(lbl(cfg,['Team coordination','Workflow planning','Shared task board'])):
   card(im,690,269+j*108,510,94,p,a)
   trace(im,[(500,416),(595,416),(595,316+j*108),(690,316+j*108)],prog(t,.5+j*.3,1.4+j*.3),p)
   progress(im,711,331+j*108,465,p,prog(t,1+j*.3,2.4+j*.3)*(.92-j*.09),8)

def notifications(im,t,cfg,p,v):
 labs=lbl(cfg,['File ready','Team update','Task completed'])
 if v==0:
  card(im,91,247,1100,350,p,'NOTIFICATION INBOX')
  for j,s in enumerate(labs):
   q=ease(prog(t,.5+j*.45,1.1+j*.45));x=mix(370,129,q);y=325+j*76
   rr(im,(x,y,x+1023,y+62),p['bg'],12);circle(im,x+26,y+31,7,p['accent'])
   tx(im,s,x+54,y+31,28,p,w=878)
  pill(im,f'{min(3,max(0,int((t-.5)/.45)+1))} UNREAD',980,263,174,p,True)
 elif v==1:
  card(im,159,295,962,239,p,'BACKGROUND UPLOAD','Working safely while you continue')
  qq=prog(t,.7,3);progress(im,195,397,716,p,qq,17)
  tx(im,f'{round(qq*100)}%',997,405,34,p,p['accent'],100,anchor='center')
  pill(im,'OPEN FILE' if qq>=1 else 'TRANSFERRING',738,451,338,p,qq>=1)
  check(im,1044,327,p,qq)
 elif v==2:
  q=ease(prog(t,1,2.2));card(im,144,248,992,95,p,'PROJECT DIGEST','3 related updates')
  for j,s in enumerate(labs):
   yy=mix(348+j*78,359+j*70,q);xx=mix(82,178,q)
   card(im,xx,yy,924,60,p,s,accent=t>2.2)
  pill(im,'GROUPED',948,270,152,p,t>2.2)
 else:
  q=ease(prog(t,.8,2));card(im,98,271,1062,124,p,'ACTION REQUIRED','A priority item needs your review',True)
  for j,s in enumerate(labs):
   y=425+j*60;rr(im,(147,y,1139,y+46),p['panel'],12)
   tx(im,s,171,y+23,23,p,p['muted'],893)
  pill(im,'REVIEW NOW',837,320,276,p,q>.9)

def kanban(im,t,cfg,p,v):
 labs=lbl(cfg,['PLANNED','ACTIVE','COMPLETE']);xs=[77,480,883]
 for j,s in enumerate(labs):card(im,xs[j],248,325,343,p,s)
 if v==0:
  q=ease(prog(t,.7,2));r=ease(prog(t,2.3,3.5));x=mix(mix(101,504,q),907,r);y=337-45*math.sin(q*math.pi)+20*math.sin(r*math.pi)
  card(im,x,y,277,114,p,'Feature task','Design + implement',True);cursor(im,x+219,y+85,p)
  if r>=1:pill(im,'DONE',935,482,213,p,True)
 elif v==1:
  for j,s in enumerate(['Design ready','Review ready']):
   q=ease(prog(t,.5+j*.35,1.6+j*.35));card(im,103,325+j*135,275,108,p,s,accent=q>=1)
   trace(im,[(378,379+j*135),(438,379+j*135),(438,414),(504,414)],prog(t,1.4,2.5),p)
  card(im,504,362,277,110,p,'DELIVERY','Dependencies met',t>2.5)
  trace(im,[(781,414),(907,414)],prog(t,2.5,3.5),p)
  card(im,907,362,277,110,p,'RELEASE','Ready to publish',t>3.5)
 elif v==2:
  q=ease(prog(t,.8,2.6));x=mix(102,504,q)
  card(im,x,350,277,140,p,'Assigned task','Owner: Team member',q>.9)
  circle(im,mix(1090,x+51,q),mix(523,442,q),21,p['secondary'])
  tx(im,'A',mix(1090,x+51,q),mix(523,442,q),24,p,p['bg'],40,anchor='center')
  if q>=1:pill(im,'IN PROGRESS',917,483,250,p,True)
 else:
  q=ease(prog(t,1,2.5));card(im,105,350,276,111,p,'PARENT TASK','Feature delivered',True)
  for j,s in enumerate(['Review release','Publish update']):
   x=mix(503,905,q) if j else 504;y=323+j*156
   card(im,x,y,277,112,p,s,'Child work item',q>.9)
   trace(im,[(381,406),(440,406),(440,y+56),(x,y+56)],prog(t,.8,2.5),p)

def dashboard(im,t,cfg,p,v):
 q=prog(t,.5,3)
 if v==0:
  card(im,73,252,348,157,p,'TOTAL ACTIVITY');tx(im,f'{round(q*1248):,}',97,350,46,p,p['accent'],290)
  card(im,450,252,750,157,p,'PERFORMANCE')
  trace(im,[(481+i*72,375-(15+29*math.sin(i*.7)+i*6)*q) for i in range(10)],1,p)
  card(im,73,438,702,159,p,'PROJECT PROGRESS');progress(im,99,523,647,p,q*.82,16)
  card(im,805,438,395,159,p,'TEAM STATUS');tx(im,'12 ACTIVE',831,533,34,p,p['accent'],340)
 elif v==1:
  card(im,79,250,746,345,p,'LIVE SYSTEM MONITOR')
  pts=[(111+i*11,426+math.sin(i*.8+t*2)*19+(math.sin(i*.28+t)>0.91)*-58) for i in range(61)]
  trace(im,pts,1,p,4);tx(im,f'{round(72+9*math.sin(t))} ms',116,533,42,p,p['accent'],640)
  for j,s in enumerate(lbl(cfg,['Connection ready','Worker active','Result received'])):
   card(im,857,274+j*104,342,87,p,s,f'SYSTEM EVENT 0{j+1}',t>.8+j*.55)
 elif v==2:
  q=ease(prog(t,.8,2.4));card(im,83,253,1114,341,p,'DETAIL REPORT')
  for j in range(5):
   xx=125+j*100;hh=(45+j*27)*q;rr(im,(xx,528-hh,xx+66,528),p['accent'] if j==3 else p['secondary'],7)
  for j,s in enumerate(lbl(cfg,['Top channel','Conversion','Engagement'])):
   tx(im,s,735,335+j*69,26,p,w=315);tx(im,[val(cfg,0,'62%'),val(cfg,1,'24%'),val(cfg,2,'14%')][j],1124,335+j*69,26,p,p['accent'],120,anchor='right')
  line(im,[(698,304),(698,553)],p['muted'],1)
 else:
  card(im,97,266,585,314,p,'PRIMARY METRIC');tx(im,val(cfg,0,f'{round(q*98)}%'),137,414,82,p,p['accent'],490)
  tx(im,'Progress toward the current target',138,517,24,p,p['muted'],495,'sans')
  card(im,725,266,451,145,p,'PREVIOUS PERIOD');tx(im,val(cfg,1,'84%'),753,361,44,p,w=390)
  card(im,725,436,451,145,p,'CHANGE');tx(im,val(cfg,2,'+14 POINTS'),753,530,39,p,p['accent'],390)

def checkout(im,t,cfg,p,v):
 if v==0:
  labs=lbl(cfg,['DETAILS','PAYMENT','CONFIRMED'])
  for j,s in enumerate(labs):
   x=184+j*450;check(im,x,274,p,prog(t,.5+j*.75,1.2+j*.75));tx(im,s,x+29,274,23,p,w=305)
   if j<2:trace(im,[(x+280,274),(x+420,274)],prog(t,.75+j*.7,1.5+j*.7),p)
  card(im,143,333,994,250,p,'CHECKOUT DETAILS')
  for j,s in enumerate(['Contact confirmed','Payment method ready','Order confirmation']):
   tx(im,s,180,416+j*62,29,p,w=809);check(im,1078,416+j*62,p,prog(t,.7+j*.8,1.3+j*.8))
 elif v==1:
  card(im,80,253,495,342,p,'PRODUCTS');card(im,637,253,563,342,p,'ORDER SUMMARY')
  for j,s in enumerate(lbl(cfg,['Main product','Accessory'])):
   yy=340+j*115;asset(im,cfg,104,yy-31,109,84,p,j)
   tx(im,s,227,yy,26,p,w=320)
   q=ease(prog(t,.7+j*.6,1.8+j*.6));tx(im,s,675,yy,26,p,w=292,opacity=q);tx(im,val(cfg,j,'RM 50'),1159,yy,25,p,p['accent'],149,anchor='right',opacity=q)
  pill(im,'CHECKOUT',818,524,334,p,t>2.5)
 elif v==2:
  card(im,162,250,956,348,p,'INVOICE  /  SAMPLE')
  for j,s in enumerate(lbl(cfg,['Product line','Service line','TOTAL'])):
   yy=343+j*74;tx(im,s,202,yy,29,p,w=673);tx(im,val(cfg,j,['RM 50','RM 20','RM 70'][j]),1082,yy,29,p,p['accent'],230,anchor='right',opacity=prog(t,.5+j*.5,1.2+j*.5))
  if t>2.7:pill(im,'PAID',855,527,224,p,True)
 else:
  card(im,95,252,1090,344,p,'APPLY OFFER')
  asset(im,cfg,135,307,286,230,p)
  tx(im,'PRODUCT PRICE',489,335,23,p,p['muted'],637)
  tx(im,val(cfg,0,'RM 100'),489,386,48,p,w=630)
  q=prog(t,1.5,3);tx(im,val(cfg,1,'RM 80'),489,469,59,p,p['accent'],640,opacity=q)
  pill(im,'COUPON APPLIED' if q>=1 else 'DEMO COUPON',773,531,356,p,q>=1)

def controls(im,t,cfg,p,v):
 if v==0:
  card(im,151,248,979,352,p,'FEATURE SETTINGS')
  for j,s in enumerate(lbl(cfg,['Notifications','Cloud sync','Auto save'])):
   yy=339+j*85;tx(im,s,187,yy,30,p,w=650);q=ease(prog(t,.55+j*.65,1.3+j*.65))
   rr(im,(973,yy-20,1088,yy+20),p['accent'] if q>.5 else p['bg'],20,p['muted']);circle(im,mix(996,1065,q),yy,15,p['text'])
 elif v==1:
  card(im,81,249,634,350,p,'VISUAL CONTROLS');card(im,753,249,443,350,p,'LIVE PREVIEW')
  qs=[prog(t,.55,2.3)*.76,prog(t,.8,2.6)*.48,prog(t,1.1,2.9)*.91]
  for j,s in enumerate(lbl(cfg,['Size','Roundness','Intensity'])):
   yy=328+j*88;tx(im,s,110,yy,24,p,w=530);progress(im,111,yy+27,541,p,qs[j],9);circle(im,111+541*qs[j],yy+31,11,p['text'],p['accent'],2)
  zz=80+100*qs[0];rr(im,(974-zz,429-zz*.65,974+zz,429+zz*.65),p['accent'],10+qs[1]*45)
 elif v==2:
  q=ease(prog(t,.75,3.2));card(im,147,252,986,342,p,'THEME PREVIEW')
  preview=layer(910,235);rr(preview,(0,0,910,235),'#EEF2FA',18)
  tx(preview,'LIGHT MODE',25,38,27,p,'#24324A',390)
  for j in range(3):rr(preview,(25+j*295,83,290+j*295,208),'#D5DEEE',15)
  dark=layer(910,235);rr(dark,(0,0,910,235),p['bg'],18);tx(dark,'DARK MODE',25,38,27,p,w=390)
  for j in range(3):rr(dark,(25+j*295,83,290+j*295,208),p['panel'],15,p['accent'])
  width=round(910*q)
  if width:preview.alpha_composite(dark.crop((0,0,width,235)),(0,0))
  paste(im,preview,185,323,anchor='topleft');line(im,[(185+width,331),(185+width,550)],p['accent'],4)
 elif v==3:
  card(im,104,249,1066,351,p,'ACCESS PERMISSIONS')
  for j,s in enumerate(lbl(cfg,['VIEWER','EDITOR','ADMIN'])):tx(im,s,555+j*229,320,25,p,w=210,anchor='center')
  for row,s in enumerate(['Read files','Edit content','Manage team']):
   tx(im,s,137,401+row*76,27,p,w=345)
   for col in range(3):check(im,555+col*229,401+row*76,p,1 if col>=row and t>.6+col*.65+row*.12 else 0)

def player(im,t,cfg,p,v):
 if v==0:
  card(im,115,253,1050,343,p,'AUDIO PLAYER')
  wave(im,152,398,970,104,p,t,True);progress(im,154,484,965,p,prog(t,.7,3.9),9)
  pill(im,'PAUSE',533,528,211,p,True);tx(im,f'00:{int(max(0,t-.7)*14):02d}',155,546,25,p,p['muted'],200,'mono')
 elif v==1:
  card(im,78,251,416,348,p,'NOW PLAYING');asset(im,cfg,121,321,329,191,p,kind='screen')
  idx=min(2,max(0,int((t-.6)/1.15)))
  for j,s in enumerate(lbl(cfg,['Track one','Track two','Track three'])):
   card(im,540,277+j*107,663,88,p,s,'Playlist item',j==idx)
   if j==idx:progress(im,566,338+j*107,610,p,(t-.6-j*1.15)/1.15,7)
 elif v==2:
  card(im,86,248,1109,350,p,'VIDEO CHAPTERS');asset(im,cfg,120,317,508,244,p,kind='screen')
  idx=min(2,max(0,int((t-.5)/1.2)))
  for j,s in enumerate(lbl(cfg,['Introduction','Main idea','Next action'])):pill(im,s,683,327+j*73,461,p,j==idx)
  progress(im,684,566,461,p,prog(t,.5,4),10)
 else:
  card(im,156,267,968,304,p,'VOICE RECORDER')
  circle(im,829,300,9,p['accent'] if int(t*3)%2 else p['muted']);tx(im,'RECORDING' if t<3.5 else 'CLIP READY',850,300,21,p,w=237)
  wave(im,195,412,885,97,p,t)
  pill(im,'EXPORT CLIP' if t>3.5 else f'00:{int(t*8):02d}',745,504,334,p,t>3.5)

def calendar(im,t,cfg,p,v):
 if v==0:
  card(im,89,249,1105,348,p,'BOOK A TIME')
  for j,s in enumerate(lbl(cfg,['MON','TUE','WED','THU','FRI'])):
   x=119+j*213;tx(im,s,x+90,323,23,p,w=180,anchor='center')
   for k in range(3):rr(im,(x,361+k*68,x+183,408+k*68),p['bg'],10,p['accent'] if j==2 and k==1 and t>1.5 else p['muted'])
  if t>2.5:pill(im,'BOOKED  /  WED 11:00',777,537,372,p,True)
  cursor(im,mix(1100,627,ease(prog(t,.65,2))),mix(555,450,ease(prog(t,.65,2))),p)
 elif v==1:
  card(im,89,255,1105,331,p,'DAILY SCHEDULE')
  for j in range(6):
   x=124+j*198;line(im,[(x,353),(x,556)],p['muted'],1);tx(im,f'{9+j}:00',x,318,21,p,p['muted'],150)
  for j,s in enumerate(lbl(cfg,['Plan','Build','Review'])):
   x=126+j*310;w=254*ease(prog(t,.5+j*.4,1.6+j*.4));rr(im,(x,373+j*56,x+max(1,w),417+j*56),p['accent'] if j==1 else p['secondary'],10)
   tx(im,s,x+17,395+j*56,24,p,p['bg'],220,opacity=prog(t,.8+j*.4,1.7+j*.4))
  xx=126+990*prog(t,.8,4);line(im,[(xx,345),(xx,552)],p['text'],2)
 elif v==2:
  card(im,242,249,797,348,p,'PROJECT SESSION','Wednesday  /  11:00')
  for j in range(4):
   q=ease(prog(t,.7+j*.3,1.5+j*.3));circle(im,337+j*186,419+18*(1-q),37,p['secondary'],p['accent'] if q>=1 else None,2)
   tx(im,chr(65+j),337+j*186,419,31,p,p['bg'],70,anchor='center',opacity=q)
  pill(im,'RSVP CONFIRMED' if t>2.7 else 'JOIN SESSION',460,512,361,p,t>2.7)
 else:
  card(im,255,247,770,354,p,'DATE RANGE')
  q=prog(t,.6,3.2);last=7+round(10*q)
  for j in range(21):
   x=294+(j%7)*102;y=327+(j//7)*71;selected=7<=j<=last
   rr(im,(x,y,x+73,y+49),p['accent'] if selected else p['bg'],10)
   tx(im,j+1,x+36,y+25,25,p,p['bg'] if selected else p['text'],65,anchor='center')
  tx(im,f'8 -- {last+1}  /  SELECTED RANGE',295,568,23,p,p['accent'],680)

def uploads(im,t,cfg,p,v):
 if v==0:
  card(im,82,254,1118,341,p,'UPLOAD SOURCE')
  for j in range(15):
   xx=561+j*39;line(im,[(xx,332),(xx+21,332)],p['muted'],2);line(im,[(xx,548),(xx+21,548)],p['muted'],2)
  line(im,[(561,332),(561,548)],p['muted'],2);line(im,[(1140,332),(1140,548)],p['muted'],2)
  q=ease(prog(t,.6,2.5));xx=mix(140,772,q);yy=mix(378,382,q)-40*math.sin(q*math.pi)
  card(im,xx,yy,260,101,p,'Source.pdf','DOCUMENT',q>.9);cursor(im,xx+215,yy+73,p)
  if q>=1:pill(im,'ATTACHED',799,523,296,p,True)
 elif v==1:
  card(im,121,251,1037,350,p,'TRANSFER QUEUE')
  for j,s in enumerate(lbl(cfg,['Report.pdf','Images.zip','Notes.txt'])):
   y=333+j*82;q=prog(t,.5+j*.5,2.5+j*.4);tx(im,s,155,y,25,p,w=650)
   progress(im,154,y+27,840,p,q,10);check(im,1082,y+12,p,q)
 elif v==2:
  card(im,74,251,489,348,p,'LOCAL FILES');card(im,720,251,489,348,p,'CLOUD FILES')
  for j,s in enumerate(lbl(cfg,['Project A','Reference B','Assets C'])):
   y=345+j*77;tx(im,s,104,y,26,p,w=425);tx(im,s,754,y,26,p,w=425)
   trace(im,[(564,y),(720,y)],prog(t,.6+j*.6,1.7+j*.6),p)
  pill(im,'IN SYNC',492,546,296,p,t>3)
 else:
  card(im,117,250,1046,350,p,'EXPORT DESIGN')
  for j,s in enumerate(lbl(cfg,['PNG','PDF','MP4'])):pill(im,s,157+j*330,342,286,p,j==2 and t>1)
  q=prog(t,1.3,3.6);progress(im,157,439,953,p,q,15)
  tx(im,'CHOOSE A FORMAT' if t<1.3 else 'GENERATING EXPORT',158,492,26,p,w=590)
  pill(im,'DOWNLOAD' if q>=1 else f'{round(q*100)}%',794,514,315,p,q>=1)

def handset(cfg,p,w=237,h=354,i=0,t=0,scroll=False):
 out=layer(w,h);rr(out,(0,0,w-1,h-1),p['secondary'],30,p['text'],2)
 rr(out,(7,7,w-8,h-8),p['bg'],25)
 screen=layer(w-26,h-45)
 if path_for(cfg,i):asset(screen,cfg,0,0,screen.width,screen.height,p,i,'screen')
 else:
  rr(screen,(0,0,screen.width,screen.height),p['panel'],15)
  tx(screen,'YOUR APP',18,35,21,p,w=screen.width-35)
  if scroll:
   travel=round(65*prog(t,.7,3.6))
   content=layer(screen.width,470)
   for j in range(5):
    yy=64+j*82;rr(content,(13,yy,screen.width-13,yy+65),p['bg'],11,p['accent'] if j==2 else None)
    tx(content,f'Feature {j+1}',24,yy+22,20,p,w=screen.width-46)
    progress(content,24,yy+44,screen.width-50,p,.35+j*.12,6)
   screen.alpha_composite(content.crop((0,travel,screen.width,travel+screen.height)))
  else:
   for j,s in enumerate(['Overview','Activity','Next step']):
    yy=73+j*76;rr(screen,(14,yy,screen.width-14,yy+61),p['bg'],10)
    tx(screen,s,24,yy+22,19,p,w=screen.width-48)
    progress(screen,24,yy+43,screen.width-47,p,prog(t,.5+j*.35,2+j*.35)*(.8-j*.12),6)
 paste(out,screen,13,31,anchor='topleft')
 rr(out,(w*.32,12,w*.68,22),p['bg'],8);line(out,[(w*.36,h-11),(w*.64,h-11)],p['text'],3)
 return out

def phone_plane(im,cfg,x,y,w,h,p,t=0,i=0,tilt=0,scroll=False):
 source=handset(cfg,p,w,h,i,t,scroll)
 if not tilt:paste(im,source,x,y,anchor='topleft');return
 pad=32;delta=24*tilt;quad=[(pad,15+max(0,delta)),(w+pad,15+max(0,-delta)),(w+pad-abs(delta)*.22,h+15-max(0,-delta)),(pad+abs(delta)*.22,h+15-max(0,delta))]
 warped=warp_quad(source,quad,(w+pad*2,h+30))
 paste(im,warped,x-pad,y-15,anchor='topleft')

def phones(im,t,cfg,p,v):
 if v==0:
  tilt=math.sin(t*.8)*.9;phone_plane(im,cfg,528,244,226,362,p,t,tilt=tilt)
  for j,s in enumerate(lbl(cfg,['CLEAR INTERFACE','SMOOTH FLOW','USEFUL FEATURES'])):
   x=94 if j!=1 else 828;y=279+j*102
   card(im,x,y,352,90,p,s,accent=t>1+j*.4)
   trace(im,[(x+352 if x<500 else x,y+46),(507 if x<500 else 776,y+46),(528 if x<500 else 754,421)],prog(t,.6+j*.35,1.4+j*.35),p)
 elif v==1:
  phone_plane(im,cfg,514,241,236,368,p,t)
  locations=[(79,275),(828,272),(828,467)]
  for j,s in enumerate(lbl(cfg,['OVERVIEW','ACTIVITY','ACTION'])):
   q=ease(prog(t,.7+j*.4,1.7+j*.4));xx=mix(525,locations[j][0],q);yy=mix(300+j*72,locations[j][1],q)
   card(im,xx,yy,356,118,p,s,'App feature',True)
   if q>=1:trace(im,[(xx+356 if xx<500 else xx,yy+58),(510 if xx<500 else 762,340+j*74)],1,p)
 elif v==2:
  phone_plane(im,cfg,177,244,230,361,p,t,i=0,tilt=-.45)
  phone_plane(im,cfg,878,244,230,361,p,t,i=1,tilt=.45)
  trace(im,[(408,413),(878,413)],prog(t,.8,2.8),p,4)
  q=ease(prog(t,.8,2.8));pill(im,'CONTENT',mix(421,737,q),366,142,p,True)
  if q>=1:pill(im,'RECEIVED',902,540,179,p,True)
 else:
  phone_plane(im,cfg,229,242,239,369,p,t,scroll=True)
  card(im,608,305,553,225,p,'FEATURE 3','Selected from the scrolling interface',True)
  asset(im,cfg,647,399,464,91,p,kind='screen')
  trace(im,[(469,421),(543,421),(543,413),(608,413)],prog(t,.7,2),p)

def browser(cfg,p,w,h,t=0,i=0,title_text='WORKSPACE'):
 out=layer(w,h);rr(out,(0,0,w-1,h-1),p['secondary'],18)
 rr(out,(5,5,w-6,h-6),p['bg'],14)
 for j in range(3):circle(out,18+j*16,20,4,p['muted'])
 tx(out,title_text,78,21,15,p,p['muted'],w-104,'mono')
 asset(out,cfg,18,44,w-36,h-63,p,i,'screen')
 return out

def devices(im,t,cfg,p,v):
 if v==0:
  q=ease(prog(t,.4,1.5));desktop=browser(cfg,p,609,293,t)
  paste(im,desktop,80,258+24*(1-q),anchor='topleft');rr(im,(350,553,419,580),p['secondary'],4)
  line(im,[(259,582),(509,582)],p['muted'],7)
  tablet=browser(cfg,p,357,264,t,1,'TABLET');paste(im,tablet,715,326+22*(1-prog(t,.7,1.7)),anchor='topleft')
  phone_plane(im,cfg,1096,274,119,296,p,t,2)
 elif v==1:
  paste(im,browser(cfg,p,701,335,t),78,255,anchor='topleft')
  phone_plane(im,cfg,963,244,232,365,p,t,1)
  q=ease(prog(t,.8,2.8));xx=mix(601,847,q);yy=381-49*math.sin(q*math.pi)
  token=layer(112,113);rr(token,(0,0,112,113),p['panel'],14,p['accent']);asset(token,cfg,4,4,104,105,p,0)
  paste(im,token,xx,yy,anchor='topleft');trace(im,[(779,431),(963,431)],q,p)
  if q>=1:pill(im,'CONTINUE ON MOBILE',949,571,258,p,True)
 elif v==2:
  for j in range(3):
   q=ease(prog(t,.35+j*.3,1.2+j*.3));xx=120+j*81+100*(1-q);yy=253+j*36
   b=browser(cfg,p,934,266,t,j,['HOME','FEATURES','YOUR PRODUCT'][j]);paste(im,b,xx,yy,anchor='topleft')
  pill(im,'FEATURE DETAILS',836,542,315,p,t>2)
 else:
  card(im,93,252,1091,349,p,'TABLET WORKSPACE')
  q=ease(prog(t,.7,2.8));split=421+154*q
  rr(im,(124,323,split,565),p['bg'],12);rr(im,(split+22,323,1152,565),p['bg'],12)
  tx(im,'PROJECT',150,359,26,p,w=split-173)
  for j,s in enumerate(['Brief','Assets','Tasks']):tx(im,s,150,419+j*48,23,p,p['muted'],split-175)
  tx(im,'LIVE PREVIEW',split+48,359,26,p,w=1091-split)
  asset(im,cfg,split+48,398,1056-split,147,p,kind='screen')

def products(im,t,cfg,p,v):
 if v==0:
  card(im,407,249,465,350,p);asset(im,cfg,459,280,365,282,p)
  positions=[(76,269),(938,295),(936,488)]
  for j,s in enumerate(lbl(cfg,['REFINED DESIGN','CLEAR DISPLAY','USEFUL FEATURES'])):
   x,y=positions[j];card(im,x,y,270,89,p,s,f'Feature 0{j+1}')
   trace(im,[(x+270 if x<400 else x,y+45),(392 if x<400 else 886,y+45),(485 if x<400 else 806,352+j*70)],prog(t,.5+j*.4,1.5+j*.4),p)
 elif v==1:
  card(im,87,250,612,349,p,'CHOOSE A FINISH');q=prog(t,.6,3.6);idx=min(2,int(q*3));pp=dict(p);pp['secondary']=[p['secondary'],p['accent'],p['muted']][idx]
  asset(im,cfg,224,313,337,241,pp)
  card(im,764,250,431,349,p,'FINISH OPTIONS')
  for j,s in enumerate(lbl(cfg,['Pearl','Mint','Slate'])):pill(im,s,800,340+j*72,358,p,j==idx)
 elif v==2:
  q=ease(prog(t,.65,2.8));layers=[('DISPLAY',p['accent']),('PROCESSOR',p['secondary']),('HOUSING',p['muted'])]
  for j,(s,c) in enumerate(layers):
   yy=421+(j-1)*100*q
   ImageDraw.Draw(im).polygon([(221,yy),(415,yy-47),(602,yy),(407,yy+49)],fill=c,outline=p['text'])
   line(im,[(407,yy+50),(407,yy+67)],p['muted'],2)
   card(im,746,276+j*109,445,85,p,lbl(cfg,['DISPLAY','PROCESSOR','HOUSING'])[j],f'Original schematic layer {j+1}')
   trace(im,[(604,yy),(688,yy),(688,319+j*109),(746,319+j*109)],q,p)
 elif v==3:
  card(im,87,251,611,346,p,'COMPLETE PRODUCT');asset(im,cfg,198,311,389,250,p)
  q=prog(t,.8,3.8);xx=332+75*math.sin(q*math.pi);yy=393+45*math.cos(q*math.pi)
  rr(im,(xx-66,yy-50,xx+66,yy+50),None,12,p['accent'],3)
  trace(im,[(xx+66,yy),(734,yy),(734,418),(781,418)],1,p)
  card(im,781,297,412,239,p,'FEATURE INSPECTION','Track a feature without cropping the original',True)
  tx(im,'FOCUS REGION',811,453,27,p,p['accent'],350)

def galleries(im,t,cfg,p,v):
 if v==0:
  idx=min(2,max(0,int((t-.6)/1.1)));card(im,96,246,1088,245,p)
  asset(im,cfg,120,259,1040,214,p,idx)
  for j in range(3):
   xx=289+j*250;card(im,xx,514,208,95,p,accent=j==idx);asset(im,cfg,xx+12,526,184,70,p,j)
 elif v==1:
  q=ease(prog(t,1,2.7));boxes=[(79,248,469,343),(577,248,302,152),(907,248,302,152),(577,429,632,162)]
  for j,(x,y,w,h) in enumerate(boxes):
   if j==0:w=mix(w,653,q)
   elif j in (1,2):x+=(155 if j==1 else 68)*q;w-=78*q
   else:x+=155*q;w-=155*q
   card(im,x,y,w,h,p,accent=j==0 and q>.5);asset(im,cfg,x+12,y+12,w-24,h-24,p,j)
 elif v==2:
  card(im,123,249,1034,348,p)
  left=layer(976,263);right=layer(976,263);asset(left,cfg,0,0,976,263,p,0);pp=dict(p);pp['secondary']=p['accent'];asset(right,cfg,0,0,976,263,pp,1)
  q=.25+.5*(.5+.5*math.sin((t-.5)*1.1));cut=round(976*q);left.alpha_composite(right.crop((0,0,cut,263)),(0,0))
  paste(im,left,152,318,anchor='topleft');line(im,[(152+cut,314),(152+cut,573)],p['accent'],4);circle(im,152+cut,444,16,p['accent'])
  pill(im,'OPTION A',154,266,231,p,True);pill(im,'OPTION B',898,266,230,p)
 else:
  q=ease(prog(t,.5,2.2));locs=[(76,321,328,251),(436,256,407,339),(874,321,328,251)]
  for j,(xx,yy,ww,hh) in enumerate(locs):
   x=mix(486,xx,q);y=mix(311,yy,q);card(im,x,y,ww,hh,p,accent=j==1);asset(im,cfg,x+15,y+15,ww-30,hh-64,p,j)
   tx(im,lbl(cfg,['COLLECTION 01','HERO PRODUCT','COLLECTION 03'])[j],x+20,y+hh-27,22,p,w=ww-40)

def code(im,t,cfg,p,v):
 if v==0:
  card(im,106,252,1065,345,p,'BUILD CONSOLE')
  command='> build project --release';n=round(len(command)*prog(t,.4,1.2));tx(im,command[:n],139,338,29,p,p['accent'],978,'mono')
  for j,s in enumerate(lbl(cfg,['Checking dependencies...','Compiling interface...','Build completed successfully.'])):
   tx(im,s,140,409+j*57,24,p,p['text'] if j<2 else p['accent'],970,'mono',opacity=prog(t,1+j*.65,1.6+j*.65))
 elif v==1:
  for j,s in enumerate(lbl(cfg,['TEST','PACKAGE','DEPLOY'])):
   x=91+j*405;card(im,x,309,285,235,p,s)
   q=prog(t,.5+j*.65,1.6+j*.65);progress(im,x+23,408,240,p,q,15)
   check(im,x+143,477,p,q)
   if j<2:trace(im,[(x+285,429),(x+405,429)],prog(t,1.2+j*.65,2+j*.65),p)
  pill(im,'RELEASE READY',442,565,394,p,t>3.2)
 elif v==2:
  for j,head in enumerate(['ORIGINAL','MODIFIED']):
   x=77+j*604;card(im,x,253,522,246,p,head)
   for k,s in enumerate(['let status = ready;','renderInterface();','saveResult();']):
    color=p['accent'] if j==1 and k==1 else p['muted'];tx(im,s,x+25,338+k*55,22,p,color,475,'mono',opacity=prog(t,.5+j*.3+k*.25,1.3+j*.3+k*.25))
  card(im,266,532,747,78,p,'MERGE APPROVED',accent=t>2.7)
  trace(im,[(338,499),(338,522),(640,522),(640,532)],prog(t,1.8,2.7),p);trace(im,[(942,499),(942,522),(640,522)],prog(t,1.8,2.7),p)
 else:
  card(im,83,282,409,266,p,'REQUEST')
  tx(im,'GET /resources',113,371,29,p,p['accent'],350,'mono')
  tx(im,'Accept: JSON',114,427,25,p,p['muted'],350,'mono')
  card(im,767,282,430,266,p,'RESPONSE')
  for j,s in enumerate(['status: 200','result: ready','items: 3']):tx(im,s,801,369+j*50,26,p,p['accent'],350,'mono',opacity=prog(t,1.8+j*.25,2.5+j*.25))
  trace(im,[(492,368),(767,368)],prog(t,.55,1.8),p)
  trace(im,[(767,461),(492,461)],prog(t,2,3.3),p)

def lock_icon(im,x,y,p,q=0):
 rr(im,(x-52,y-13,x+52,y+66),p['secondary'],17,p['text'],2)
 d=ImageDraw.Draw(im);d.arc((x-31,y-66-34*q,x+31,y+1-34*q),180,359,fill=p['accent'],width=8)
 circle(im,x,y+16,9,p['bg']);line(im,[(x,y+19),(x,y+41)],p['bg'],6)

def security(im,t,cfg,p,v):
 if v==0:
  card(im,89,251,611,346,p,'SECURE LOGIN')
  for j,s in enumerate(lbl(cfg,['Email verified','Access confirmed'])):
   yy=342+j*86;rr(im,(123,yy,662,yy+62),p['bg'],12);tx(im,s,143,yy+31,27,p,w=455);check(im,627,yy+31,p,prog(t,.5+j*.85,1.3+j*.85))
  card(im,761,251,434,346,p,'PROTECTED SESSION')
  lock_icon(im,976,418,p,ease(prog(t,2,3.3)))
  pill(im,'UNLOCKED' if t>3.3 else 'VALIDATING',791,524,374,p,t>3.3)
 elif v==1:
  card(im,106,253,479,342,p,'NEW DEVICE');phone_plane(im,cfg,291,329,108,220,p,t)
  card(im,698,253,479,342,p,'VERIFY SESSION')
  for j in range(4):
   x=738+j*102;rr(im,(x,359,x+79,432),p['bg'],11,p['accent']);tx(im,str(j+3) if t>.5+j*.5 else '-',x+40,394,35,p,w=65,anchor='center')
  trace(im,[(585,439),(698,439)],prog(t,2.3,3.3),p)
  pill(im,'TRUSTED',738,511,387,p,t>3.3)
 elif v==2:
  q=prog(t,.5,3.2);d=ImageDraw.Draw(im);d.polygon([(166,291),(396,291),(459,357),(414,486),(281,579),(150,486),(105,357)],fill=p['panel'],outline=p['accent'])
  line(im,[(133,314+232*q),(430,314+232*q)],p['accent'],5)
  for j,s in enumerate(lbl(cfg,['Account integrity','Device access','Data permissions'])):
   card(im,577,273+j*106,620,88,p,s);check(im,1156,317+j*106,p,prog(t,.65+j*.7,1.45+j*.7))
 elif v==3:
  card(im,111,262,394,325,p,'PASSKEY')
  for j in range(4):ImageDraw.Draw(im).arc((232-j*15,359-j*15,385+j*15,512+j*15),200,200+min(330,round(prog(t,.5,2.5)*330)),fill=p['accent'],width=3)
  card(im,768,262,394,325,p,'SESSION')
  lock_icon(im,963,435,p,ease(prog(t,2.4,3.5)))
  trace(im,[(505,425),(768,425)],prog(t,1.6,3),p)
  tx(im,'CONNECTED' if t>3 else 'PAIRING',803,536,28,p,p['accent'],320)

def team(im,t,cfg,p,v):
 if v==0:
  card(im,102,251,1075,348,p,'SHARED WORKSPACE')
  for j in range(3):
   xx=144+j*337;rr(im,(xx,339,xx+295,541),p['bg'],14,p['accent'] if t>.8+j*.4 else None)
   tx(im,lbl(cfg,['Plan','Design','Review'])[j],xx+20,374,27,p,w=250)
   q=ease(prog(t,.5+j*.3,2+j*.3));cursor(im,mix(1180,xx+140,q),mix(540,441,q),p,['Alya','Ben','Chen'][j])
 elif v==1:
  card(im,91,252,463,343,p,'DESIGN REVIEW');asset(im,cfg,123,334,398,229,p,kind='screen')
  circle(im,439,395,16,p['accent']);tx(im,'1',439,395,21,p,p['bg'],30,anchor='center')
  for j,s in enumerate(lbl(cfg,['Check this section.','Updated for clarity.','Looks good to go.'])):
   yy=259+j*107;q=ease(prog(t,.5+j*.65,1.3+j*.65));card(im,646+60*(1-q),yy,548,87,p,s,f'TEAM COMMENT 0{j+1}')
  pill(im,'RESOLVED',848,567,305,p,t>3.3)
 elif v==2:
  card(im,92,250,1101,351,p,'TEAM PRESENCE')
  for j,s in enumerate(lbl(cfg,['DESIGN','CONTENT','REVIEW','RELEASE'])):
   q=ease(prog(t,.5+j*.35,1.3+j*.35));xx=223+j*281
   circle(im,xx,361+30*(1-q),40,p['secondary']);tx(im,chr(65+j),xx,361,32,p,p['bg'],70,anchor='center',opacity=q)
   circle(im,xx+31,387,8,p['accent']);tx(im,s,xx,440,25,p,w=239,anchor='center')
   pill(im,'ONLINE',xx-95,489,190,p,q>=1)
 else:
  card(im,107,285,366,262,p,'CREATOR');circle(im,290,389,38,p['secondary']);tx(im,'A',290,389,31,p,p['bg'],70,anchor='center')
  card(im,807,285,366,262,p,'REVIEWER');circle(im,990,389,38,p['secondary']);tx(im,'B',990,389,31,p,p['bg'],70,anchor='center')
  q=ease(prog(t,.7,2.8));x=mix(457,693,q);card(im,x,386,130,101,p,'FILE',accent=True)
  trace(im,[(473,436),(807,436)],q,p);pill(im,'RECEIVED',858,480,263,p,q>=1)

def onboarding(im,t,cfg,p,v):
 if v==0:
  labs=lbl(cfg,['PROFILE','PREFERENCES','WORKSPACE']);active=min(2,max(0,int((t-.5)/1.15)))
  for j,s in enumerate(labs):
   xx=174+j*450;check(im,xx,281,p,1 if j<active else 0);tx(im,s,xx+28,281,25,p,w=324)
   if j<2:line(im,[(xx+298,281),(xx+412,281)],p['accent'] if j<active else p['muted'],3)
  card(im,253,338,774,253,p,labs[active]+' SETUP')
  for j,s in enumerate([['Name and role','Avatar selected','Contact ready'],['Theme selected','Notifications ready','Language selected'],['Sources imported','Tasks created','Ready to work']][active]):
   tx(im,s,287,421+j*57,29,p,w=660);check(im,969,421+j*57,p,1)
 elif v==1:
  card(im,90,251,741,347,p,'YOUR WORKSPACE')
  boxes=[(122,323,299,110),(453,323,346,110),(122,465,677,99)]
  idx=min(2,max(0,int((t-.6)/1.1)))
  for j,(x,y,w,h) in enumerate(boxes):rr(im,(x,y,x+w,y+h),p['bg'],15,p['accent'] if j==idx else p['muted'],3 if j==idx else 1)
  card(im,887,312,318,216,p,lbl(cfg,['OVERVIEW','ACTIVITY','NEXT STEP'])[idx],'Use this section to continue',True)
  trace(im,[(boxes[idx][0]+boxes[idx][2],boxes[idx][1]+boxes[idx][3]/2),(864,420),(887,420)],1,p)
 elif v==2:
  card(im,91,253,531,342,p,'PROFILE SETUP')
  for j,s in enumerate(lbl(cfg,['Name: Alex','Role: Creator','Preference: Clear UI'])):
   tx(im,s,127,351+j*76,27,p,w=465,opacity=prog(t,.55+j*.6,1.3+j*.6))
  card(im,704,253,491,342,p,'PROFILE PREVIEW');circle(im,950,396,54,p['secondary'])
  tx(im,'A',950,396,49,p,p['bg'],95,anchor='center');pill(im,'PROFILE READY',751,514,398,p,t>2.8)
 else:
  for j,s in enumerate(lbl(cfg,['UPLOAD','CLOUD','START EMPTY'])):
   xx=87+j*404;card(im,xx,252,291,163,p,s,'Import source',j==0 and t>1)
  q=ease(prog(t,1.3,3));card(im,235,447,810,153,p,'STARTER WORKSPACE')
  for j in range(3):
   xx=266+j*256;rr(im,(xx,508,xx+224,568),p['bg'],9,p['accent'] if q>.3+j*.2 else p['muted']);tx(im,f'ITEM {j+1}',xx+16,538,24,p,w=192,opacity=q)

def support(im,t,cfg,p,v):
 if v==0:
  items=[(81,253,815,'USER','I need help with this step.'),(367,377,814,'ASSISTANT','Let me check the details.'),(186,501,1023,'SPECIALIST','A team member is ready to help.')]
  for j,(x,y,w,s,body) in enumerate(items):
   q=ease(prog(t,.4+j*.75,1.15+j*.75));card(im,x,y+30*(1-q),w,93,p,s,body,accent=j==2 and q>=1)
 elif v==1:
  card(im,80,286,438,265,p,'SUPPORT TICKET','A clear issue description')
  pill(im,lbl(cfg,['ACCOUNT ISSUE'])[0],109,453,377,p,t>1.1)
  trace(im,[(518,418),(767,418)],prog(t,1.2,2.7),p,4)
  card(im,767,286,433,265,p,'ACCOUNT QUEUE','Assigned to the support team',t>2.7)
  pill(im,'ROUTED' if t>2.7 else 'CLASSIFYING',802,475,363,p,t>2.7)
 elif v==2:
  idx=1;q=ease(prog(t,.6,2));card(im,113,251,1051,351,p,'HELP CENTRE')
  tx(im,'How do I start?',148,332,29,p,w=971)
  yy=374;rr(im,(148,yy,1128,yy+58+118*q),p['bg'],14,p['accent']);tx(im,lbl(cfg,['How do I add a source?'])[0],168,yy+29,29,p,w=929)
  tx(im,'Choose a file and attach it to your workspace.',168,yy+86,26,p,w=918,opacity=q)
  pill(im,'OPEN UPLOAD',800,yy+111,304,p,q>=1)
  tx(im,'Where can I find my exports?',148,568,28,p,w=971)
 elif v==3:
  card(im,94,251,542,348,p,'RESOLUTION TIMELINE')
  for j,s in enumerate(lbl(cfg,['Issue reported','Fix applied','Result verified'])):
   yy=342+j*84;check(im,136,yy,p,prog(t,.5+j*.7,1.2+j*.7));tx(im,s,167,yy,27,p,w=415)
   if j<2:trace(im,[(136,yy+15),(136,yy+68)],prog(t,.8+j*.7,1.6+j*.7),p)
  card(im,702,251,491,348,p,'COMPLETE','The issue is resolved and checked',t>2.9)
  check(im,947,458,p,prog(t,2.3,3.2));pill(im,'RESOLVED',759,524,375,p,t>3.2)

def schematic_route(im,p,points,q):
 # This is an original generic route diagram, not a geographic map.
 for j in range(5):line(im,[(91,329+j*45),(707,329+j*45)],p['muted'],1)
 trace(im,points,q,p,5)
 for x,y in [points[0],points[-1]]:circle(im,x,y,10,p['accent'],p['text'],2)

def travel(im,t,cfg,p,v):
 if v==0:
  card(im,98,267,1081,322,p,'DELIVERY TRACKING')
  q=prog(t,.5,3.6)
  for j,s in enumerate(lbl(cfg,['ORDERED','PACKED','SHIPPED','DELIVERED'])):
   x=189+j*306;check(im,x,397,p,1 if q>=j/3 else 0);tx(im,s,x,466,25,p,w=251,anchor='center')
   if j<3:trace(im,[(x+17,397),(x+289,397)],clamp(q*3-j),p)
  pill(im,'PACKAGE ARRIVED' if q>=1 else 'ON THE WAY',433,523,417,p,q>=1)
 elif v==1:
  card(im,96,253,452,347,p,'BOOK A JOURNEY')
  for j,s in enumerate(lbl(cfg,['Morning route','Afternoon route','Evening route'])):pill(im,s,126,339+j*72,391,p,j==1 and t>1)
  card(im,631,253,564,347,p,'TRAVEL PASS','Origin  >  Destination',t>2.2)
  tx(im,'14:30',668,393,54,p,p['accent'],476)
  for j in range(18):
   hh=45+(j%3)*13;line(im,[(668+j*26,488),(668+j*26,488+hh)],p['text'],3+j%3)
  tx(im,'SCHEMATIC BOARDING CODE',668,571,16,p,p['muted'],476,'mono')
 elif v==2:
  card(im,76,254,684,344,p,'ROUTE DIAGRAM')
  q=prog(t,.5,3.9);points=[(124,495),(226,495),(307,394),(496,394),(667,325)]
  schematic_route(im,p,points,q)
  card(im,814,254,384,344,p,'ARRIVAL')
  tx(im,f'{max(0,round(18*(1-q)))} MIN',847,418,58,p,p['accent'],317)
  tx(im,'Destination point',847,511,25,p,w=319)
 else:
  for j,s in enumerate(lbl(cfg,['START  /  09:00','VISIT  /  11:00','RETURN  /  14:00'])):
   yy=254+j*117;active=j==min(2,max(0,int((t-.6)/1.1)))
   card(im,262 if active else 291,yy,731 if active else 673,92,p,s,'Itinerary stop',active)
   check(im,159,yy+46,p,1 if t>.5+j*.8 else 0)
   if j<2:trace(im,[(159,yy+60),(159,yy+148)],prog(t,.7+j*.8,1.5+j*.8),p)
   line(im,[(175,yy+46),(250 if active else 279,yy+46)],p['muted'],2)

def pricing(im,t,cfg,p,v):
 labs=lbl(cfg,['STARTER','PLUS','PRO'])
 if v==0:
  for j,s in enumerate(labs):
   x=75+j*405;selected=j==1 and t>1.3;yy=247 if selected else 267
   card(im,x,yy,320,318+(20 if selected else 0),p,s,accent=selected)
   tx(im,val(cfg,j,['RM 20','RM 50','RM 80'][j]),x+25,yy+98,42,p,p['accent'] if selected else p['text'],270)
   for k,a in enumerate(['Core tools','Useful templates','Export options']):tx(im,a,x+25,yy+172+k*41,23,p,w=273)
   pill(im,'SELECTED' if selected else 'VIEW PLAN',x+24,yy+267,272,p,selected)
 elif v==1:
  card(im,145,253,990,342,p,'BILLING OPTIONS');annual=t>1.5
  pill(im,'MONTHLY',180,327,415,p,not annual);pill(im,'ANNUAL',683,327,415,p,annual)
  tx(im,val(cfg,0,'RM 50 / month'),180,426,38,p,p['muted'] if annual else p['accent'],423)
  tx(im,val(cfg,1,'RM 480 / year'),683,426,38,p,p['accent'] if annual else p['muted'],421)
  pill(im,'SAMPLE SAVING: RM 120',466,514,349,p,annual)
 elif v==2:
  card(im,95,248,1090,351,p,'PLAN COMPARISON')
  for j,s in enumerate(labs):tx(im,s,604+j*221,316,25,p,w=202,anchor='center')
  for row,s in enumerate(['Basic tools','Extra templates','Team features']):
   yy=397+row*73;tx(im,s,128,yy,27,p,w=380)
   for col in range(3):check(im,604+col*221,yy,p,1 if col>=row and t>.5+row*.4+col*.4 else 0)
 elif v==3:
  card(im,80,279,429,278,p,'CURRENT PLAN');card(im,770,279,429,278,p,'UPGRADED PLAN',accent=t>2.7)
  q=prog(t,.5,3.2)
  for j,s in enumerate(['Storage','Exports','Team seats']):
   tx(im,s,110,356+j*63,23,p,w=365);progress(im,110,382+j*63,365,p,.35,9)
   tx(im,s,800,356+j*63,23,p,w=365);progress(im,800,382+j*63,365,p,.35+.6*q,9)
  trace(im,[(509,418),(770,418)],q,p,4)

def store(im,t,cfg,p,v):
 if v==0:
  card(im,78,253,556,344,p,'PRODUCT');asset(im,cfg,193,306,326,253,p)
  card(im,703,253,497,344,p,'SHOPPING CART')
  q=ease(prog(t,.75,2.7));token=layer(151,121);asset(token,cfg,0,0,151,121,p)
  paste(im,token,mix(469,733,q),mix(344,356,q),anchor='topleft')
  tx(im,'Product item',896,384,25,p,w=270,opacity=q)
  tx(im,'Quantity: 1',735,461,27,p,w=420,opacity=q)
  pill(im,'CHECKOUT',735,526,428,p,q>=1)
 elif v==1:
  q=ease(prog(t,.5,2.1));card(im,100,250,1080,349,p,'PRODUCT QUICKVIEW')
  asset(im,cfg,133,313,472,245,p)
  for j,s in enumerate(lbl(cfg,['Product title','A concise feature summary','Finish: selected option'])):tx(im,s,667,330+j*72,30 if j==0 else 24,p,w=470,opacity=q)
  pill(im,'ADD TO CART',667,527,470,p,q>=1)
 elif v==2:
  q=ease(prog(t,.65,2.4));card(im,91,248,1101,350,p,'PRODUCT BUNDLE')
  for j in range(3):
   x=mix(509,126+j*366,q);card(im,x,327,296,174,p,accent=q>.9);asset(im,cfg,x+12,339,272,149,p,j)
  pill(im,'BUNDLE TOTAL  /  '+val(cfg,0,'RM 120'),376,539,535,p,q>=1)
 else:
  card(im,80,250,491,348,p,'PRODUCT');asset(im,cfg,159,315,333,256,p)
  card(im,632,250,567,348,p,'REVIEW SUMMARY','Sample scores for layout demonstration')
  tx(im,val(cfg,0,'4.8 / 5'),667,374,44,p,p['accent'],483)
  for j,s in enumerate(lbl(cfg,['Design','Ease of use','Value'])):
   tx(im,s,667,438+j*53,24,p,w=160);progress(im,858,433+j*53,303,p,prog(t,.6+j*.3,2.3+j*.3)*(.9-j*.04),10)

def design(im,t,cfg,p,v):
 if v==0:
  q=ease(prog(t,.65,2.5));names=lbl(cfg,['BACKGROUND','CONTENT','CONTROLS'])
  for j,s in enumerate(names):
   yy=420+(j-1)*101*q;ImageDraw.Draw(im).polygon([(136,yy),(360,yy-47),(617,yy),(393,yy+50)],fill=[p['muted'],p['secondary'],p['accent']][j],outline=p['text'])
   card(im,763,273+j*108,426,86,p,s,f'LAYER 0{j+1}')
   trace(im,[(619,yy),(695,yy),(695,316+j*108),(763,316+j*108)],q,p)
 elif v==1:
  card(im,80,251,427,346,p,'COMPONENT LIBRARY');card(im,658,251,541,346,p,'INTERFACE PREVIEW')
  parts=[('BUTTON',326,90),('INPUT',420,76),('CARD',508,100)]
  for j,(s,y,h) in enumerate(parts):
   q=ease(prog(t,.55+j*.5,1.5+j*.5));xx=mix(114,694,q);yy=mix(y,324+j*83,q)
   rr(im,(xx,yy,xx+358,yy+58),p['accent'] if j==0 else p['bg'],12,p['secondary'])
   tx(im,s,xx+20,yy+29,24,p,p['bg'] if j==0 else p['text'],315)
 elif v==2:
  card(im,81,250,687,349,p,'LAYOUT CANVAS');card(im,826,250,371,349,p,'INSPECTOR')
  q=prog(t,.6,3);ww=330+154*q;rr(im,(164,350,164+ww,498),p['accent'],10+30*q)
  rr(im,(157,343,171+ww,505),None,4,p['text'],2)
  for x,y in [(157,343),(171+ww,343),(157,505),(171+ww,505)]:rr(im,(x-4,y-4,x+4,y+4),p['text'],1)
  for j,s in enumerate([f'WIDTH  {round(ww)}',f'RADIUS  {round(10+30*q)}','FILL  ACCENT']):tx(im,s,855,345+j*72,23,p,p['muted'] if j<2 else p['accent'],309,'mono')
 elif v==3:
  active=min(2,max(0,int((t-.5)/1.2)));card(im,86,246,1108,243,p,'ACTIVE VERSION')
  for j in range(active+1):rr(im,(128+j*343,324,430+j*343,451),[p['muted'],p['secondary'],p['accent']][j],12)
  for j in range(3):
   x=139+j*398;card(im,x,517,210,89,p,f'VERSION 0{j+1}',accent=j==active)
   if j<2:trace(im,[(x+210,561),(x+398,561)],1 if j<active else 0,p)

DRAWERS=[pipeline,composer,response,search,notifications,kanban,dashboard,checkout,controls,player,calendar,uploads,phones,devices,products,galleries,code,security,team,onboarding,support,travel,pricing,store,design]

def render(pid,t,cfg):
 metadata=PRESETS[pid];p=palette(cfg);im=base(cfg);scene=layer()
 # Tempo modifies the choreography while keeping content legible through the hold.
 action_t=min(4.08,max(0,t)*float(cfg.get('tempo',1)))
 DRAWERS[metadata['recipe_group']](scene,action_t,cfg,p,metadata['recipe_variant'])
 title(scene,cfg,p)
 q=ease(prog(t,.12,.6));opacity=q*(1-smooth(prog(t,4.35,5)))
 paste(im,scene,640,360+20*(1-q),opacity,scale=.98+.02*q)
 return im

if __name__=='__main__':
 target=Path(__file__).with_name('premium_ui_product_index.json')
 target.write_text(json.dumps(PRESETS,indent=2,ensure_ascii=False)+'\n')
 print(f'{len(PRESETS)} presets written to {target}')
