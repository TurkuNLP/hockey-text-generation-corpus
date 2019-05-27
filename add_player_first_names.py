import json
import sys
import re

def find_match(occ,references):
    occ_parts=occ.split()
    if len(occ_parts)==1: #just a surname
        matches=set(m for m in references if m.endswith(occ_parts[0]))
    else: #more than that
        matches=set(m for m in references if m.endswith(occ_parts[-1]) and m.startswith(occ_parts[0]))
    matches=sorted(matches,key=lambda m: len(m), reverse=True)
    return matches[0]
    #print(occ, " ----> ", ", ".join(matches))

def norm_name(n):
    parts=n.strip().split()
    if None in parts:
        print("WTF:",parts, file=sys.stderr)

    if len(parts)==1:
        #no first name
        pass
    elif len(parts)==2:
        #first last
        pass
    else:
        #whoa - more than two
        if len(parts[-1])==1 or sum(1 for c in parts[-1] if c.isupper())>1 or parts[-1].endswith(".") or parts[-1]=="Erä":
            parts=parts[:-1]
            print("PARTS",parts,file=sys.stderr)
        if len(parts[0])==1 or sum(1 for c in parts[0] if c.isupper())>1:
            parts=parts[1:]
        if len(parts)>2:
            print("WHOA",n,file=sys.stderr)
            print(file=sys.stderr)
    return " ".join(parts)
    

def all_names_into_map(names):
    name_map={}
    clean_names=set()
    for n in names:
        clean_names.add(norm_name(n))
    for c in clean_names:
        name_map[c]=find_match(c,clean_names)
    return name_map
            

def fix(s):
    s=s.replace("PesonenIlkka","Pesonen, Ilkka")
    s=s.replace("DamonSakari", "Damon, Sakari")
    s=s.replace("nagander","Nagander")
    s=s.replace("Nielikäinen Teemu Virkkunen","Nielikäinen, Teemu Virkkunen")
    s=s.replace("Matti Kuusisto Matt","Matti Kuusisto, Matt")
    s=s.replace("Fandul Jari Korpisalo","Fandul, Jari Korpisalo")
    s=s.replace("Da costa","Da Costa")
    s=s.replace("Tapanilan","")
    return s
            
data=json.load(sys.stdin)

for game in data.values():
    all_names=set()
    for ev in game["events"]:
        if ev.get("Player") and ev.get("Player")!="None":
            for n in re.split(r",| ja ",fix(ev.get("Player"))):
                all_names.add(n.strip())
        if ev.get("Assist") and ev.get("Assist")!="None":
            for n in re.split(r",| ja ",fix(ev.get("Assist"))):
                all_names.add(n.strip())
    name_map=all_names_into_map(all_names)
    for ev in game["events"]:
        if ev.get("Player"):
            exp_players=[]
            for n in re.split(r",| ja ",fix(ev.get("Player"))):
                exp_players.append(name_map.get(norm_name(n.strip()),norm_name(n.strip())))
            if "Kaipainen" in exp_players:
                print(game["events"],file=sys.stderr)
            ev["Player_fullname"]=", ".join(exp_players)
            print(ev["Player"],"   --->   ",ev["Player_fullname"],file=sys.stderr)

        if ev.get("Assist"):
            exp_players=[]
            for n in re.split(r",| ja ",fix(ev.get("Assist"))):
                exp_players.append(name_map.get(norm_name(n.strip()),norm_name(n.strip())))
            ev["Assist_fullname"]=", ".join(exp_players)
            print(ev["Assist"],"   --->   ",ev["Assist_fullname"],file=sys.stderr)

s=json.dumps(data,ensure_ascii=False,indent=2)
print(s)
        
        
