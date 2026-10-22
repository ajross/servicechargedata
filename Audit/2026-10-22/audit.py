"""Read-only source-to-output audit. Writes reports only; no dataset edits."""
import csv,json,re,zipfile,xml.etree.ElementTree as ET,posixpath,subprocess,hashlib
from pathlib import Path
from decimal import Decimal,InvalidOperation,ROUND_HALF_UP
from collections import defaultdict,Counter
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).parent
issues=[];stats=defaultdict(Counter); ledger=[];source_ids=defaultdict(lambda:defaultdict(set));source_names=defaultdict(lambda:defaultdict(set))
def norm(s):return re.sub(r'[^a-z0-9]','',str(s).lower())
def num(s):
 s=str(s or '').strip().replace(',','').replace('£','').replace('�','')
 if s.upper() in ('','NULL','N/A','#N/A'):return Decimal(0)
 if s.startswith('(') and s.endswith(')'):s='-'+s[1:-1]
 return Decimal(s)
def read(p,skip=0):
 p=Path(p); data=p.read_bytes()
 try:text=data.decode('utf-8-sig')
 except UnicodeDecodeError:text=data.decode('cp1252')
 rr=csv.reader(text.splitlines());rows=list(rr)[skip:];h=[x.strip() for x in rows[0]]
 return [dict(zip(h,r))|{'_ref':str(p.relative_to(ROOT))+f':{n+skip+2}'} for n,r in enumerate(rows[1:]) if any(x.strip() for x in r)]
def issue(file,key,field,actual,expected,ref,kind='difference'):
 issues.append(dict(file=str(file),key=str(key),field=field,actual=str(actual),expected=str(expected),source=str(ref),kind=kind))
def check(file,row,field,expected,ref,numeric=True,noise=False):
 stats[str(file)]['checks']+=1; a=row.get(field,'<MISSING>')
 try:equal=num(a)==num(expected) if numeric else norm(a)==norm(expected)
 except (InvalidOperation,ValueError):equal=False
 if not equal and noise:
  try:equal=abs(num(a)-num(expected))<Decimal('0.000001')
  except:pass
  if equal:stats[str(file)]['excel_noise']+=1
 if not equal:issue(file,row.get('Block_ID',row.get('Mapsite_ID',row.get('Estate_ID',''))),field,a,expected,ref)
 else:stats[str(file)]['matched']+=1
 if numeric and str(expected).strip().upper() in ('','NULL'):stats[str(file)]['blank_to_zero']+=1
 ledger.append((str(file),row.get('Block_ID',row.get('Mapsite_ID',row.get('Estate_ID',''))),field,ref))
def index(rows,field):
 d=defaultdict(list)
 for row in rows:d[norm(row.get(field,''))].append(row)
 return d
def join(file,row,idx,key):
 candidates=idx.get(norm(key),[])
 if len(candidates)!=1:
  issue(file,row.get('Block_ID',row.get('Mapsite_ID','')), 'source join',key,f'{len(candidates)} exact normalized candidates','', 'ambiguous_join' if candidates else 'source_gap');return None
 return candidates[0]
def xlsx(path):
 z=zipfile.ZipFile(path);ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 strings=[]
 if 'xl/sharedStrings.xml' in z.namelist():strings=[''.join(t.text or '' for t in si.iter('{'+ns['m']+'}t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
 rel={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))};result={}
 for sh in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',ns):
  target=rel[sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
  raw=[]
  for rr in ET.fromstring(z.read(target)).findall('m:sheetData/m:row',ns):
   row={}
   for c in rr.findall('m:c',ns):
    v=c.find('m:v',ns);s=v.text if v is not None else ''.join(c.find('m:is',ns).itertext()) if c.find('m:is',ns) is not None else ''
    if c.attrib.get('t')=='s':s=strings[int(s)]
    row[re.sub(r'\d','',c.attrib['r'])]=s
   raw.append((rr.attrib['r'],row))
  head=raw[0][1] if raw else {};result[sh.attrib['name']]=[{head.get(k,k).strip():v for k,v in row.items()}|{'_ref':str(path.relative_to(ROOT))+':'+sh.attrib['name']+'!'+n} for n,row in raw[1:]]
 return result
annual={};lookups={}
for borough in ['Lambeth','Lewisham','Southwark','Tower Hamlets','Wandsworth']:
 lookups[borough]={k:read(ROOT/borough/'Lookups'/f'{k}.csv') for k in ['blocks','estates']+(['mapsites'] if borough=='Tower Hamlets' else [])}
 for p in sorted((ROOT/borough).glob('*/*.csv')):
  if not re.fullmatch(r'\d{4}-\d{4}',p.parent.name) or (p.stem!=p.parent.name and p.name!='mapsites.csv'):continue
  rel=str(p.relative_to(ROOT));rows=read(p);annual[rel]=rows;stats[rel]['rows']=len(rows)
  seen=set();bs={(r['Estate_ID'],r['Block_ID']):r for r in lookups[borough]['blocks']};es={r['Estate_ID']:r for r in lookups[borough]['estates']};ms={r['Mapsite_ID']:r for r in lookups[borough].get('mapsites',[])}
  for row in rows:
   key=(row.get('Estate_ID'),row.get('Block_ID',row.get('Mapsite_ID')))
   if key in seen:issue(rel,key,'identity','duplicate','unique',row['_ref'],'structural')
   seen.add(key)
   for k,v in row.items():
    if k=='_ref':continue
    if not v.strip():issue(rel,key,k,'blank','complete',row['_ref'],'structural')
   check(rel,row,'Year_Start',p.parent.name[:4],row['_ref']);check(rel,row,'Year_End',p.parent.name[5:],row['_ref'])
   if 'Block_ID' in row:
    b=bs.get(key);e=es.get(row['Estate_ID'])
    if b:check(rel,row,'Block_Name',b['Block_Name'],b['_ref'],False)
    else:issue(rel,key,'lookup','missing','present','','structural')
    if e:check(rel,row,'Estate_Name',e['Estate_Name'],e['_ref'],False)
    else:issue(rel,key,'estate lookup','missing','present','','structural')
   if 'Mapsite_ID' in row:
    m=ms.get(row['Mapsite_ID'])
    if m:check(rel,row,'Mapsite_Name',m['Mapsite_Name'],m['_ref'],False)
    else:issue(rel,key,'mapsite lookup','missing','present','','structural')
# Lewisham: rebuild pivot independently, validate every cost including absent-service zeros.
b='Lewisham';path=next((ROOT/b).glob('*/Original Data/*.csv'));raw=read(path);groups=defaultdict(list)
for r in raw:groups[(r['sc_schid'].strip(),r['sc_grpid'].strip())].append(r)
services={}
for r in raw:
 label=' '.join(r['sc_serv_desc'].split());col=label.title().replace(' ','_').replace('(','').replace(')','')
 services[label]=col
print('LEWISHAM SERVICES',services)
# Explicit source-label mappings are audited, not inferred from output values.
services.update({**{k:v.replace('Tech_Repairs','Technical_Repairs') for k,v in services.items()}, 'CARETAKING LEV 2':'Caretaking_Level_2','TEC REPAIRS CENT HTG ONLY':'Technical_Repairs_Central_Heating_Only','WINCL':'Window_Cleaning','TECHNICAL REPAIRS (CENTRAL HEATING ONLY)':'Technical_Repairs_Central_Heating_Only'})
for row in annual[b+'/2022-2023/2022-2023.csv']:
 g=groups.get((row['Estate_ID'],row['Block_ID']),[]); costs=defaultdict(list)
 for r in g:costs[services[' '.join(r['sc_serv_desc'].split())]].append(r)
 if not g:issue(b,row['Block_ID'],'group','absent','present','','source_gap');continue
 for field,sourcefield in [('Estate_Name','sc_schname'),('Block_Name','sc_grpdesc'),('Property_Count','propcnt')]:
  for r in g:check(b+'/2022-2023/2022-2023.csv',row,field,r[sourcefield],r['_ref'],field=='Property_Count')
 for col in list(row)[7:]:
  if col=='_ref':continue
  rs=costs.get(col,[]);vals={num(r['actual cost']) for r in rs}
  if len(vals)>1:issue(b,row['Block_ID'],col,row[col],str(vals),'|'.join(r['_ref'] for r in rs),'source_conflict')
  check(b+'/2022-2023/2022-2023.csv',row,col,next(iter(vals)) if vals else 0,'|'.join(r['_ref'] for r in rs) or 'absent source service')
 for r in g:source_ids[b]['blocks'].add((r['sc_schid'].strip(),r['sc_grpid'].strip()));source_ids[b]['estates'].add(r['sc_schid'].strip())
# Southwark numeric columns direct position, independent of ID assignments.
b='Southwark';src=ROOT/b/'2022-2023/Original Data';br=read(next(src.glob('*Block*.csv')),2);er=read(next(src.glob('*Estate*.csv')),2);bi=index(br,'Block');ei=index(er,'Estate');book=xlsx(next(src.glob('*.xlsx')))['Summary'];links=defaultdict(set)
for x in book:links[norm(x.get('Block_Name',''))].add(norm(x.get('Estate_Name','')))
for row in annual[b+'/2022-2023/2022-2023.csv']:
 f=b+'/2022-2023/2022-2023.csv';r=join(f,row,bi,row['Block_Name'])
 if r:
  for dst,srcfield in zip(['Block_Bed_Weighting']+[k for k in row if k.startswith('Block_') and k not in ['Block_ID','Block_Name','Block_Bed_Weighting']],list(br[0])[1:-1]):check(f,row,dst,r[srcfield],r['_ref'])
 candidates=links[norm(row['Block_Name'])]
 if candidates and norm(row['Estate_Name']) not in candidates:issue(f,row['Block_ID'],'Estate_Name',row['Estate_Name'],str(candidates),'Templer attachment.xlsx','mapping_difference')
 if not candidates:issue(f,row['Block_ID'],'estate mapping',row['Estate_Name'],'no exact source-book block match','Templer attachment.xlsx','mapping_gap')
 r=join(f,row,ei,row['Estate_Name']) if norm(row['Estate_Name']) in ei else None
 for dst,srcfield in zip(['Estate_Bed_Weighting','Estate_Care_and_Upkeep','Estate_Grounds_Maintenance','Estate_Lighting','Estate_Repairs_and_Maintenance'],list(er[0])[1:-1]):check(f,row,dst,r[srcfield] if r else 0,r['_ref'] if r else 'no estate charge record')
# Wandsworth exact estate + reconstructed address range; retain duplicate ambiguity.
b='Wandsworth';src=ROOT/b/'2023-2024/Original Data';br=read(next(src.glob('*Block*')));er=read(next(src.glob('*Estate*')));bi=defaultdict(list);ei=index(er,'ESTATE')
for r in br:bi[(norm(r['ESTATE']),norm(r['BLOCK']+', '+r['PROP']))].append(r)
for row in annual[b+'/2023-2024/2023-2024.csv']:
 f=b+'/2023-2024/2023-2024.csv';rs=bi.get((norm(row['Estate_Name']),norm(row['Block_Name'])),[])
 if not rs:
  rs=[x for x in br if norm(x['BLOCK']+', '+x['PROP'])==norm(row['Block_Name'])]
  if len(rs)==1:issue(f,row['Block_ID'],'estate spelling',row['Estate_Name'],rs[0]['ESTATE'],rs[0]['_ref'],'name_normalization')
 if len(rs)!=1:issue(f,row['Block_ID'],'block join',row['Block_Name'],f'{len(rs)} source matches','','source_gap');continue
 r=rs[0]
 for dst,sf in zip(['Block_Property_Count','Block_Grounds_Maintenance','Block_Tree_Maintenance','Block_Communal_Electricity','Block_Lift_Electricity','Block_Repairs_and_Maintenance','Block_Lift_Repairs','Block_Cleaning','Block_Paladins'],['RES','GARDENING','TREES','BLOCK ELECTRIC','LIFT ELECTRIC','BLOCK REPAIRS','LIFT REPAIRS','CLEANING','PALADINS']):check(f,row,dst,r[sf],r['_ref'])
 check(f,row,'Block_Property_Type',{'Y':'Flats','H':'Houses','':'Unknown'}.get(r['FLATS'],r['FLATS']),r['_ref'],False)
 es=ei.get(norm(row['Estate_Name']),[]);e=es[0] if len(es)==1 else None
 for dst,sf in zip(['Estate_Flat_Count','Estate_House_Count','Estate_Grounds_Maintenance','Estate_Tree_Maintenance','Estate_Communal_Electricity','Estate_Repairs_and_Maintenance','Estate_Cleaning'],['FLATS','HOUSES','GARDEN MAINTENANCE','TREES','ELECTRICITY','ESTATE REPAIRS','CLEANING']):check(f,row,dst,e[sf] if e else 0,e['_ref'] if e else 'no estate source record')
# Tower Hamlets: independently read cached workbook XML, not an annual-derived model.
b='Tower Hamlets';book=xlsx(next((ROOT/b).glob('2022-2023/Original Data/*.xlsx')));bl=index(book['Block'],'Block');mi=index(book['Mapsite'],'Mapsite');bo=index(book['Boiler'],'Block Name')
service={'Block_Repairs':'Block Repairs','Boiler_Repairs':'Boiler Repairs','Block_Lift_Repairs':'Lift Repairs','Block_Door_Entry_System_Repairs':'Door Entry System Repairs','Block_TV_Aerial_Repairs':'TV Aerial Repairs','Block_Caretaking':'Block Caretaking','Block_Bin_Hire':'Bin Hire','Boiler_Fuel':'Boiler Fuel','Block_Communal_Electricity':'Communal Electricity','Block_Concierge_Service':'Concierge Service','Block_Pest_Control_Service':'Pest Control Service','Block_Resident_Engagement_Service':'Resident Engagement Service','Block_Customer_Access':'Customer Access','Block_Antisocial_Behaviour_Service':'Antisocial Behaviour Service','Block_TMO_Housing_Management_Service':'TMO Housing Management Service','Block_Building_Insurance_Total':'Building Insurance Total'}
mapservice={'Mapsite_Repairs':'Estate Repairs','Mapsite_Caretaking':'Estate Caretaking','Mapsite_Grounds_Maintenance':'Grounds Maintenance','Mapsite_Bulk_Waste':'Bulk Waste'}
for year in ['2022-2023','2023-2024']:
 if year=='2023-2024':
  src=ROOT/b/year/'Original Data';bl=index(read(next(src.glob('*block*'))),'Block');mi=index(read(next(src.glob('*mapsite*'))),'Estate (Mapsite)')
 for typ in ['main','mapsites']:
  f=f'{b}/{year}/{year if typ=="main" else "mapsites"}.csv'
  for row in annual[f]:
   if typ=='main':
    r=join(f,row,bl,row['Block_Name'] if year=='2022-2023' else row['Block_ID'])
    if r:
     for dst,sf in service.items():check(f,row,dst,r.get(sf,''),r['_ref'],noise=year=='2022-2023')
     for dst,sf in [('Block_GRV','Block GRV' if year=='2022-2023' else 'Total GV'),('Block_Property_Count' if year=='2022-2023' else 'Block_Leasehold_Property_Count','No. of Properties' if year=='2022-2023' else 'Count of Properties')]:check(f,row,dst,r[sf],r['_ref'])
     check(f,row,'Leasehold_Management_Per_Property' if year=='2022-2023' else 'Leasehold_Management_Total',r.get('Leasehold Management (flat rate charge to all leaseholders)' if year=='2022-2023' else 'Leasehold Management',''),r['_ref'],noise=True)
     if year=='2022-2023':
      check(f,row,'Mapsite_Name',r['Mapsite'],r['_ref'],False);check(f,row,'Estate_Name',r['Estate'],r['_ref'],False)
      boilers=bo.get(norm(row['Block_Name']),[])
      if len(boilers)==1:
       br=boilers[0]
       for dst,sf in [('Boiler_Name','Boiler Name'),('Boiler_Total_Points','Boiler Total Boiler Points'),('Block_Boiler_Points','Boiler Points')]:check(f,row,dst,br.get(sf,''),br['_ref'],dst!='Boiler_Name',True)
      elif not boilers:
       check(f,row,'Boiler_Total_Points',0,'no Boiler-tab record');check(f,row,'Block_Boiler_Points',0,'no Boiler-tab record')
   mr=join(f,row,mi,row['Mapsite_Name'] if year=='2022-2023' else row['Mapsite_ID'])
   if mr:
    for dst,sf in mapservice.items():check(f,row,dst,mr.get(sf,''),mr['_ref'],noise=year=='2022-2023')
    check(f,row,'Mapsite_GRV',mr['Mapsite GRV' if year=='2022-2023' else 'Total GV'],mr['_ref'])
    check(f,row,'Mapsite_Property_Count' if year=='2022-2023' else 'Mapsite_Leasehold_Property_Count',mr['No. of Properties' if year=='2022-2023' else 'Count of Properties'],mr['_ref'])
# Lambeth raw service mappings follow the council headings, not column positions in outputs.
b='Lambeth';base=ROOT/b
blockcols=['Block_Boiler_Repairs_and_Maintenance','Block_CCTV','Block_Cleaning','Block_Communal_Electricity','Block_Communal_Electrical_Maintenance','Block_TV_Aerial','Block_Communal_Water_Quality','Block_Communal_Window_Cleaning','Block_Communal_Ventilation_Maintenance','Block_Concierge','Block_Disinfestation','Block_Dry_Riser','Block_Door_Entry_System','Block_Ext_Cleaning','Block_Ext_Grounds_Maintenance','Block_Ext_External_Tree_Maintenance','Block_Ext_Repairs_and_Maintenance','Block_Fire_Ventilation_Maintenance','Block_Repairs_and_Maintenance','Block_Lift_Services_and_Repairs','Block_Lightning_Protection']
estcols=['Estate_CCTV','Estate_Cleaning','Estate_Communal_Electricity','Estate_Repairs_and_Maintenance','Estate_Grounds_Maintenance','Estate_Tree_Maintenance']
lambethraw=[]
for year in ['2023-2024','2024-2025']:
 src=base/year/'Original Data';br=read(next(src.glob('*Block*')));er=read(next(src.glob('*Estate*')))
 bcode='Block Code';ecode='Estate Code' if year=='2023-2024' else 'Esate Code';bi=index(br,bcode);bn=index(br,'Block');ei=index(er,'Estate Code')
 if year=='2023-2024':
  sc=['BOIREPMTNB Aun','CCTVB Aun','CLEANING Aun','COMMELEC Aun','COMMELMNTB Aun','COMMTVAR Aun','COMMWATER Aun','COMMWINCN Aun','COMVENTMNT Aun','CONCIERG Aun','DISINFEST Aun','DRYRISER Aun','ENTRYPHO Aun','EXTCLEANB Aun','EXTGRSMTNB Aun','EXTREEMNTB Aun','EXTREPMTNB Aun','FIREVENTMT Aun','GENMNTBK Aun','LIFTSEREPB Aun','LIGHTNGPRO Aun'];ec=['CCTVE Aun','CLEANEST Aun','COMMELECE Aun','GENMNTES Aun','GROUNDMNTE Aun','TREEMNTEST Aun']
 else:sc=list(br[0])[5:26];ec=['CCTV','Estate Cleaning','Estate Communal Electricity','Estate Repairs & Maintenance','Estate Grounds Maintenance','Estate Tree Maintenance']
 f=f'{b}/{year}/{year}.csv';used=set()
 for row in annual[f]:
  idx=bi if norm(row['Block_ID']) in bi else bn;key=row['Block_ID'] if idx is bi else row['Block_Name'];r=join(f,row,idx,key)
  if r:
   used.add(r['_ref']);check(f,row,'Block_RV',r['Blk RV'],r['_ref'])
   for dst,sf in zip(blockcols,sc):check(f,row,dst,r[sf],r['_ref'])
   if r[ecode] and r[ecode]!=row['Estate_ID']:issue(f,row['Block_ID'],'Estate_ID',row['Estate_ID'],r[ecode],r['_ref'],'mapping_override')
  es=ei.get(norm(row['Estate_ID']),[])
  e=es[0] if len(es)==1 else None
  if len(es)>1:issue(f,row['Estate_ID'],'estate source','multiple',len(es),'','ambiguous_join')
  check(f,row,'Estate_RV',e['Est RV'] if e else 0,e['_ref'] if e else 'no matching estate source ID')
  for dst,sf in zip(estcols,ec):check(f,row,dst,e[sf] if e else 0,e['_ref'] if e else 'no matching estate source ID')
 for r in br:
  if not r.get('Block Code') and not r.get('Block'):continue
  lambethraw.append(r)
  if r['_ref'] not in used:issue(f,r.get(bcode),'source block coverage',r.get('Block'),'not retained',r['_ref'],'source_not_represented')
# PDF rows: numeric tokens anchored at the right avoid shifting service columns.
def pdfrows(file,n):
 text=subprocess.check_output(['pdftotext','-layout',str(file),'-'],text=True);out=[]
 for line_num,line in enumerate(text.splitlines(),1):
  tokens=list(re.finditer(r'(?<!\S)-?\d[\d,]*(?:\.\d+)?(?!\S)',line))
  if len(tokens)<n:continue
  tail=tokens[-n:];prefix=line[:tail[0].start()].strip();names=re.split(r'\s{2,}',prefix)
  if not prefix:continue
  out.append({'name':names[0],'estate':names[1] if len(names)>1 else '', 'values':[m.group() for m in tail],'_ref':str(file.relative_to(ROOT))+f':text-line-{line_num}'})
 return out
pb=pdfrows(base/'2022-2023/Original Data/Block.pdf',22);pe=pdfrows(base/'2022-2023/Original Data/Estate.pdf',7)
print('PDF parsed',len(pb),len(pe))
bi=index(pb,'name');ei=index(pe,'name');used=set();f='Lambeth/2022-2023/2022-2023.csv'
legacybase=Path('/home/ai-ajross/projects/ServiceChargerator/public');legacyblocks=list(csv.DictReader((legacybase/'blocks.csv').open()));legacynames={r['ID']:r['Block_Name'] for r in legacyblocks}
for row in annual[f]:
 matches=bi.get(norm(row['Block_Name']),[]) or bi.get(norm(legacynames.get(row['Block_ID'],'')),[])
 if len(matches)==1:
  r=matches[0];used.add(r['_ref']);check(f,row,'Block_RV',r['values'][0],r['_ref'])
  for dst,val in zip(blockcols,r['values'][1:]):check(f,row,dst,val,r['_ref'])
 else:issue(f,row['Block_ID'],'PDF block join',row['Block_Name'],f'{len(matches)} exact normalized name candidates','Block.pdf','source_gap')
 matches=ei.get(norm(row['Estate_Name']),[])
 if len(matches)==1:
  r=matches[0];check(f,row,'Estate_RV',r['values'][0],r['_ref'])
  for dst,val in zip(estcols,r['values'][1:]):check(f,row,dst,val,r['_ref'])
 elif row['Estate_ID']!='EX01':issue(f,row['Estate_ID'],'PDF estate join',row['Estate_Name'],f'{len(matches)} name candidates','Estate.pdf','source_gap')
for r in pb:
 if r['_ref'] not in used:issue(f,r['name'],'source PDF coverage','not matched','annual row',r['_ref'],'source_not_represented')
# Earlier years: retained legacy export is corroboration, never independent council evidence.
legacy=list(csv.DictReader((legacybase/'charges.csv').open()));li=defaultdict(list)
for x in legacy:li[(x['Year_Start'],x['Block_ID'])].append(x)
for f,rows in annual.items():
 if not f.startswith('Lambeth/') or int(rows[0]['Year_Start'])>=2022:continue
 for row in rows:
  rs=li.get((row['Year_Start'],row['Block_ID']),[])
  if len(rs)==1:
   for col in blockcols+estcols:check(f,row,col,rs[0][col],'ServiceChargerator/public/charges.csv (legacy transformed export)')
  else:issue(f,row['Block_ID'],'legacy match',len(rs),'one legacy row','','source_gap')
 issue(f,'all','primary source availability','no original council file retained','independent source needed','','evidence_gap')
# Lookup-to-source audit. Synthetic IDs require source-backed names/relationships, not council-ID equality.
for borough,tables in lookups.items():
 for typ,rows in tables.items():
  field={'blocks':'Block','estates':'Estate','mapsites':'Mapsite'}[typ];seen=set();annualkeys=set()
  relevant=[r for f,rs in annual.items() if f.startswith(borough+'/') for r in rs if field+'_ID' in r]
  for r in relevant:annualkeys.add((r.get('Estate_ID'),r[field+'_ID']) if typ=='blocks' else r[field+'_ID'])
  for r in rows:
   key=(r.get('Estate_ID'),r[field+'_ID']) if typ=='blocks' else r[field+'_ID'];f=f'{borough}/Lookups/{typ}.csv'
   if key in seen:issue(f,key,'identity','duplicate','unique',r['_ref'],'structural')
   seen.add(key)
   if key not in annualkeys:issue(f,key,'lookup coverage','no annual use','annual use',r['_ref'],'lookup_only')
   if typ=='blocks' and r['Estate_ID'] not in {e['Estate_ID'] for e in tables['estates']}:issue(f,key,'estate FK',r['Estate_ID'],'valid estate',r['_ref'],'structural')
   if borough=='Lewisham':
    rs=groups.get((r.get('Estate_ID'),r.get('Block_ID')),[]) if typ=='blocks' else [x for x in raw if x['sc_schid'].strip()==r['Estate_ID']]
    values={norm(x['sc_grpdesc' if typ=='blocks' else 'sc_schname']) for x in rs}
    if norm(r[field+'_Name']) not in values:issue(f,key,'source name',r[field+'_Name'],str(values),'Actuals22 23.csv','lookup_source_difference')
   elif borough=='Lambeth':
    if typ=='blocks':
     rs=[x for x in lambethraw if x.get('Block Code')==r['Block_ID']]
     if not rs:issue(f,key,'council code evidence',r['Block_ID'],'not present in retained ID-bearing originals','2023/2024 source CSVs','lookup_evidence_gap')
     elif norm(r['Block_Name']) not in {norm(x['Block']) for x in rs}:issue(f,key,'source name',r['Block_Name'],' | '.join({x['Block'] for x in rs}),'2023/2024 source CSVs','lookup_name_variant')
# Independent lookup relationship checks for the synthetic-ID boroughs.
for borough in ['Southwark','Wandsworth','Tower Hamlets']:
 tables=lookups[borough];est={r['Estate_ID']:r['Estate_Name'] for r in tables['estates']}
 if borough=='Southwark':
  source=xlsx(next((ROOT/borough).glob('*/Original Data/*.xlsx')))['Summary']; names={norm(x.get('Estate_Name','')) for x in source}
  names|={norm(x.get('Estate','')) for x in read(next((ROOT/borough).glob('*/Original Data/*Estate*.csv')),2)}
 elif borough=='Wandsworth':
  src=ROOT/borough/'2023-2024/Original Data'; source=read(next(src.glob('*Block*')));names={norm(x['ESTATE']) for x in source}|{norm(x['ESTATE']) for x in read(next(src.glob('*Estate*')))}
 else:
  source=xlsx(next((ROOT/borough).glob('2022-2023/Original Data/*.xlsx'))); names={norm(x.get('Estate','')) for x in source['Estate']+source['Mapsite']+source['Block']}
 for r in tables['estates']:
  if norm(r['Estate_Name']) not in names and r['Estate_Name']!='Unassigned estate':
   issue(f'{borough}/Lookups/estates.csv',r['Estate_ID'],'estate name evidence',r['Estate_Name'],'no exact normalized original name',r['_ref'],'lookup_name_variant')
 if borough=='Tower Hamlets':
  blocks=index(source['Block'],'Block'); maps=index(source['Mapsite'],'Mapsite'); knowncodes={x['Block'] for x in read(next((ROOT/borough).glob('2023-2024/Original Data/*block*')))}
  for r in tables['blocks']:
   rs=blocks.get(norm(r['Block_Name']),[])
   if len(rs)==1:
    if norm(est[r['Estate_ID']])!=norm(rs[0]['Estate']):issue('Tower Hamlets/Lookups/blocks.csv',r['Block_ID'],'estate relationship',est[r['Estate_ID']],rs[0]['Estate'],rs[0]['_ref'],'lookup_source_difference')
    ml={x['Mapsite_ID']:x['Mapsite_Name'] for x in tables['mapsites']}
    if norm(ml.get(r['Mapsite_ID']))!=norm(rs[0]['Mapsite']):issue('Tower Hamlets/Lookups/blocks.csv',r['Block_ID'],'mapsite relationship',ml.get(r['Mapsite_ID']),rs[0]['Mapsite'],rs[0]['_ref'],'lookup_source_difference')
   else:issue('Tower Hamlets/Lookups/blocks.csv',r['Block_ID'],'cross-year relationship evidence',r['Block_Name'],'code present in 2023 but no exact full-address 2022 match' if r['Block_ID'] in knowncodes else 'no unique full-address match','','lookup_evidence_gap')
  for r in tables['mapsites']:
   if norm(r['Mapsite_Name']) not in maps:issue('Tower Hamlets/Lookups/mapsites.csv',r['Mapsite_ID'],'mapsite full name evidence',r['Mapsite_Name'],'2023 code only; no 2022 name match','','lookup_evidence_gap')
# Source observations excluded from denormalized tables: retain for review, do not silently discard.
for borough in ['Southwark','Wandsworth']:
 path=next((ROOT/borough).glob('*/Original Data/*Estate*.csv')); er=read(path,2 if borough=='Southwark' else 0)
 outnames={norm(r['Estate_Name']) for f,rs in annual.items() if f.startswith(borough+'/') for r in rs if 'Estate_Name' in r}
 for r in er:
  name=r.get('Estate',r.get('ESTATE',''))
  if norm(name) not in outnames and norm(name)!='total':issue(str(path.relative_to(ROOT)),name,'source estate coverage',name,'not used under exact name',r['_ref'],'source_not_represented')
# Audit metadata with intentionally unavailable source-year fields, and historical RV carry-back.
for f,rows in annual.items():
 if f.startswith('Tower Hamlets/'):
  for r in rows:
   year=r['Year_Start']
   for col in (['Mapsite_Leasehold_Property_Count','Block_Leasehold_Property_Count','Leasehold_Management_Total'] if year=='2022' else ['Mapsite_Property_Count','Block_Property_Count','Boiler_Total_Points','Block_Boiler_Points','Leasehold_Management_Per_Property']):
    if col in r:check(f,r,col,0,'not supplied in this source year')
   if 'Boiler_Name' in r and (year=='2023' or r['Boiler_Total_Points']=='0.00'):
    check(f,r,'Boiler_Name','Not supplied','no source boiler entry',False)
 if f.startswith('Lambeth/') and int(rows[0]['Year_Start'])<2022:
  later=[x for ff,rr in annual.items() if ff.startswith('Lambeth/') and int(rr[0]['Year_Start'])>=2022 for x in rr]
  for r in rows:
   for kind in ['Block','Estate']:
    candidates=[x for x in later if x[kind+'_ID']==r[kind+'_ID']]
    if candidates:
     first=min(candidates,key=lambda x:x['Year_Start']);check(f,r,kind+'_RV',first[kind+'_RV'],'oldest retained annual RV carry-back; NOT contemporary council evidence')
# Human-review candidates for unresolved Southwark aliases, never automatically accepted.
import difflib
source=xlsx(next((ROOT/'Southwark').glob('*/Original Data/*.xlsx')))['Summary'];sourceblocks={x.get('Block_Name',''):x.get('Estate_Name','') for x in source}
with (OUT/'southwark-mapping-review.csv').open('w',newline='') as out:
 w=csv.writer(out);w.writerow(['block_id','block_name','current_estate','candidate_source_block','candidate_source_estate','similarity_not_proof'])
 names=list(sourceblocks)
 for i in issues:
  if i['kind']!='mapping_gap':continue
  r=next(x for x in annual['Southwark/2022-2023/2022-2023.csv'] if x['Block_ID']==i['key'])
  choices=sorted(names,key=lambda n:difflib.SequenceMatcher(None,norm(r['Block_Name']),norm(n)).ratio(),reverse=True)[:3]
  for choice in choices:w.writerow([r['Block_ID'],r['Block_Name'],r['Estate_Name'],choice,sourceblocks[choice],round(difflib.SequenceMatcher(None,norm(r['Block_Name']),norm(choice)).ratio(),4)])
# Estate PDF coverage and source-origin anomalies, independent of block-row output.
output_estates={norm(r['Estate_Name']) for r in annual['Lambeth/2022-2023/2022-2023.csv']}
for r in pe:
 if norm(r['name']) not in output_estates:issue('Lambeth/2022-2023/2022-2023.csv',r['name'],'source estate PDF coverage','no annual estate row','source estate exists',r['_ref'],'source_not_represented')
with (OUT/'source-precision.csv').open('w',newline='') as out:
 w=csv.writer(out);w.writerow(['file','csv_record','block_id','estate_id','field','value'])
 for f,rows in annual.items():
  if not f.startswith('Lambeth/2024-2025/'):continue
  for r in rows:
   for k,v in r.items():
    if not (k.startswith('Block_') or k.startswith('Estate_')) or k.endswith(('_ID','_Name','_RV')):continue
    d=num(v)
    if d!=d.quantize(Decimal('.01')):w.writerow([f,r['_ref'].rsplit(':',1)[-1],r['Block_ID'],r['Estate_ID'],k,v])
# These are source count inconsistencies, not values altered by transformation.
wrows=annual['Wandsworth/2023-2024/2023-2024.csv'];wg=defaultdict(list)
for r in wrows:wg[r['Estate_ID']].append(r)
with (OUT/'wandsworth-count-reconciliation.csv').open('w',newline='') as out:
 w=csv.writer(out);w.writerow(['estate_id','estate_name','source_estate_flats','source_estate_houses','sum_block_flats','sum_block_houses','difference_flats','difference_houses'])
 for key,rs in wg.items():
  flats=sum(num(r['Block_Property_Count']) for r in rs if r['Block_Property_Type']=='Flats');houses=sum(num(r['Block_Property_Count']) for r in rs if r['Block_Property_Type']=='Houses');ef=num(rs[0]['Estate_Flat_Count']);eh=num(rs[0]['Estate_House_Count'])
  if ef!=flats or eh!=houses:w.writerow([key,rs[0]['Estate_Name'],ef,eh,flats,houses,flats-ef,houses-eh])
# Test the checker on deliberate in-memory faults, never on the repository data.
saved=(len(issues),len(ledger));oldstats=stats.copy()
check('__checker_test__',{'Block_ID':'T','amount':'1.01'},'amount','1.00','deliberate one-penny fault')
assert len(issues)==saved[0]+1 and issues[-1]['kind']=='difference'
check('__checker_test__',{'Block_ID':'T','amount':'-1.00'},'amount','1.00','deliberate sign fault')
assert len(issues)==saved[0]+2
check('__checker_test__',{'Block_ID':'T','amount':'0.00'},'amount','','allowed blank substitution')
assert len(issues)==saved[0]+2
issues[saved[0]:]=[];ledger[saved[1]:]=[];stats.pop('__checker_test__')
# Explicit coverage inventory and immutable input hashes.
for f,rows in annual.items():stats[f]['issues']=sum(i['file']==f for i in issues)
with (OUT/'findings.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['file','key','field','actual','expected','source','kind']);w.writeheader();w.writerows(issues)
import gzip
with gzip.open(OUT/'cell-ledger.csv.gz','wt',newline='') as f:
 w=csv.writer(f);w.writerow(['file','key','field','source']);w.writerows(ledger)
(OUT/'coverage.json').write_text(json.dumps(dict(stats),indent=2))
files=[p for p in ROOT.rglob('*') if p.is_file() and (p.suffix in ['.csv','.xlsx','.pdf']) and 'Audit' not in p.parts]
(OUT/'input-sha256.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2))
print('ISSUES',Counter(i['kind'] for i in issues));print('CHECKS',sum(x['checks'] for x in stats.values()))
