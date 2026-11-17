import numpy as np
import pandas as pd
import pytest
from src.pipeline import geometry, load_data, split_dates, FEATURES, scores, calibration

def test_geometry_center_and_symmetry():
    d,a=geometry([.9,.9,.9],[.5,.3,.7])
    assert d[0]==pytest.approx(10.5)
    assert a[0]==pytest.approx(2*np.arctan(3.66/10.5))
    assert a[1]==pytest.approx(a[2])
    assert a[0]>a[1]

@pytest.mark.parametrize('x,y',[(1.1,.5),(.5,-.1),(float('nan'),.5)])
def test_bad_coordinates(x,y):
    with pytest.raises(ValueError):geometry([x],[y])

def test_source_audit_and_exclusions():
    s,a=load_data()
    assert a['raw_shots']==2746 and a['matches']==100
    assert len(s)==a['raw_shots']-a['excluded']
    assert not s.situation.eq('Penalty').any()
    assert not s.result.eq('OwnGoal').any()
    assert s.shot_id.is_unique

def test_temporal_match_separation():
    s,_=load_data();s['split']=split_dates(s)
    assert s.groupby('fixture_id').split.nunique().max()==1
    assert s.groupby('date').split.nunique().max()==1
    parts=[s[s.split.eq(p)] for p in ['train','validation','test']]
    assert parts[0].date.max()<parts[1].date.min()<parts[2].date.min()
    assert parts[1].date.max()<parts[2].date.min()

def test_no_target_or_provider_features():
    assert set(FEATURES)=={'distance_m','angle_rad','shot_type','situation','last_action'}

def test_metric_and_calibration_fixtures():
    y=np.array([0,1]);p=np.array([.2,.8]);m=scores(y,p)
    assert m['brier']==pytest.approx(.04)
    assert m['log_loss']==pytest.approx(-np.log(.8))
    assert m['auc']==1
    assert sum(b['count'] for b in calibration(y,p))==2

def test_duplicate_shots_rejected(tmp_path):
    from src.pipeline import ROOT
    import shutil
    for p in (ROOT/'data/raw').glob('*'):shutil.copy(p,tmp_path/p.name)
    s=pd.read_csv(tmp_path/'shots.csv');pd.concat([s,s.iloc[:1]]).to_csv(tmp_path/'shots.csv',index=False)
    with pytest.raises(ValueError,match='Duplicate'):load_data(tmp_path)

def test_export_integrity_and_portable_model(tmp_path):
    import json,sqlite3
    from src.pipeline import run
    report,s=run(tmp_path)
    with sqlite3.connect(tmp_path/'shots.sqlite') as db:
        assert db.execute('SELECT COUNT(*) FROM shots').fetchone()[0]==len(s)
        assert db.execute('SELECT COUNT(DISTINCT shot_id) FROM shots').fetchone()[0]==len(s)
    assert s.model_xg.between(0,1).all()
    winner=min(['logistic','boosted'],key=lambda k:report['evaluations'][k]['validation']['log_loss'])
    assert winner==report['selected_model']
    assert sum(b['count'] for b in report['evaluations'][winner]['calibration'])==report['partitions']['test']['shots']
    model=json.loads((tmp_path/'logistic.json').read_text())
    assert len(model['coef'])==len(model['numeric'])+sum(map(len,model['categories']))
