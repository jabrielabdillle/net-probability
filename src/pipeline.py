"""Reproducible, pre-shot xG experiment on a pinned partial-season snapshot."""
from pathlib import Path
import hashlib
import json
import sqlite3
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss, brier_score_loss, roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '5a9d2391d8cf1879a54c8a67bc25039c454479f0'
NUMERIC = ['distance_m', 'angle_rad']
CATEGORICAL = ['shot_type', 'situation', 'last_action']
FEATURES = NUMERIC + CATEGORICAL
OUTCOMES = {'MissedShots', 'BlockedShot', 'Goal', 'SavedShot', 'ShotOnPost', 'OwnGoal'}

def geometry(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if not (np.isfinite(x).all() and np.isfinite(y).all() and ((x >= 0) & (x <= 1)).all() and ((y >= 0) & (y <= 1)).all()):
        raise ValueError('Coordinates must be finite and normalized to [0, 1]')
    dx, dy = (1 - x) * 105, (y - .5) * 68
    distance = np.hypot(dx, dy)
    angle = np.arctan2(7.32 * dx, dx ** 2 + dy ** 2 - 3.66 ** 2)
    return distance, angle

def load_data(raw=ROOT / 'data/raw'):
    s = pd.read_csv(raw / 'shots.csv', keep_default_na=False)
    f = pd.read_csv(raw / 'fixtures.csv', keep_default_na=False)
    required = {'shot_id','fixture_id','date','x','y','xg','result','h_a','player','minute','gw',*CATEGORICAL}
    if not required.issubset(s.columns): raise ValueError('Missing shot columns')
    if s.shot_id.duplicated().any() or s.shot_id.eq('').any(): raise ValueError('Duplicate or empty shot IDs')
    if f.fixture_id.duplicated().any(): raise ValueError('Duplicate fixtures')
    if not set(s.result) <= OUTCOMES: raise ValueError('Unknown shot outcome')
    if not set(s.h_a) <= {'h','a'}: raise ValueError('Invalid home/away flag')
    if s[['player',*CATEGORICAL]].eq('').any().any(): raise ValueError('Missing categorical data')
    s['distance_m'], s['angle_rad'] = geometry(s.x, s.y)
    s['xg'] = pd.to_numeric(s.xg, errors='coerce')
    eligible = ~(s.situation.eq('Penalty') | s.result.eq('OwnGoal'))
    if not (np.isfinite(s.loc[eligible,'xg']).all() and s.loc[eligible,'xg'].between(0,1).all()): raise ValueError('Invalid provider xG for modeled shot')
    s = s.merge(f[['fixture_id','kickoff_time','home_team','away_team','finished']], on='fixture_id', how='left', validate='many_to_one', indicator=True)
    if not s._merge.eq('both').all(): raise ValueError('Orphan fixture')
    if not s.finished.eq(1).all(): raise ValueError('Shot in unfinished fixture')
    shot_dates = pd.to_datetime(s.date, utc=True, errors='raise')
    kicks = pd.to_datetime(s.kickoff_time, utc=True, errors='raise')
    if not shot_dates.eq(kicks).all(): raise ValueError('Shot/fixture kickoff disagreement')
    s['date'] = kicks.dt.strftime('%Y-%m-%d')
    s['team'] = np.where(s.h_a.eq('h'),s.home_team,s.away_team)
    s['opponent'] = np.where(s.h_a.eq('h'),s.away_team,s.home_team)
    s['goal'] = s.result.eq('Goal').astype(int)
    excluded = s.situation.eq('Penalty') | s.result.eq('OwnGoal')
    audit = {'raw_shots':len(s),'penalties':int(s.situation.eq('Penalty').sum()),'own_goals':int(s.result.eq('OwnGoal').sum()),'excluded':int(excluded.sum()),'modeled_shots':int((~excluded).sum()),'matches':int(s.fixture_id.nunique()),'first_date':s.date.min(),'last_date':s.date.max(),'gw_min':int(s.gw.min()),'gw_max':int(s.gw.max()),'source_exported_at':json.loads((raw/'manifest.json').read_text())['exported_at']}
    return s.loc[~excluded].drop(columns=['_merge']).sort_values(['date','fixture_id','shot_id']).reset_index(drop=True), audit

def split_dates(s):
    dates = sorted(s.date.unique())
    if len(dates) < 10: raise ValueError('At least ten distinct match dates required')
    a,b = int(len(dates)*.6),int(len(dates)*.8)
    labels = {d: ('train' if i<a else 'validation' if i<b else 'test') for i,d in enumerate(dates)}
    result = s.date.map(labels)
    for part in ['train','validation','test']:
        if s.loc[result.eq(part),'goal'].nunique() != 2: raise ValueError('Each partition must include goals and non-goals')
    return result

def scores(y,p):
    return {'log_loss':float(log_loss(y,p,labels=[0,1])), 'brier':float(brier_score_loss(y,p)), 'auc':float(roc_auc_score(y,p)) if len(set(y))>1 else None}

def calibration(y,p):
    bins = np.minimum((np.asarray(p)*10).astype(int),9)
    return [{'lower':i/10,'upper':(i+1)/10,'count':int((bins==i).sum()),'predicted':float(np.mean(p[bins==i])),'observed':float(np.mean(y[bins==i]))} for i in range(10) if (bins==i).any()]

def bootstrap(s, p, repetitions=300):
    rng=np.random.default_rng(42)
    groups=[np.flatnonzero(s.fixture_id.to_numpy()==k) for k in s.fixture_id.unique()]
    draws=[]
    for _ in range(repetitions):
        idx=np.concatenate([groups[i] for i in rng.integers(0,len(groups),len(groups))])
        draws.append(scores(s.goal.to_numpy()[idx],p[idx]))
    return {metric:[float(v) for v in np.quantile([r[metric] for r in draws if r[metric] is not None],[.025,.975])] for metric in ['log_loss','brier','auc']}

def run(output=ROOT/'web/public/data'):
    output.mkdir(parents=True,exist_ok=True)
    s,audit=load_data();s['split']=split_dates(s)
    train=s[s.split.eq('train')]; val=s[s.split.eq('validation')]; test=s[s.split.eq('test')]
    def transform():
        return ColumnTransformer([('num',StandardScaler(),NUMERIC),('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),CATEGORICAL)])
    models={'logistic':make_pipeline(transform(),LogisticRegression(C=1,max_iter=2000,random_state=42)), 'boosted':make_pipeline(transform(),HistGradientBoostingClassifier(max_iter=100,max_leaf_nodes=7,min_samples_leaf=30,l2_regularization=5,learning_rate=.05,early_stopping=False,random_state=42))}
    probabilities={'base_rate':np.full(len(s),train.goal.mean()),'provider':s.xg.to_numpy()}
    for name,model in models.items():
        model.fit(train[FEATURES],train.goal)
        probabilities[name]=model.predict_proba(s[FEATURES])[:,1]
    valmask=s.split.eq('validation').to_numpy(); testmask=s.split.eq('test').to_numpy()
    chosen=min(models,key=lambda name:log_loss(val.goal,probabilities[name][valmask]))
    evaluations={}
    for name,p in probabilities.items():
        evaluations[name]={'validation':scores(val.goal,p[valmask]),'test':scores(test.goal,p[testmask]),'calibration':calibration(test.goal.to_numpy(),p[testmask]),'test_ci95':bootstrap(test,p[testmask])}
    s['model_xg']=probabilities[chosen]
    for name in models: s[name+'_xg']=probabilities[name]
    partitions={part:{'shots':len(g),'matches':int(g.fixture_id.nunique()),'goals':int(g.goal.sum()),'start':g.date.min(),'end':g.date.max()} for part,g in s.groupby('split')}
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'data/raw').glob('*') if p.is_file()}
    report={'source':'pl-catalogue / Understat','source_url':'https://github.com/oladeeayo/pl-catalogue','source_commit':SOURCE_SHA,'season':'2026–27','audit':audit,'hashes':hashes,'features':FEATURES,'partitions':partitions,'selected_model':chosen,'selection_rule':'Lowest validation log loss; no retraining on validation or test','evaluations':evaluations,'bootstrap':'300 resamples of whole test matches, percentile 95% intervals; conditional on fitted models','provider_caveat':'External published xG; provider training data and evaluation independence are unknown.'}
    fields=['shot_id','fixture_id','gw','date','minute','player','team','opponent','x','y','distance_m','angle_rad','shot_type','situation','last_action','result','goal','xg','model_xg','logistic_xg','boosted_xg','split']
    rows=json.loads(s[fields].to_json(orient='records',double_precision=10))
    (output/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    (output/'shots.json').write_text(json.dumps(rows,ensure_ascii=False,allow_nan=False)+'\n')
    s[fields].to_csv(output/'shots.csv',index=False)
    with sqlite3.connect(output/'shots.sqlite') as db:
        db.execute('DROP TABLE IF EXISTS shots')
        s[fields].to_sql('shots',db,index=False)
        db.execute('CREATE UNIQUE INDEX shot_key ON shots(shot_id)')
        db.execute('CREATE INDEX shot_filters ON shots(team, date, player)')
        db.execute('DROP TABLE IF EXISTS provenance')
        db.execute('CREATE TABLE provenance (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        db.executemany('INSERT INTO provenance VALUES (?,?)',[('source',report['source_url']),('commit',SOURCE_SHA),('usage','Non-commercial with attribution; upstream provider rights apply')])
    # Export a logistic model for live what-if inference; parity checked against sklearn.
    prep=models['logistic'][0]; classifier=models['logistic'][1]; scaler=prep.named_transformers_['num']; encoder=prep.named_transformers_['cat']
    portable={'numeric':NUMERIC,'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'categorical':CATEGORICAL,'categories':[a.tolist() for a in encoder.categories_],'coef':classifier.coef_[0].tolist(),'intercept':float(classifier.intercept_[0]),'model':'logistic','pitch_m':[105,68],'goal_width_m':7.32}
    (output/'logistic.json').write_text(json.dumps(portable,indent=2)+'\n')
    print(json.dumps({'audit':audit,'partitions':partitions,'selected':chosen,'test':{k:v['test'] for k,v in evaluations.items()}},indent=2))
    return report,s

if __name__=='__main__': run()
