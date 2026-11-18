import initSqlJs from 'sql.js';
import wasm from 'sql.js/dist/sql-wasm.wasm?url';
let pending;
export function database(){return pending??=(async()=>{const SQL=await initSqlJs({locateFile:()=>wasm});const r=await fetch('./data/shots.sqlite');if(!r.ok)throw new Error('Database download failed');return new SQL.Database(new Uint8Array(await r.arrayBuffer()));})();}
export async function query(team='',split=''){const db=await database();const st=db.prepare('SELECT shot_id,date,player,team,opponent,result,model_xg,split FROM shots WHERE (? = \'\' OR team = ?) AND (? = \'\' OR split = ?) ORDER BY date DESC,shot_id DESC');try{st.bind([team,team,split,split]);const rows=[];while(st.step())rows.push(st.getAsObject());return rows;}finally{st.free();}}
