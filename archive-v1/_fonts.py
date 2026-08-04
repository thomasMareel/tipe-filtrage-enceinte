import urllib.request, re, os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
url=("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700"
     "&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap")
css=urllib.request.urlopen(urllib.request.Request(url,headers=UA)).read().decode()
os.makedirs('libs/fonts',exist_ok=True)
blocks=re.split(r'(?=/\*)', css)
out=[]
for b in blocks:
    if '@font-face' not in b: continue
    m=re.search(r'/\*\s*([\w-]+)\s*\*/', b)
    if not m or m.group(1)!='latin': continue   # garder seulement le sous-ensemble latin
    fam=re.search(r"font-family:\s*'([^']+)'", b).group(1)
    w=re.search(r'font-weight:\s*(\d+)', b); w=w.group(1) if w else '400'
    st=re.search(r'font-style:\s*(\w+)', b); st=st.group(1) if st else 'normal'
    u=re.search(r'url\((https://[^)]+\.woff2)\)', b)
    if not u: continue
    fn="%s-%s-%s.woff2"%(fam.replace(' ',''),w,st)
    data=urllib.request.urlopen(urllib.request.Request(u.group(1),headers=UA)).read()
    open('libs/fonts/'+fn,'wb').write(data)
    out.append("@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;src:url('%s') format('woff2');}"%(fam,st,w,fn))
open('libs/fonts/fonts.css','w',encoding='utf-8').write("\n".join(out)+"\n")
print("polices locales :",len(out),"fichiers woff2")
