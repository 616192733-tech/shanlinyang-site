#!/usr/bin/env python3
import json, html, os, re, glob
BASE="https://www.shanlinyangapparel.com"; ROOT="/home/claude/shanlinyang-site"
CDN="https://image.made-in-china.com/2f0j00"
WA="https://wa.me/8617750659112?text=Hello%20Shanlinyang%2C%20I%27d%20like%20a%20quote%20for%20custom%20women%27s%20clothing."

# image key -> (path, alt)
P={
 "thread":"YWqkbmKcfouD/Fashion-Collar-Tight-Fit-Thread-Pit-Long-Sleeve-Suit-Women-s-Clothes.jpg",
 "denim":"dLWbfwFPkcgB/Women-2-Piece-Skirts-Casual-Outfits-Denim-Jeans-Suit-Clothes.jpg",
 "wideleg":"elDqTNmhLkzK/Sleeveless-Halter-Elastic-Waist-Slit-Wide-Leg-Sexy-Suit.jpg",
 "bratop":"giLqsFZzbbrt/Sexy-Hollow-out-Bra-Top-High-Waisted-Tight-Shorts-Set-Women-s-Clothes.jpg",
 "baseball":"LiPolYwsLMrA/Winter-Boutique-Fashion-Fitness-Gym-Casual-Baseball-Coats-Jackets-Two-Piece-Pants.jpg",
 "zipknit":"TipbzuCgJMrn/2024-Knitted-Sweater-Hoodies-Zipper-Slim-Long-Sleeve-Crop-Top-Clothes.jpg",
 "burnt":"LWDbpBOPYogT/Sports-Hollow-out-Burnt-Flower-Long-Sleeve-Pants-Women-s-Clothes.jpg",
 "jumpsuit":"NlHoScnRSKrs/Jumpsuits-Women-Clothes-Sexy-One-Piece-Fitness-Jumpsuit-for-Ladies.jpg",
 "halterdress":"iLKcqNbCMzpd/2024-Cheap-Women-s-Summer-Solid-Dresses-Casual-Clothing-Halter-Backless-Dress.jpg",
 "bodycon":"aVgcPWCtqBzD/2024-Women-Clothing-Sexy-Long-Sleeve-Backless-Ladies-Bodycon-Mini-Dress.jpg",
 "sequin":"OWPkYpFnAouH/One-Line-Shoulder-French-Waist-Sequin-Skirt-Midlength-Dress.jpg",
 "camo":"OigbPVjnMerS/2023-Plus-Size-Casual-Fashion-Waisted-Woven-Camouflage-Short-Jumpsuit-for-Woman.jpg",
 "rhine":"pWgbiMCyCezU/Women-Sexy-Deep-V-Cut-Hollow-out-Glitter-One-Piece-Rhinestone-Swimwear.jpg",
 "logoswim":"JVHotkygrjus/Custom-Logo-Summer-Swimsuits-Halter-V-Neck-Sexy-One-Piece-Swimwear.jpg",
 "kimono":"WVrkuMZykBpm/Sexy-Swimwear-Coverup-Summer-2024-Beach-Kimonos-Long-Cover-UPS-for-Women.jpg",
 "feather":"QircHoGBVMzt/Women-s-Strapless-Backless-Pure-Sex-Style-Feather-Sequin-Dress.jpg",
 "meshparty":"ohVcPIRtsCpW/Sexy-Mesh-Girls-Party-Ladies-Short-Bodycon-See-Through-Backless-Dress.jpg",
 "laceup":"ahVcQDUlTCgG/Women-Lace-up-Crop-Top-Club-Wear-Outfits-Ladies-Sexy-Mini-Dress.jpg",
 "meshromper":"MlhcKqTRHCrL/Sexy-Jumpsuits-Knit-Mesh-Long-Sleeve-Rompers-Club-Wear-Women-s-Clothes.jpg",
 "tasselcover":"mihkPREnbvgD/Trendy-Women-Beach-Wear-Cover-up-Tassel-Swimwear-for-Ladies.jpg",
 # NEW batch
 "auradress":"phgqivWKgouf/Aura-Queen-Purple-Dress-Annual-Birthday-Catwalk-Evening-Dress.jpg",
 "vsequin":"ylHqcVbPfkus/Wholesale-V-Neck-Long-Sleeve-Short-Sequin-Hip-Wrap-Dress.jpg",
 "featherwrap":"WiucafzZgegJ/Deep-V-Backless-Sleeveless-Feather-Wrap-Hip-Dress-Wholesale.jpg",
 "velvetjump":"SxvpyrcVnWUX",  # price page had no og:image captured cleanly; will reuse if needed
 "velvettrack":"YiCbemrWHzgu/Women-Winter-Thicken-Velvet-Long-Sleeve-Sports-Wear-Tracksuit-Two-Piece-Sets-Clothes.jpg",
 "cottontrack":"EIscQutzILpA/Summer-Cotton-Tracksuit-Women-s-Jogging-Crop-Top.jpg",
 "printbikini":"ylBbqdEkrogI/2024-Swimwear-Beachwear-Wholesale-Printed-Bikini-and-Skirt.jpg",
}
def src(k): return f"{CDN}/{P[k]}"

# ============ EXPANDED CATEGORY DATA (6-8 products each) ============
CATS={
 "two-piece-sets":dict(name="Two-Piece & Three-Piece Sets",h1="Wholesale & Custom Women's Two-Piece Sets",
   title="Custom Women's Two Piece Sets Manufacturer | Wholesale Matching Sets China",
   desc="Factory-direct women's two-piece sets: thread-knit suits, denim skirt sets, halter wide-leg, velvet & cotton tracksuit sets. Real photos & FOB prices. Custom logo from 100pcs.",
   intro="Matching sets are our highest-volume line. Photos are our own studio shots; FOB prices are real wholesale tiers. Open-pack wholesale from 2 pieces, full custom with your branding from 100 pieces per color per style.",
   tags=["all","knit","casual","luxe"],
   products=[
     ("918","Thread-Knit Long Sleeve Suit","Ribbed thread-pit knit, collar top + fitted bottom","Spandex/Polyester · S–XL","thread",7.82,8.55,2,"knit"),
     ("LYSKMEQ-196","Denim Skirt Two-Piece Set","Light-blue patch denim top + skirt set","Poly-cotton denim · S–XXL","denim",18.56,20.04,2,"casual"),
     ("LYS-005","Halter Slit Wide-Leg Suit","Halter top + slit wide-leg pant, autumn line","Spandex/Cotton · XS–XL","wideleg",6.06,8.02,2,"casual"),
     ("1113","Bra Top + High-Waist Shorts Set","Cut-out bralette with high-waist short","Polyester · S–L","bratop",10.68,11.66,2,"knit"),
     ("YD8791","Thick Velvet Tracksuit Set","Winter velvet long-sleeve sports two-piece, anti-UV","Velvet poly-spandex · S–XXL","velvettrack",10.98,12.56,1,"luxe"),
     ("HR8163","Summer Cotton Jogging Set","Lightweight cotton crop + short tracksuit","Cotton/Polyester · S–XL","cottontrack",7.11,7.64,2,"casual"),
     ("KNIT-01","Zipper Crop Knit Hoodie Set","Zip-front knit crop set, private-label base","Polyester knit · custom","zipknit",8.83,11.03,2,"knit"),
     ("123","Baseball Jacket + Pants Set","Varsity-style two-piece for gym &amp; street","Breathable knit · custom","baseball",10.58,11.27,2,"casual"),
   ]),
 "tracksuits-joggers":dict(name="Tracksuits & Joggers",h1="Custom Tracksuit Manufacturer — Velvet, Knit & Cotton",
   title="Custom Tracksuit Manufacturer China | Velvet & Jogger Sets Wholesale",
   desc="OEM tracksuits & jogger sets: thick velvet sports suits, summer cotton joggers, baseball sets, zipper knit crop hoodies. Real photos & FOB prices. Custom logo from 100pcs.",
   intro="From thick winter velvet to lightweight summer cotton, we produce tracksuits the way streetwear and athleisure brands spec them: matched dye lots, clean embroidery, branded trims.",
   tags=["all","winter","summer","knit"],
   products=[
     ("YD8791","Thick Velvet Winter Tracksuit","Anti-static, anti-UV velvet sports two-piece","Velvet poly-spandex · S–XXL","velvettrack",10.98,12.56,1,"winter"),
     ("123","Baseball Jacket Tracksuit","Boutique fitness baseball coat + pants","Breathable knit · custom","baseball",10.58,11.27,2,"winter"),
     ("HR8163","Summer Cotton Jogging Set","Breathable cotton crop + short set","Cotton/Polyester · S–XL","cottontrack",7.11,7.64,2,"summer"),
     ("KNIT-01","Zipper Slim Crop Hoodie Set","2024 knit sweater hoodie, zip front","Polyester knit · custom","zipknit",8.83,11.03,2,"knit"),
     ("918","Thread-Knit Track Suit","Tight-fit collar suit, gym-to-street","Spandex/Polyester · S–XL","thread",7.82,8.55,2,"knit"),
     ("1113","Bra + Short Training Set","Hollow-out bralette + compression short","Polyester · S–L","bratop",10.68,11.66,2,"summer"),
   ]),
 "activewear-yoga":dict(name="Activewear & Yoga Wear",h1="Activewear & Yoga Wear Manufacturer for Private Labels",
   title="Private Label Activewear Manufacturer China | Gym & Yoga Sets Low MOQ",
   desc="Custom gym & yoga wear: burnt-flower sport sets, bra+shorts gym sets, fitness jumpsuits, mesh rompers. Real photos & FOB prices. Private label from 100pcs.",
   intro="Our activewear line is built on stretch knits with opacity-checked bottoms. Launch capsule gym collections without committing to thousand-piece runs. Photos are our own studio shots.",
   tags=["all","sets","onepiece"],
   products=[
     ("SPT-01","Burnt-Flower Long Sleeve Sport Set","Hollow-out burnout floral two-piece","Spandex/Polyester · S–L","burnt",8.72,9.70,2,"sets"),
     ("1113","Bra Top + High-Waist Shorts Set","Hollow-out bralette + compression short","Polyester · S–L","bratop",10.68,11.66,2,"sets"),
     ("JMP-02","One-Piece Fitness Jumpsuit","Quick-dry stretch unitard for studio lines","Quick-dry knit · S–L","jumpsuit",3.91,4.89,2,"onepiece"),
     ("LYSKMEQ-037","Knit Mesh Long Sleeve Romper","Sheer mesh romper, club &amp; festival","Knit mesh · free size","meshromper",2.23,4.19,2,"onepiece"),
     ("HR8163","Cotton Jogging Crop Set","Breathable cotton crop + short","Cotton/Polyester · S–XL","cottontrack",7.11,7.64,2,"sets"),
     ("918","Ribbed Thread Active Set","Ribbed crop + legging, contour seams","Ribbed knit · S–XL","thread",7.82,8.55,2,"sets"),
   ]),
 "dresses":dict(name="Dresses",h1="Women's Dress Manufacturer — Casual, Sequin, Feather & Bodycon",
   title="Women's Dress Manufacturer China | Custom Summer, Sequin & Evening Dresses",
   desc="Dress factory: halter summer dresses, sequin midis, feather wrap dresses, mesh-rhinestone gowns, evening dresses. Real photos & FOB prices from US$5.39. OEM from 100pcs.",
   intro="Dresses are where our light-fabric and embellishment expertise shows: silk-touch poly, satin, sequin, feather and mesh — cut for US and EU bodies. Photos are our own studio shots.",
   tags=["all","casual","occasion","party"],
   products=[
     ("LYSKMEQ-116","Halter Backless Summer Dress","Casual halter midi, open back — best-seller","Spandex/Polyester · S–XL","halterdress",5.39,6.27,2,"casual"),
     ("LYSKMEQ-001","Backless Bodycon Mini Dress","Fitted long-sleeve mini, spring/summer","Spandex/Polyester · S–XL","bodycon",7.69,9.65,2,"casual"),
     ("11056","One-Shoulder Sequin Midi Dress","Satin sequin midi — 14 colorways","Satin/sequin · long sleeve","sequin",9.33,11.80,1,"occasion"),
     ("1011","Aura Queen Sequin Evening Dress","Full-length catwalk sequin gown, birthday/evening","Poly/spandex sequin · S–XL","auradress",27.35,30.65,2,"occasion"),
     ("11037","V-Neck Sequin Hip Wrap Dress","Long sleeve short sequin wrap, 3 colors","Spandex/Polyester · S–XL","vsequin",8.82,10.89,2,"party"),
     ("1008","Feather Wrap Hip Dress","Deep-V backless feather-trim mini","Poly/spandex · S–XL","featherwrap",10.09,13.62,2,"party"),
     ("11057","Lace-Up Crop Mini Dress","Club-wear lace-up mini, spring/autumn","Poly/spandex · S–XL","laceup",7.60,8.19,2,"party"),
     ("PARTY-01","Mesh See-Through Party Dress","Sheer bodycon mesh party dress","Poly/spandex · S–XL","meshparty",6.45,7.43,2,"party"),
   ]),
 "plus-size":dict(name="Plus Size XL–5XL",h1="Plus Size Clothing Manufacturer (XL–5XL)",
   title="Plus Size Clothing Manufacturer China XL-5XL | Wholesale Curve Fashion",
   desc="Plus size women's clothing: S–5XL jumpsuits, curve suits, halter dresses graded on real curve blocks. Real photos & FOB prices. Custom label from 100pcs.",
   intro="Curve is graded on real plus-size blocks — not scaled-up straight sizes. Our styles run through 5XL, a range most factories won't produce at low MOQ. Photos are our own studio shots.",
   tags=["all","sets","dress","jumpsuit"],
   products=[
     ("PLS-01","Plus Size Camo Short Jumpsuit","Stocked S through 5XL — direct digital print","Woven · S–5XL","camo",9.49,11.45,2,"jumpsuit"),
     ("LYS-005","Curve Halter Wide-Leg Suit","Elastic-waist suit, graded to curve on request","Spandex/Cotton · to 5XL","wideleg",6.06,8.02,2,"sets"),
     ("LYSKMEQ-116","Curve Halter Backless Dress","Best-selling halter, extended sizing","Spandex/Polyester · to 5XL","halterdress",5.39,6.27,2,"dress"),
     ("YD8791","Curve Velvet Tracksuit","Velvet sports set, sizes to XXL+ on request","Velvet poly-spandex · to 5XL","velvettrack",10.98,12.56,1,"sets"),
     ("11037","Curve V-Neck Sequin Dress","Occasion sequin wrap, curve grading","Spandex/Polyester · to 4XL","vsequin",8.82,10.89,2,"dress"),
     ("LYSKMEQ-037","Curve Mesh Romper","Stretch mesh romper, free-size to curve","Knit mesh · free–curve","meshromper",2.23,4.19,2,"jumpsuit"),
   ]),
 "swimwear":dict(name="Swimwear & Beachwear",h1="Swimwear Manufacturer — One-Pieces, Bikinis & Cover-Ups",
   title="Custom Swimwear Manufacturer China | Bikini Sets & Beachwear Low MOQ",
   desc="Swimwear factory: rhinestone one-pieces, custom-logo swimsuits, 3-piece printed bikini sets, beach kimonos & tassel cover-ups. Real photos & FOB prices. Custom from 100pcs.",
   intro="Swim is produced on dedicated lines with flatlock seams and lined cups. The halter one-piece is our custom-logo base style. Photos are our own studio shots.",
   tags=["all","onepiece","bikini","coverup"],
   products=[
     ("LYSKMEQ-151","Rhinestone Glitter One-Piece","Deep-V statement swimsuit for resort","Spandex/Nylon · S–XXL","rhine",5.80,6.83,5,"onepiece"),
     ("LYSKMEQ-064","Custom Logo Halter One-Piece","Our private-label base, quick-dry","Poly-spandex · S–XXL","logoswim",6.21,7.76,2,"onepiece"),
     ("LYSKMEQ-013","3-Piece Printed Bikini + Skirt","Halter bikini with matching beach skirt","Poly/spandex · S–2XL","printbikini",5.64,6.63,2,"bikini"),
     ("LYSKMEQ-023","Beach Kimono Long Cover-Up","Sheer quick-dry kimono cover-up","Poly-spandex · S–L","kimono",6.10,7.61,2,"coverup"),
     ("LYSKMEQ-192","Tassel Beach Cover-Up","Trendy tassel beachwear, one size","Acrylic/Cotton · OS","tasselcover",6.45,7.50,5,"coverup"),
   ]),
}

# extract header/footer (already has fab-wa, reveal script, lookbook nav)
ref=open(f"{ROOT}/about.html").read()
HEAD=ref[:ref.index('<div class="topbar">')]
header=ref[ref.index('<div class="topbar">'):ref.index('<main id="main">')+len('<main id="main">')]
footer=ref[ref.index('</main>'):]

def page(path,title,desc,canon,body,lds,ogimg):
    ld="\n".join('<script type="application/ld+json">\n%s\n</script>'%json.dumps(o,ensure_ascii=False,indent=1) for o in lds)
    h=HEAD
    h=re.sub(r'<title>.*?</title>',f'<title>{html.escape(title)}</title>',h,flags=re.S)
    h=re.sub(r'<meta name="description" content=".*?">',f'<meta name="description" content="{html.escape(desc,quote=True)}">',h)
    h=re.sub(r'<link rel="canonical" href=".*?">',f'<link rel="canonical" href="{canon}">',h)
    h=re.sub(r'<meta property="og:title" content=".*?">',f'<meta property="og:title" content="{html.escape(title,quote=True)}">',h)
    h=re.sub(r'<meta property="og:description" content=".*?">',f'<meta property="og:description" content="{html.escape(desc,quote=True)}">',h)
    h=re.sub(r'<meta property="og:url" content=".*?">',f'<meta property="og:url" content="{canon}">',h)
    h=re.sub(r'<meta property="og:image" content=".*?">',f'<meta property="og:image" content="{ogimg}">',h)
    h=re.sub(r'<script type="application/ld\+json">.*</script>',ld,h,flags=re.S)
    open(os.path.join(ROOT,path),"w").write(h+header+"\n"+body+footer)
    print("wrote",path)

def crumbs(items):
    lis="".join(f'<li><a href="{u}">{html.escape(n)}</a></li>' if u else f'<li aria-current="page">{html.escape(n)}</li>' for n,u in items)
    ld={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,**({"item":BASE+u} if u else {})} for i,(n,u) in enumerate(items)]}
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{lis}</ol></div></nav>',ld

CAT_FAQ={
 "two-piece-sets":[("Can I mix sizes within the 100pcs custom MOQ?","Yes — split the 100 pieces per color across any size curve (S–XL or XL–5XL) at no extra charge."),("Are tops and bottoms cut from the same dye lot?","Yes. Sets are cut and dyed together so the top and bottom match exactly, even on reorders.")],
 "tracksuits-joggers":[("Can you embroider our logo on velvet and fleece?","Yes — flat, 3D puff and appliqué embroidery on velvet, fleece and knit, included in custom pricing at 100pcs+."),("What fabric weights are available?","Velvet 240–320gsm, fleece/terry 280–420gsm, summer cotton blends 180–240gsm. Swatch cards ship with every sample.")],
 "activewear-yoga":[("Are your bottoms squat-proof?","Bulk fabrics are 220–260gsm spandex blends with opacity checked at QC; an opacity & stretch report ships with samples."),("Can you do custom all-over prints?","Yes — sublimation prints and burnout florals from 100–300pcs depending on base fabric.")],
 "dresses":[("Can you produce sequin and feather styles at low MOQ?","Yes — sequin application and feather trims are done in-house, available from 100pcs per color (1pc MOQ on some stock styles)."),("Do you grade dresses to EU sizes?","Yes, to both US (0–24) and EU (32–56) charts, with dual-label sizing for both markets.")],
 "plus-size":[("Do you use real plus-size patterns or scaled grading?","Separate curve blocks with adjusted rise, bust dart and arm openings, fit-tested on 2XL forms before bulk."),("What is the size range?","Standard XL–5XL; extended to 6XL on knit styles by request.")],
 "swimwear":[("Can you do custom prints and logos on swim?","Yes — the halter one-piece is our custom-logo base; sublimation prints and logo tags from 100pcs."),("Are fabrics chlorine resistant?","Nylon/poly-spandex tested for chlorine and UV; certificates ship with the QC report.")],
}

for slug,c in CATS.items():
    canon=f"{BASE}/products/{slug}.html"
    cr,crl=crumbs([("Home","/"),("Products","/products/"),(c["name"],None)])
    items_ld={"@context":"https://schema.org","@type":"ItemList","itemListElement":[]}
    cards=""
    for i,(no,nm,dd,fab,k,lo,hi,moq,tag) in enumerate(c["products"]):
        u=src(k)
        items_ld["itemListElement"].append({"@type":"ListItem","position":i+1,"item":{
            "@type":"Product","name":nm,"sku":no,"description":re.sub('&amp;','&',dd),"image":u,
            "brand":{"@type":"Brand","name":"Shanlinyang Apparel"},"material":fab.split("·")[0].strip(),
            "offers":{"@type":"AggregateOffer","priceCurrency":"USD","lowPrice":f"{lo:.2f}","highPrice":f"{hi:.2f}","availability":"https://schema.org/InStock","url":canon}}})
        cards+=f'''<article class="pcard" data-tag="{tag}">
  <div class="ph qv-open" style="background:#fff" data-img="{u}" data-no="{html.escape(no)}" data-nm="{html.escape(nm)}" data-fob="US${lo:.2f}–{hi:.2f}" data-fab="{html.escape(fab)}" data-moq="{moq}" role="button" tabindex="0" aria-label="Quick view {html.escape(nm)}">
    <img src="{u}" alt="{html.escape(nm)} — Shanlinyang Apparel factory photo" loading="lazy" width="420" height="525" style="width:100%;height:100%;object-fit:cover"></div>
  <div class="meta"><span class="style-no">STYLE {html.escape(no)}</span><h3>{html.escape(nm)}</h3>
  <p class="fab">{dd} · <strong>{html.escape(fab.split("·")[0].strip())}</strong></p>
  <span class="moq">FOB US${lo:.2f}–{hi:.2f} · STOCK FROM {moq} PCS · CUSTOM 100 PCS</span></div>
</article>\n'''
    # filter bar
    tagnames={"all":"All","knit":"Knit","casual":"Casual","luxe":"Luxe","winter":"Winter","summer":"Summer","sets":"Sets","onepiece":"One-Piece","occasion":"Occasion","party":"Party","dress":"Dress","jumpsuit":"Jumpsuit","bikini":"Bikini","coverup":"Cover-Up"}
    pills="".join(f'<button data-filter="{t}"{" class=\"active\"" if t=="all" else ""}>{tagnames.get(t,t.title())}</button>' for t in c["tags"])
    faqs=CAT_FAQ[slug]
    faq_html="".join(f'<details><summary>{html.escape(q)}</summary><div class="a">{html.escape(a)}</div></details>' for q,a in faqs)
    faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    strip="".join(f'<img src="{src(p[4])}" alt="" aria-hidden="true">' for p in c["products"][:6])
    body=f'''{cr}
<section class="cat-hero">
  <div class="bgstrip" aria-hidden="true">{strip}</div>
  <div class="wrap">
    <span class="spec-label" style="color:#E48BB1">PRODUCT LINE — {html.escape(c["name"].upper())}</span>
    <h1>{html.escape(c["h1"])}<span class="count-chip">{len(c["products"])} STYLES SHOWN</span></h1>
    <p class="lead">{html.escape(c["intro"])}</p>
    <p style="margin-top:1.2rem"><a class="btn" href="/contact.html">Request the line sheet</a> &nbsp; <a class="btn btn--wa" href="{WA}" rel="noopener">Quote on WhatsApp</a></p>
  </div>
</section>
<section class="band"><div class="wrap">
<div class="filterbar" role="group" aria-label="Filter styles">{pills}</div>
<div class="grid-3" style="margin-top:1rem">
{cards}</div>
<p style="margin-top:1.4rem;font-family:var(--font-mono);font-size:.78rem;color:var(--mono-grey)">961 STYLES IN THE FULL CATALOG · TAP ANY PHOTO FOR QUICK VIEW — <a href="/contact.html">REQUEST THE FULL LINE SHEET →</a></p>
</div></section>
<section class="band band--tint faq"><div class="wrap">
<span class="spec-label">BUYER QUESTIONS — {html.escape(c["name"].upper())}</span><h2>FAQ</h2>{faq_html}
</div></section>'''
    page(f"products/{slug}.html",c["title"],c["desc"],canon,body,[crl,items_ld,faq_ld],src(c["products"][0][4]))

print("category pages expanded")

# ============ GLOBAL JS: quick-view + filters + scroll progress + count-up ============
QV='''
<div id="qv" role="dialog" aria-modal="true" aria-label="Product quick view"><span class="close" id="qvClose" role="button" tabindex="0" aria-label="Close">×</span>
<div class="box"><img id="qvImg" src="" alt=""><div class="det">
<span class="style-no" id="qvNo"></span><h3 id="qvNm"></h3><div class="price" id="qvFob"></div>
<table><tr><td>Fabric</td><td id="qvFab"></td></tr><tr><td>Stock MOQ</td><td id="qvMoq"></td></tr><tr><td>Custom MOQ</td><td>100 pcs / color / style</td></tr><tr><td>Sampling</td><td>7–12 days</td></tr><tr><td>Logo</td><td>Print · embroidery · woven label</td></tr></table>
<div class="acts"><a class="btn btn--wa" id="qvWa" href="%s" rel="noopener">Quote this style on WhatsApp</a><a class="btn btn--ghost" href="/contact.html">Send an inquiry form</a></div>
</div></div></div>
<div class="scrollbar-top" id="scrollbar"></div>
<script>
(function(){
// scroll progress
var sb=document.getElementById('scrollbar');
if(sb)addEventListener('scroll',function(){var h=document.documentElement;var p=h.scrollTop/(h.scrollHeight-h.clientHeight)*100;sb.style.width=p+'%%';},{passive:true});
// quick view
var qv=document.getElementById('qv');
function openQV(el){
  document.getElementById('qvImg').src=el.dataset.img;
  document.getElementById('qvImg').alt=el.dataset.nm;
  document.getElementById('qvNo').textContent='STYLE '+el.dataset.no;
  document.getElementById('qvNm').textContent=el.dataset.nm;
  document.getElementById('qvFob').textContent='FOB '+el.dataset.fob;
  document.getElementById('qvFab').textContent=el.dataset.fab;
  document.getElementById('qvMoq').textContent=el.dataset.moq+' pcs (test order)';
  document.getElementById('qvWa').href='https://wa.me/8617750659112?text='+encodeURIComponent('Hello Shanlinyang, please quote style '+el.dataset.no+' ('+el.dataset.nm+').');
  qv.classList.add('on');document.body.style.overflow='hidden';
}
function closeQV(){qv.classList.remove('on');document.body.style.overflow='';}
document.querySelectorAll('.qv-open').forEach(function(el){
  el.addEventListener('click',function(){openQV(el)});
  el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();openQV(el)}});
});
if(qv){document.getElementById('qvClose').onclick=closeQV;qv.addEventListener('click',function(e){if(e.target===qv)closeQV()});
addEventListener('keydown',function(e){if(e.key==='Escape')closeQV()});}
// filters
var pills=document.querySelectorAll('.filterbar button');
pills.forEach(function(b){b.onclick=function(){
  pills.forEach(function(x){x.classList.remove('active')});b.classList.add('active');
  var f=b.dataset.filter;
  document.querySelectorAll('.pcard[data-tag]').forEach(function(c){
    c.classList.toggle('hide', f!=='all' && c.dataset.tag!==f);});
};});
// count-up stats
var ce=document.querySelectorAll('.stats b');
if(ce.length){var io=new IntersectionObserver(function(en){en.forEach(function(x){
  if(x.isIntersecting){var el=x.target;var t=el.textContent;var m=t.match(/[\\d,]+/);
  if(m){var n=parseInt(m[0].replace(/,/g,''));var suf=t.replace(m[0],'');var s=0,step=Math.max(1,Math.ceil(n/40));
  var iv=setInterval(function(){s+=step;if(s>=n){s=n;clearInterval(iv)}el.textContent=s.toLocaleString()+suf;},22);}
  io.unobserve(el);}});},{threshold:.5});ce.forEach(function(e){io.observe(e)});}
})();
</script>
</body>''' % WA

for f in glob.glob(f"{ROOT}/**/*.html",recursive=True):
    s=open(f).read()
    if 'id="qv"' in s: continue  # idempotent
    s=s.replace("</body>",QV,1)
    open(f,"w").write(s)
print("global quick-view/filter/scroll JS injected")

# ============ update sitemap lastmod ============
print("v5 build complete")
