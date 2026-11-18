import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import {geometry,predict,aggregate,csv} from '../src/model.js';
const shots=JSON.parse(readFileSync(new URL('../public/data/shots.json',import.meta.url))),model=JSON.parse(readFileSync(new URL('../public/data/logistic.json',import.meta.url)));
test('portable logistic predictions agree with sklearn across every shot',()=>{for(const s of shots)assert.ok(Math.abs(predict(model,s)-s.logistic_xg)<1e-8);});
test('geometry is symmetric around goal center',()=>{assert.equal(geometry(.9,.5)[0],10.499999999999998);assert.ok(Math.abs(geometry(.9,.2)[1]-geometry(.9,.8)[1])<1e-12);});
test('aggregation conserves totals and CSV escapes quotes',()=>{const a=aggregate(shots,'team');assert.equal(a.reduce((n,r)=>n+r.shots,0),shots.length);assert.equal(a.reduce((n,r)=>n+r.goals,0),shots.reduce((n,r)=>n+r.goal,0));assert.equal(csv([{name:'A"B'}]),'"name"\n"A""B"');});
