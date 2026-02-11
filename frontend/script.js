const API_BASE = "http://127.0.0.1:8000";

const elUser = document.getElementById("username");
const elPass = document.getElementById("password");

const btnCredsAdmin = document.getElementById("btnCredsAdmin");
const btnCredsUser = document.getElementById("btnCredsUser");
const btnPayload = document.getElementById("btnPayload");
const btnClear = document.getElementById("btnClear");
const btnVuln = document.getElementById("btnVuln");
const btnSafe = document.getElementById("btnSafe");

const output = document.getElementById("output");
const loading = document.getElementById("loading");
const metaEndpoint = document.getElementById("metaEndpoint");
const metaHttp = document.getElementById("metaHttp");

// Función que deshabilita los botones cuando la petición está en curso
function setLoading(v){
  loading.classList.toggle("hidden", !v);
  [btnVuln, btnSafe, btnCredsAdmin, btnCredsUser, btnPayload, btnClear].forEach(b => b.disabled = v);
}

function setMeta(endpoint, http){
  metaEndpoint.textContent = endpoint ?? "—";
  metaHttp.textContent = http ?? "—";
}

function pretty(x){ return JSON.stringify(x, null, 2); }

// Función que se encarga de llamar al endpoint pasado por parámetro para iniciar sesión
async function login(path){
  const username = elUser.value.trim();
  const password = elPass.value;

  if(!username || !password){
    output.textContent = "⚠️ Rellena usuario y password.";
    return;
  }

  const url = `${API_BASE}${path}`;
  setMeta(path, "—");
  setLoading(true);

  try{
    const res = await fetch(url, {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({username, password})
    });

    const text = await res.text();
    let body;
    try { body = JSON.parse(text); } catch { body = {raw:text}; }

    setMeta(path, `${res.status} ${res.ok ? "(OK)" : "(ERROR)"}`);
    output.textContent = pretty(body);
  }catch(e){
    setMeta(path, "NETWORK ERROR");
    output.textContent = pretty({error: String(e)});
  }finally{
    setLoading(false);
  }
}

// EVENTOS DE LOS BOTONES
btnCredsAdmin.onclick = () => { elUser.value="admin"; elPass.value="admin123"; };
btnCredsUser.onclick = () => { elUser.value="user"; elPass.value="user123"; };

// Payload típico de bypass: en password
btnPayload.onclick = () => { elUser.value="admin"; elPass.value="' OR '1'='1"; };

btnClear.onclick = () => { elUser.value=""; elPass.value=""; setMeta(null,null); output.textContent="Rellena usuario/password y prueba ambos endpoints."; };

btnVuln.onclick = () => login("/login-vuln");
btnSafe.onclick = () => login("/login-safe");
