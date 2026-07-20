(async()=>{
  const loadText=async files=>{const parts=await Promise.all(files.map(f=>fetch(`assets/${f}`).then(r=>{if(!r.ok)throw new Error(`Failed to load ${f}`);return r.text()})));return parts.join("")};
  const manifest={"styles.css": ["styles.css.part01.txt", "styles.css.part02.txt"], "data.js": ["data.js.part01.txt", "data.js.part02.txt"], "app.js": ["app.js.part01.txt", "app.js.part02.txt", "app.js.part03.txt", "app.js.part04.txt", "app.js.part05.txt", "app.js.part06.txt", "app.js.part07.txt"]};
  const css=await loadText(manifest["styles.css"]);const style=document.createElement("style");style.textContent=css;document.head.appendChild(style);
  const data=await loadText(manifest["data.js"]);(0,eval)(data);
  const app=await loadText(manifest["app.js"]);(0,eval)(app);
})().catch(err=>{console.error(err);document.body.innerHTML=`<pre style="direction:ltr;padding:24px">${err.stack||err}</pre>`});
