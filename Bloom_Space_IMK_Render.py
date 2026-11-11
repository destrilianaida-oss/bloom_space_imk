# Bloom Space - Web IMK (satu file Python)
# Jalankan file ini di VS Code dengan tombol Run Python File.
# Tidak perlu Flask atau aplikasi tambahan.

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import threading
import webbrowser
import os
from pathlib import Path

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))

HTML = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bloom Space | IMK</title>
<style>
:root{--pink:#e77eaa;--deep:#a33d70;--pale:#fff0f6;--cream:#fff9ef;--ink:#59384a;--muted:#987b8b}
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;background:linear-gradient(135deg,#fff0f6,#fff9ef);color:var(--ink);min-height:100vh}
button,input,textarea{font:inherit}button{cursor:pointer;border:0;border-radius:13px;padding:12px 16px;background:var(--pink);color:white;font-weight:bold}button:hover{filter:brightness(.96)}.soft{background:#ffedf5;color:var(--deep)}.small{padding:8px 11px;font-size:12px}
.auth-wrap{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}.auth{width:min(900px,100%);background:white;border-radius:26px;overflow:hidden;box-shadow:0 15px 45px #b66b8b25;display:grid;grid-template-columns: .9fr 1.1fr}.welcome{padding:40px;background:linear-gradient(145deg,#f7c4d9,#fff0d8);display:flex;flex-direction:column;justify-content:center}.welcome .flower{font-size:65px}.welcome h1{font-size:34px;margin:12px 0}.welcome p{line-height:1.7;color:#805c70}.authform{padding:40px;display:flex;align-items:center;justify-content:center}.panel{width:100%;max-width:360px}.panel h2{margin:0 0 8px}.sub{color:var(--muted);font-size:14px;line-height:1.5;margin:0 0 22px}label{display:block;font-size:13px;font-weight:bold;margin:14px 0 7px}input,textarea{width:100%;border:1px solid #ead9e2;background:#fffdfd;border-radius:12px;padding:13px;color:var(--ink);outline:none}input:focus,textarea:focus{border-color:var(--pink);box-shadow:0 0 0 3px #fbe3ee}.full{width:100%;margin-top:18px}.links{text-align:center;font-size:13px;color:var(--muted);margin-top:17px}.links a{color:var(--deep);font-weight:bold;cursor:pointer;text-decoration:underline}.msg{min-height:18px;font-size:13px;color:#b34470;margin-top:10px}.hide{display:none!important}
.app{min-height:100vh;display:grid;grid-template-columns:220px 1fr}.sidebar{background:linear-gradient(180deg,#e77eaa,#d96698);padding:25px 15px;color:white}.brand{text-align:center;font-weight:bold;font-size:22px;margin:5px 0 35px}.brand span{display:block;font-size:35px}.nav{display:flex;flex-direction:column;gap:9px}.nav button{background:transparent;text-align:left;color:white;font-weight:normal}.nav button.active,.nav button:hover{background:#ffffff50}.main{padding:30px;max-width:1250px;width:100%;margin:auto}.top{display:flex;justify-content:space-between;align-items:center;gap:12px}.top h1{margin:0;font-size:28px}.top p{margin:7px 0 22px;color:var(--muted)}.banner{padding:25px;border-radius:20px;background:linear-gradient(110deg,#ffd9e9,#fff0d8);display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:24px}.banner h2{margin:0 0 8px;color:var(--deep)}.banner p{margin:0;color:#805c70}.banner .flower{font-size:50px}.section-title{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:18px 0}.section-title h2{font-size:19px;margin:0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px}.entry{background:white;border:1px solid #f2dce6;border-radius:16px;padding:17px;box-shadow:0 5px 18px #c887a015}.entry .date{font-size:12px;color:var(--muted);margin-bottom:10px}.entry .body{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.5}.entry-actions{display:flex;justify-content:flex-end;gap:8px;margin-top:14px}.empty{background:white;border:1px dashed #e8b8ce;border-radius:16px;padding:28px;text-align:center;color:var(--muted)}.editor{background:white;border:1px solid #f2dce6;border-radius:18px;padding:22px;max-width:750px}.editor textarea{min-height:180px;resize:vertical}.editor-actions{display:flex;gap:10px;flex-wrap:wrap}.editor-actions button{margin-top:15px}.about{background:white;border-radius:18px;padding:25px;line-height:1.7}.about h2{color:var(--deep)}
@media(max-width:700px){.auth{grid-template-columns:1fr}.welcome{padding:24px;text-align:center}.welcome .flower{font-size:45px}.welcome h1{font-size:26px}.authform{padding:26px}.app{grid-template-columns:1fr}.sidebar{padding:12px}.brand{margin:5px 0 10px}.brand span{display:inline;font-size:24px}.nav{flex-direction:row;flex-wrap:wrap;justify-content:center}.nav button{padding:9px 11px;font-size:12px}.main{padding:18px}.top h1{font-size:22px}.banner{padding:18px}.banner .flower{font-size:35px}}
</style></head>
<body>
<div id="authScreen" class="auth-wrap">
 <div class="auth">
  <div class="welcome"><div class="brand">✿ BLOOM SPACE</div><div class="flower">🌷</div><h1>Tempat nyaman<br>untuk memulai.</h1><p>Login, kelola akun, dan nikmati pengalaman web yang sederhana serta menyenangkan.</p></div>
  <div class="authform">
   <section class="panel" id="loginPanel"><h2>Selamat datang! 💗</h2><p class="sub">Masuk ke akun Bloom Space kamu.</p><label>Username</label><input id="loginUser" placeholder="Masukkan username"><label>Password</label><input id="loginPass" type="password" placeholder="Masukkan password"><button class="full" onclick="login()">Login →</button><div class="msg" id="loginMsg"></div><div class="links">Belum punya akun? <a onclick="showAuth('registerPanel')">Daftar di sini</a><br><br><a onclick="showAuth('forgotPanel')">Lupa Password?</a></div></section>
   <section class="panel hide" id="registerPanel"><h2>Daftar Akun 🌸</h2><p class="sub">Buat akun baru untuk mulai menggunakan Bloom Space.</p><label>Nama lengkap</label><input id="regName" placeholder="Nama kamu"><label>Username</label><input id="regUser" placeholder="Buat username"><label>Password</label><input id="regPass" type="password" placeholder="Minimal 4 karakter"><label>Konfirmasi password</label><input id="regConfirm" type="password" placeholder="Ulangi password"><button class="full" onclick="register()">Daftar</button><div class="msg" id="regMsg"></div><div class="links"><a onclick="showAuth('loginPanel')">Kembali ke Login</a></div></section>
   <section class="panel hide" id="forgotPanel"><h2>Reset Password 🔐</h2><p class="sub">Masukkan username dan password baru. (Simulasi tugas)</p><label>Username</label><input id="forgotUser" placeholder="Username terdaftar"><label>Password baru</label><input id="forgotPass" type="password" placeholder="Password baru"><button class="full" onclick="resetPassword()">Simpan password baru</button><div class="msg" id="forgotMsg"></div><div class="links"><a onclick="showAuth('loginPanel')">Kembali ke Login</a></div></section>
  </div>
 </div>
</div>
<div id="appScreen" class="app hide">
 <aside class="sidebar"><div class="brand"><span>🌷</span><br>BLOOM SPACE</div><div class="nav"><button id="navDashboard" class="active" onclick="showPage('dashboard')">⌂ Dashboard</button><button id="navDiary" onclick="showPage('diary')">▤ My Diary</button><button id="navAbout" onclick="showPage('about')">ⓘ About</button><button onclick="logout()">⇥ Logout</button></div></aside>
 <main class="main">
  <section id="dashboardPage"><div class="top"><div><h1>Hai, <span id="helloName">Teman</span>! 🌸</h1><p>Kamu berhasil login. Selamat datang di Bloom Space.</p></div><button class="small" onclick="logout()">Logout</button></div><div class="banner"><div><h2>Write your thoughts,<br>make it beautiful ♡</h2><p>Ruang kecil untuk menyimpan cerita dan pikiranmu.</p></div><div class="flower">🌷💌</div></div><div class="section-title"><h2>✿ Catatan Terbaru Kamu</h2><button class="small" onclick="showPage('write')">＋ Tulis Catatan</button></div><div id="recentEntries" class="cards"></div></section>
  <section id="diaryPage" class="hide"><div class="top"><div><h1>My Diary 📔</h1><p>Kumpulan catatan yang kamu simpan.</p></div><button class="small" onclick="showPage('write')">＋ Tulis Catatan</button></div><div id="allEntries" class="cards"></div></section>
  <section id="writePage" class="hide"><div class="top"><div><h1>Tulis Catatan Baru ✿</h1><p>Tuangkan cerita atau pikiranmu di sini.</p></div></div><div class="editor"><label for="noteText">Catatan kamu</label><textarea id="noteText" placeholder="Tulis catatan kamu di sini... ♡"></textarea><div class="editor-actions"><button onclick="saveNote()">💾 Simpan Catatan</button><button class="soft" onclick="showPage('diary')">↩ Batal</button></div><div class="msg" id="noteMsg"></div></div></section>
  <section id="aboutPage" class="hide"><div class="top"><div><h1>About Bloom Space ✿</h1><p>Informasi singkat tentang web.</p></div></div><div class="about"><h2>Bloom Space</h2><p>Bloom Space adalah prototype website diary digital yang dibuat untuk tugas mata kuliah Interaksi Manusia dan Komputer (IMK). Website ini menyediakan fitur daftar akun, login, simulasi lupa password, dashboard, serta pencatatan diary.</p><p>Tujuan desainnya adalah membuat antarmuka sederhana, mudah dipahami, dan nyaman digunakan.</p></div></section>
 </main>
</div>
<script>
const readUsers=()=>JSON.parse(localStorage.getItem('bloomSpaceUsers')||'{}');
const writeUsers=u=>localStorage.setItem('bloomSpaceUsers',JSON.stringify(u));
let current=localStorage.getItem('bloomSpaceCurrent')||'';
function showAuth(id){document.querySelectorAll('#authform .panel');['loginPanel','registerPanel','forgotPanel'].forEach(x=>document.getElementById(x).classList.add('hide'));document.getElementById(id).classList.remove('hide')}
function register(){let name=regName.value.trim(),user=regUser.value.trim(),pass=regPass.value,confirm=regConfirm.value,msg=regMsg,u=readUsers();if(!name||!user||!pass||!confirm){msg.textContent='Semua kolom wajib diisi.';return}if(pass.length<4){msg.textContent='Password minimal 4 karakter.';return}if(pass!==confirm){msg.textContent='Konfirmasi password tidak sama.';return}if(u[user]){msg.textContent='Username sudah dipakai.';return}u[user]={name,password:pass,notes:[]};writeUsers(u);msg.textContent='Akun berhasil dibuat! Silakan login.';setTimeout(()=>showAuth('loginPanel'),800)}
function login(){let user=loginUser.value.trim(),pass=loginPass.value,u=readUsers();if(!u[user]||u[user].password!==pass){loginMsg.textContent='Username atau password salah.';return}current=user;localStorage.setItem('bloomSpaceCurrent',current);openApp()}
function resetPassword(){let user=forgotUser.value.trim(),pass=forgotPass.value,u=readUsers();if(!user||!pass){forgotMsg.textContent='Kolom harus diisi.';return}if(pass.length<4){forgotMsg.textContent='Password minimal 4 karakter.';return}if(!u[user]){forgotMsg.textContent='Username tidak ditemukan.';return}u[user].password=pass;writeUsers(u);forgotMsg.textContent='Password berhasil diubah. Silakan login.'}
function logout(){current='';localStorage.removeItem('bloomSpaceCurrent');appScreen.classList.add('hide');authScreen.classList.remove('hide');showAuth('loginPanel')}
function openApp(){let u=readUsers();if(!current||!u[current]){logout();return}authScreen.classList.add('hide');appScreen.classList.remove('hide');helloName.textContent=u[current].name;renderEntries();showPage('dashboard')}
function showPage(page){['dashboard','diary','write','about'].forEach(p=>document.getElementById(p+'Page').classList.add('hide'));document.getElementById(page+'Page').classList.remove('hide');['Dashboard','Diary','About'].forEach(n=>document.getElementById('nav'+n).classList.toggle('active',page.toLowerCase()===n.toLowerCase()));if(page==='diary'||page==='dashboard')renderEntries()}
function getNotes(){let u=readUsers();if(!u[current])return [];if(!Array.isArray(u[current].notes))u[current].notes=[];return u[current].notes;}
function renderEntries(){let notes=getNotes();let newestFirst=notes.slice().reverse();recentEntries.innerHTML=renderList(newestFirst);allEntries.innerHTML=renderList(newestFirst);}
function renderList(items){if(!items.length)return '<div class="empty">Belum ada catatan. Yuk, tulis diary pertamamu! 🌷</div>';return items.map(item=>`<article class="entry"><div class="date">📅 ${item.date}</div><div class="body">${escapeHTML(item.text)}</div><div class="entry-actions"><button class="soft small" onclick="deleteNote(${item.id})">🗑 Hapus</button></div></article>`).join('')}
function escapeHTML(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function saveNote(){let text=noteText.value.trim();if(!text){noteMsg.textContent='Catatan tidak boleh kosong.';return}let u=readUsers();if(!Array.isArray(u[current].notes))u[current].notes=[];u[current].notes.push({id:Date.now(),date:new Date().toLocaleString('id-ID'),text:text});writeUsers(u);noteText.value='';noteMsg.textContent='Catatan berhasil ditambahkan ke diary 💕';renderEntries();setTimeout(()=>showPage('diary'),500)}
function deleteNote(id){if(!confirm('Yakin ingin menghapus catatan ini?'))return;let u=readUsers();u[current].notes=u[current].notes.filter(n=>n.id!==id);writeUsers(u);renderEntries()}
if(current)openApp();
</script>
</body></html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Bloom Space berjalan pada port {PORT}.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nWeb dihentikan.")
        server.server_close()
