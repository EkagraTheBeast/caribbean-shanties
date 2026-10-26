from __future__ import annotations
import hashlib, json, re, shutil, struct, unicodedata, csv
from pathlib import Path
from PIL import Image, ImageDraw

SOURCE=Path(r"C:\Users\Ekagra\Downloads\Mod Work\Shanties Music Discs")
PROJECT=Path(__file__).resolve().parents[1]
RES=PROJECT/"src/main/resources"; NS="caribbean_shanties"
ASSETS=RES/"assets"/NS; DATA=RES/"data"/NS/"jukebox_song"

def norm(s):
    s=unicodedata.normalize("NFKD",s)
    s="".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+"," ",s).strip()

def slug(s): return re.sub(r"_+","_",re.sub(r"[^a-z0-9]+","_",norm(s))).strip("_")

def parse_name(filename):
    stem=Path(filename).stem; low=stem.casefold()
    game="black_flag"; artist="Various Artists"
    if "rogue" in low: game="rogue"
    elif "resynced" in low: game="resynced"
    if game=="resynced":
        bits=[b.strip(" .") for b in stem.split("｜") if b.strip(" .")]
        if bits and ("dagher" in bits[-1].casefold() or "greene" in bits[-1].casefold()): artist=bits[-1]
        m=re.match(r"\s*(.+?)\s*\(Sea Shanty",stem,re.I)
        title=m.group(1) if m else stem.split("｜",1)[0]
    elif game=="rogue":
        m=re.search(r"\)\s*-\s*(.+?)(?:\s*\(Track\s*\d+\))?$",stem,re.I); title=m.group(1) if m else stem
    elif "sea shanty edition" in low:
        m=re.search(r"\s-\s(.+?)(?:\s*\(Track\s*\d+\))?$",stem,re.I); title=m.group(1) if m else stem
    elif "sea shanty -" in low and stem.startswith(("'", '"', "“", "＂")):
        m=re.match(r"['\"“＂](.+?)['\"”＂]\s*Sea Shanty",stem,re.I); title=m.group(1) if m else stem
    elif "sea shanty -" in low:
        title=re.split(r"sea shanty\s*-",stem,flags=re.I,maxsplit=1)[1]
    elif "sea shanty" in low:
        m=re.match(r"['\"“＂](.+?)['\"”＂]\s*Sea Shanty",stem,re.I)
        title=m.group(1) if m else re.split(r"\s*\(Sea Shanty",stem,flags=re.I,maxsplit=1)[0]
    elif "｜" in stem:
        bits=[p.strip() for p in stem.split("｜") if p.strip()]
        title=bits[0] if bits else stem
    else:
        m=re.search(r"shanty\s+['\"“＂](.+?)['\"”＂]",stem,re.I); title=m.group(1) if m else stem
    title=re.sub(r"\s*\(Track\s*\d+\)\s*$","",title,flags=re.I).strip(" .\t")
    title=re.sub(r"\s+"," ",title).strip(" '\"“”＂")
    if norm(title)=="hi for the beggerman": title="Hi for the Beggarman"
    if norm(title)=="good morning ladies all": title="Good Morning Ladies All"
    if norm(title)=="running down to cuba": title="Running Down to Cuba"
    return title,game,artist

def ogg_info(path):
    b=path.read_bytes(); p=0; rate=None; codec=""; granule=0; packets=[]; packet=bytearray()
    while p+27<=len(b):
        if b[p:p+4]!=b"OggS" or b[p+4]!=0: raise ValueError("invalid Ogg page")
        n=b[p+26]; segs=b[p+27:p+27+n]; body=p+27+n
        gp=struct.unpack_from("<Q",b,p+6)[0]
        if gp!=0xFFFFFFFFFFFFFFFF: granule=max(granule,gp)
        for size in segs:
            packet.extend(b[body:body+size]); body+=size
            if size<255: packets.append(bytes(packet)); packet.clear()
        p=body
    if p!=len(b): raise ValueError("truncated Ogg stream")
    first=packets[0] if packets else b""
    if first.startswith(b"\x01vorbis"): codec="vorbis"; rate=struct.unpack_from("<I",first,12)[0]
    elif first.startswith(b"OpusHead"): codec="opus"
    else: raise ValueError("not OGG Vorbis or Opus")
    return {"codec":codec,"rate":rate,"duration":round(granule/rate,3) if rate else 0,"sha256":hashlib.sha256(b).hexdigest(),"audio_fingerprint":hashlib.sha256(b"".join(packets[3:])).hexdigest() if codec=="vorbis" else hashlib.sha256(b"".join(packets[2:])).hexdigest(),"size":len(b)}

def writejson(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def texture(path,sid,game):
    seed=int(hashlib.sha256(sid.encode()).hexdigest()[:8],16)
    base={"rogue":(58,108,91),"resynced":(38,104,130)}.get(game,(150,91,43))
    im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.ellipse((2,2,29,29),fill=(30,25,22,255),outline=(220,194,140,255))
    for r in (5,8,11,14,17,20,23,26):
        q=r//2; d.ellipse((16-q,16-q,16+q,16+q),outline=(58+seed%22,52,43,255))
    col=tuple(max(0,min(255,c+(seed%19)-9)) for c in base)+(255,)
    d.ellipse((8,8,23,23),fill=col,outline=(239,213,161,255))
    d.ellipse((13,13,18,18),fill=(41,34,28,255)); d.ellipse((15,15,16,16),fill=(240,220,168,255))
    for i in range(4):
        x=10+((seed>>(i*4))%13); y=10+((seed>>(i*3+2))%13)
        if 11<=x<=20 and 11<=y<=20 and (x,y) not in ((15,15),(16,16)): d.point((x,y),fill=(232,209,161,255))
    path.parent.mkdir(parents=True,exist_ok=True); im.save(path)

def main():
    if not SOURCE.is_dir(): raise SystemExit(f"Audio folder missing: {SOURCE}")
    files=sorted(SOURCE.glob("*.ogg"),key=lambda p:p.name.casefold())
    if not files: raise SystemExit("No OGG files in supplied audio folder")
    groups={}
    for p in files:
        title,game,artist=parse_name(p.name); key=norm(title)
        if not title or not key: raise SystemExit(f"Could not parse title: {p.name}")
        meta=ogg_info(p)
        if meta["codec"]!="vorbis": raise SystemExit(f"{p.name}: codec {meta['codec']}; expected Vorbis")
        groups.setdefault(key,[]).append({"path":p,"title":title,"game":game,"artist":artist,"key":key,"meta":meta})
    songs=[]
    for key,versions in groups.items():
        pick=sorted(versions,key=lambda x:(x["meta"]["size"]*8/max(x["meta"]["duration"],1),x["meta"]["rate"] or 0,x["game"]=="resynced"),reverse=True)[0]
        games={x["game"] for x in versions}
        label="Assassin's Creed Rogue" if games=={"rogue"} else "Assassin's Creed IV: Black Flag Resynced" if games=={"resynced"} else "Assassin's Creed 4 Black Flag"
        if "black_flag" in games and "resynced" in games: label="Assassin's Creed 4 Black Flag"
        songs.append({**pick,"id":slug(pick["title"]),"label":label,"games":games,"versions":versions})
    songs.sort(key=lambda s:norm(s["title"]))
    valid_songs={s["id"] for s in songs}
    # Remove stale generated assets from a prior import while retaining the original starter sheet.
    for folder, suffix in ((ASSETS/"sounds"/"shanties",".ogg"),(DATA,".json")):
        if folder.exists():
            for old_file in folder.glob("*"+suffix): old_file.unlink()
    for folder, suffix in ((ASSETS/"models"/"item",".json"),(ASSETS/"items",".json"),(ASSETS/"textures"/"item",".png")):
        if folder.exists():
            for old_file in folder.glob("shanty_*"+suffix): old_file.unlink()
    for folder in (ASSETS/"sounds"/"shanties",ASSETS/"models"/"item",ASSETS/"items",ASSETS/"textures"/"item",ASSETS/"lang",DATA): folder.mkdir(parents=True,exist_ok=True)
    sounddefs={}; lang={"itemGroup.caribbean_shanties.shanties":"Sea Shanties"}; java_rows=[]; manifest=[]
    for s in songs:
        sid=s["id"]; itemid="shanty_"+sid; ev="shanty."+sid; soundfile=f"shanties/{sid}.ogg"
        shutil.copy2(s["path"],ASSETS/"sounds"/soundfile)
        sounddefs[ev]={"sounds":[{"name":f"{NS}:{soundfile[:-4]}","stream":True}]}
        desc=f'{s["artist"]} - {s["title"]}'
        writejson(DATA/f"{sid}.json",{"comparator_output":1,"description":{"translate":f"jukebox_song.{NS}.{sid}"},"length_in_seconds":s["meta"]["duration"],"sound_event":{"sound_id":f"{NS}:{ev}"}})
        lang[f"item.{NS}.{itemid}"]=f'{s["title"]} ({s["label"]})'
        lang[f"jukebox_song.{NS}.{sid}"]=desc
        writejson(ASSETS/"models"/"item"/f"{itemid}.json",{"parent":"minecraft:item/generated","textures":{"layer0":f"{NS}:item/{itemid}"}})
        writejson(ASSETS/"items"/f"{itemid}.json",{"model":{"type":"minecraft:model","model":f"{NS}:item/{itemid}"}})
        texture(ASSETS/"textures"/"item"/f"{itemid}.png",sid,next(iter(s["games"])))
        java_rows.append((itemid,sid))
        manifest.append({"title":s["title"],"normalized_title":s["key"],"game_label":s["label"],"artist":s["artist"],"item_id":itemid,"jukebox_song_id":sid,"source_file":s["path"].name,"all_source_files":";".join(v["path"].name for v in s["versions"]),"codec":s["meta"]["codec"],"sample_rate":s["meta"]["rate"],"duration_seconds":s["meta"]["duration"],"source_bitrate_kbps":round(s["meta"]["size"]*8/max(s["meta"]["duration"],1)/1000,1),"sha256":s["meta"]["sha256"],"audio_fingerprint":s["meta"]["audio_fingerprint"],"status":"imported"})
    writejson(ASSETS/"sounds.json",sounddefs); writejson(ASSETS/"lang"/"en_us.json",lang)
    writejson(RES/"data"/"minecraft"/"tags"/"item"/"creeper_drop_music_discs.json", {"replace":False,"values":[f"{NS}:{item_id}" for item_id,_ in java_rows]})
    java='''package dev.caribbean.shanties;\n\nimport java.util.ArrayList;\nimport java.util.List;\nimport net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;\nimport net.minecraft.core.Registry;\nimport net.minecraft.core.registries.BuiltInRegistries;\nimport net.minecraft.core.registries.Registries;\nimport net.minecraft.resources.ResourceKey;\nimport net.minecraft.resources.Identifier;\nimport net.minecraft.world.item.CreativeModeTab;\nimport net.minecraft.world.item.ItemStack;\nimport net.minecraft.network.chat.Component;\nimport net.minecraft.world.item.Item;\nimport net.minecraft.world.item.JukeboxSong;\nimport net.minecraft.sounds.SoundEvent;\n\npublic final class ShantyDiscs {\n    private ShantyDiscs() {}\n    public static final List<Item> ALL = new ArrayList<>();\n    private static final ResourceKey<CreativeModeTab> SHANTIES_TAB = ResourceKey.create(Registries.CREATIVE_MODE_TAB, Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, "shanties"));\n    private static final String[][] ENTRIES = {\n'''
    java+=",\n".join(f'        {{"{a}", "{b}"}}' for a,b in java_rows)
    java+='''\n    };\n    public static void initialize() {\n        for (String[] entry : ENTRIES) {\n            String itemPath = entry[0];\n            ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, itemPath));\n            Identifier soundId = Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, "shanty." + entry[1]);
            Registry.register(BuiltInRegistries.SOUND_EVENT, soundId, SoundEvent.createVariableRangeEvent(soundId));
            ResourceKey<JukeboxSong> songKey = ResourceKey.create(Registries.JUKEBOX_SONG, Identifier.fromNamespaceAndPath(CaribbeanShanties.MOD_ID, entry[1]));\n            Item item = Registry.register(BuiltInRegistries.ITEM, itemKey, new Item(new Item.Properties().setId(itemKey).stacksTo(1).jukeboxPlayable(songKey)));\n            ALL.add(item);\n        }\n        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, SHANTIES_TAB, FabricCreativeModeTab.builder()\n                .title(Component.translatable("itemGroup.caribbean_shanties.shanties"))\n                .icon(() -> new ItemStack(ALL.get(0)))\n                .displayItems((parameters, output) -> ALL.forEach(output::accept))\n                .build());\n    }\n}\n'''
    (PROJECT/"src/main/java/dev/caribbean/shanties/ShantyDiscs.java").write_text(java,encoding="utf-8")
    cols=list(manifest[0].keys())
    with (PROJECT/"shanty_manifest.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(manifest)
    print(json.dumps({"source_files":len(files),"unique_songs":len(songs),"duplicate_files_collapsed":len(files)-len(songs),"imported_files":len(list((ASSETS/"sounds"/"shanties").glob("*.ogg"))),"freedom_cry_sources":sum(1 for v in [x for group in groups.values() for x in group] if v["game"]=="freedom_cry"),"manifest":str(PROJECT/"shanty_manifest.csv")},indent=2))

if __name__=="__main__": main()
