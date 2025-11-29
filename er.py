from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LoveFrom — 45 Jahre & AGB Quiz</title>
<style>
  :root{
    --bg:#ffffff;
    --text:#0b0b0b;
    --muted:#6b6b6b;
    --accent:#111111;
    --max-width:1100px;
    --radius:18px;
    --mono: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  }
  *{box-sizing:border-box;}
  html,body{height:100%;margin:0;font-family:var(--mono);background:var(--bg);color:var(--text);line-height:1.36;}
  .wrap{max-width:var(--max-width);margin:0 auto;padding:64px 28px;}
  header{display:flex;align-items:center;justify-content:center;gap:24px;}
  .brand{font-weight:600;font-size:32px;letter-spacing:0.08em;text-transform:uppercase;text-align:center;}
  nav a{display:none;}
  footer{margin-top:120px;padding:36px 0;color:var(--muted);border-top:1px solid rgba(11,11,11,0.04);text-align:center;}

  /* AGB Overlay */
  #agb-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;z-index:9999;}
  #agb-window{background:#fff;color:#111;padding:36px;border-radius:16px;width:80%;max-width:900px;max-height:80%;overflow-y:auto;box-shadow:0 10px 40px rgba(0,0,0,0.3);}
  #agb-window h2{margin-top:0;font-size:22px;font-weight:600;color:#111;}
  #agb-accept{display:block;margin-top:24px;padding:12px 20px;font-weight:600;border-radius:12px;border:none;background:#111;color:#fff;cursor:pointer;width:100%;}
  #agb-window ol{padding-left:20px;}

  /* QUIZ */
  #quiz-section{margin-top:80px;}
  #quiz-form .question{margin-bottom:24px;}
  input[type="text"]{
    width:100%;padding:10px 12px;border-radius:8px;border:1px solid var(--muted);font-size:15px;
  }
  .wrong{border:2px solid red;background:#ffe0e0;}
  #check-btn{display:inline-block;padding:14px 22px;border-radius:12px;border:1px solid var(--accent);text-decoration:none;font-weight:600;cursor:pointer;margin-top:16px;}
  #finish-btn{display:none;margin-top:32px;}
  #countup{font-size:32px;text-align:center;margin-top:40px;font-weight:600;}
  @media (max-width:620px){.wrap{padding:36px 20px}}
</style>
</head>
<body>

<!-- AGB OVERLAY -->
<div id="agb-overlay">
  <div id="agb-window">
    <h2>Allgemeine Geschäftsbedingungen</h2>
    <ol>
      {% for agb in agbs %}
        <li>{{ agb }}</li>
      {% endfor %}
    </ol>
    <button id="agb-accept">Akzeptieren</button>
  </div>
</div>

<div class="wrap">
  <header>
    <div class="brand" id="countup">L O V E F R O M</div>
  </header>

  <main>
    <!-- QUIZ SECTION -->
    <section id="quiz-section">
      <h1>Happy Birthday</h1>
      <p>Beantworte alle fragen richtig. Tipp: du brauchst die AGBs.</p>

      <form id="quiz-form">
        {% for i, q in enumerate(questions) %}
          <div class="question">
            <p>{{ i+1 }}. {{ q['question'] }}</p>
            <input type="text" data-answer="{{ q['answer'] }}">
          </div>
        {% endfor %}
      </form>

      <button id="check-btn" type="button">Antworten prüfen</button>
      <a id="finish-btn" href="https://dein-link-hier.de">Geheimer Link</a>
    </section>

    <footer>
      <div style="font-weight:600">Happy Birthday</div>
      <div style="color:var(--muted);font-size:14px">© 2025 — Alle Rechte vorbehalten</div>
    </footer>
  </main>
</div>

<script>
  /* COUNTDOWN bis 04.12.2025 00:01, danach 45 Jahre */
  function updateCountup(){
    const birthday45 = new Date('2025-12-04T00:01:00'); // 45 Jahre
    const now = new Date();

    if(now < birthday45){
      let diff = birthday45 - now;

      let totalSeconds = Math.floor(diff / 1000);
      let totalMinutes = Math.floor(totalSeconds / 60);
      let totalHours = Math.floor(totalMinutes / 60);
      let totalDays = Math.floor(totalHours / 24);

      const years = 44; // noch nicht 45
      const months = Math.floor((totalDays % 365.25) / 30);
      const weeks = Math.floor(((totalDays % 365.25) % 30) / 7);
      const days = Math.floor(((totalDays % 365.25) % 30) % 7);
      const hours = totalHours % 24;
      const minutes = totalMinutes % 60;
      const seconds = totalSeconds % 60;

      document.getElementById('countup').textContent =
        `${years} Jahre, ${months} Monate, ${weeks} Wochen, ${days} Tage, ${hours}h ${minutes}m ${seconds}s`;
    } else {
      document.getElementById('countup').textContent = `45 Jahre, 0 Monate, 0 Wochen, 0 Tage, 0h 0m 0s`;
    }
  }
  setInterval(updateCountup, 1000);
  updateCountup();

  /* AGB Overlay */
  document.getElementById('agb-accept').addEventListener('click',()=>{
    document.getElementById('agb-overlay').style.display='none';
  });

  /* QUIZ */
  const inputs = document.querySelectorAll('input');
  document.getElementById('check-btn').addEventListener('click',()=>{
    let correctCount = 0;
    inputs.forEach(input=>{
      const user = input.value.toLowerCase().replace(/[^\wäöüß]+/g,"").trim();
      const corr = input.dataset.answer.toLowerCase().replace(/[^\wäöüß]+/g,"").trim();
      if(!corr.includes(user) && !user.includes(corr)){
        input.classList.add("wrong");
      } else {
        input.classList.remove("wrong");
        correctCount++;
      }
    });

    if(correctCount >= 12){
      document.getElementById('finish-btn').style.display = 'inline-block';
      alert(`Super! Du hast ${correctCount} von 15 richtig beantwortet. Der geheime Link ist freigeschaltet.`);
    } else {
      alert(`Du hast ${correctCount} von 15 richtig beantwortet. Mindestens 12 richtig erforderlich.`);
    }
  });
</script>

</body>
</html>
"""

# AGBs
all_agbs = [
    "Alle Nutzer:innen müssen bei jedem Besuch mindestens einmal innerlich „Yippie!“ rufen.",
    "Jeder Klick auf einen Button erzeugt automatisch ein imaginäres Konfetti-Feuerwerk.",
    "Wer scrollt, darf dabei Grimassen schneiden oder so tun, als ob.",
    "Lachen ist nicht nur erlaubt, sondern ausdrücklich vorgeschrieben.",
    "Jede:r Besucher:in verpflichtet sich, ab sofort nur noch die freundlichste Version von sich selbst zu sein.",
    "Schokolade und Kekse sind während der Nutzung dringend empfohlen.",
    "Getränke dürfen verschüttet werden – vorzugsweise Tee oder heiße Schokolade.",
    "Wer keinen Kuchen mag, muss dies öffentlich bereuen.",
    "Alle Haustiere gelten als Co-Administratoren dieser Webseite.",
    "Einhörner haben absolutes Rederecht auf allen Seiten.",
    "Nutzer:innen müssen mindestens einmal täglich einen imaginären Drachen streicheln.",
    "Tiere haben Anspruch auf wöchentliche Karaoke-Sessions.",
    "Bei jedem Pop-up ist eine kleine Tanzbewegung vorgeschrieben.",
    "Wer die Maus bewegt, muss ein Mini-Jumping-Jack ausführen.",
    "Scrollen ohne Rhythmus ist strengstens verboten.",
    "Jeder Button auf der Seite kann magisch werden."
]

# Mapping zu Fragen
def convert_to_question(agb):
    if "Yippie" in agb: return "Was müssen Besucher:innen innerlich rufen?"
    if "Konfetti" in agb: return "Was passiert bei jedem Klick?"
    if "Grimassen" in agb: return "Was darf man beim Scrollen machen?"
    if "Lachen" in agb: return "Was ist ausdrücklich vorgeschrieben?"
    if "freundlichste" in agb: return "Wie sollen sich alle Besucher:innen verhalten?"
    if "Schokolade" in agb: return "Was wird während der Nutzung empfohlen?"
    if "Kuchen" in agb: return "Was muss jemand tun, der keinen Kuchen mag?"
    if "Haustiere" in agb: return "Welche Rolle haben Haustiere hier?"
    if "Einhörner" in agb: return "Welche Rechte haben Einhörner hier?"
    if "Drachen" in agb: return "Was muss man täglich tun?"
    if "Karaoke" in agb: return "Was bekommen Tiere wöchentlich?"
    if "Pop-up" in agb: return "Was muss man bei einem Pop-up tun?"
    if "Mini-Jumping" in agb: return "Was muss man tun, wenn man die Maus bewegt?"
    return "Beantworte: " + agb

import random

selected_agbs = random.sample(all_agbs, 15)
questions = [{"question": convert_to_question(a), "answer": a} for a in selected_agbs]

@app.route("/")
def index():
    return render_template_string(HTML, agbs=all_agbs, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
