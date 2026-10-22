'use strict';
const api=require('./render_character.cjs');module.exports=api;
if(require.main===module)api.main().catch(e=>{console.error(e.message);process.exitCode=1});
