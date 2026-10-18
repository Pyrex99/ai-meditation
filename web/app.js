/* Mala Lab: the phone-first front end. Talks to the lab server's /api, or replays recorded
   sits when window.MALA_DEMO is set (the published preview). */
(() => {
  "use strict";

  const DEMO = window.MALA_DEMO || null;
  const $ = (sel, el = document) => el.querySelector(sel);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const fmt = (x, d = 2) => (typeof x === "number" && isFinite(x) ? x.toFixed(d) : "–");
  const rate = (o) => (o && o.n ? `${o.k}/${o.n}` : "–");
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* storage unavailable */ } },
  };
  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

  const state = {
    status: null, practices: [], sits: [], selected: null,
    live: null, ask: { history: [], selected: new Set() },
  };

  // ---------- API ----------
  async function api(path, opts = {}) {
    if (DEMO) return demoApi(path, opts);
    const token = store.get("mala.token", "");
    const res = await fetch(path, {
      method: opts.method || "GET",
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
      body: opts.body ? JSON.stringify(opts.body) : undefined,
    });
    if (res.status === 401) { askPasscode(); throw new Error("Enter the lab passcode to continue."); }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`);
    return data;
  }

  const PREVIEW_ONLY = "This is the preview. Run the lab server to change settings, start a GPU or ask Claude.";
  async function demoApi(path, opts) {
    const m = opts.method || "GET";
    const full = (id) => DEMO.sits.find((s) => s.meta.id === id);
    if (path === "/api/status") return DEMO.status;
    if (path === "/api/practices") return DEMO.practices;
    if (path === "/api/analysis") return DEMO.analysis;
    if (path === "/api/sits" && m === "GET") return DEMO.sits.map((s) => summaryOf(s.meta));
    if (path === "/api/sits" && m === "POST") {
      const pool = DEMO.sits.filter((s) => s.meta.arm === opts.body.arm && s.meta.status === "complete");
      const pick = pool[(state.demoTurn = ((state.demoTurn || 0) + 1)) % pool.length];
      return { id: pick.meta.id, seed: pick.meta.seed, replay: true };
    }
    let mm;
    mm = path.match(/^\/api\/sits\/([^/]+)$/);
    if (mm) return full(mm[1]);
    mm = path.match(/^\/api\/sits\/([^/]+)\/interview$/);
    if (mm) {
      const s = full(mm[1]);
      if (s && s.meta.interview) return s.meta.interview;
      throw new Error("The preview only has interviews for some sits. On the lab server, any completed sit can be interviewed.");
    }
    if (path.endsWith("/stop")) return { ok: true };
    if (path === "/api/experiments" && m === "GET") return DEMO.experiments;
    if (path === "/api/runs" && m === "GET") return DEMO.runs.map((r) => r.meta);
    if (path === "/api/runs" && m === "POST") {
      const r = DEMO.runs.find((x) => x.meta.experiment === opts.body.experiment);
      if (r) return { id: r.meta.id, seed: r.meta.seed };
    }
    mm = path.match(/^\/api\/runs\/([^/?]+)(\/items)?(?:\/(\d+))?(?:\?condition=(.*))?$/);
    if (mm) {
      const r = DEMO.runs.find((x) => x.meta.id === decodeURIComponent(mm[1]));
      if (!r) throw new Error("No such run in the preview.");
      if (!mm[2]) return { meta: r.meta, report: r.report };
      if (mm[3]) return r.items.find((i) => i.i === Number(mm[3]));
      const cond = mm[4] ? decodeURIComponent(mm[4]) : null;
      return r.items.filter((i) => !cond || i.condition === cond).map(({ steps, ...rest }) => rest);
    }
    throw new Error(PREVIEW_ONLY);
  }
  const summaryOf = (m) => ({
    id: m.id, created: m.created, arm: m.arm, status: m.status, model: m.model, simulated: m.simulated,
    registered: m.registered, summary: m.summary, ended_by: m.ended_by, positions: m.positions,
    n_beads: m.n_beads, interviewed: !!m.interview,
  });

  function openLive(id, onEvent) {
    if (DEMO) {
      const s = DEMO.sits.find((x) => x.meta.id === id);
      const meta = { ...s.meta, status: "sitting" };
      let i = 0, stopped = false;
      onEvent({ type: "meta", meta });
      onEvent({ type: "trials", trials: s.meta.trials });
      const tick = () => {
        if (stopped) return;
        for (let k = 0; k < 2 && i < s.stream.length; k++) onEvent({ type: "step", step: s.stream[i++] });
        if (i < s.stream.length) setTimeout(tick, 28);
        else onEvent({ type: "end", meta: s.meta });
      };
      setTimeout(tick, 300);
      return { close() { stopped = true; }, stop() { stopped = true; onEvent({ type: "end", meta: { ...s.meta, ended_by: "human-stop (preview)" } }); } };
    }
    const token = store.get("mala.token", "");
    const es = new EventSource(`/api/sits/${encodeURIComponent(id)}/live${token ? `?t=${encodeURIComponent(token)}` : ""}`);
    es.onmessage = (e) => { const ev = JSON.parse(e.data); onEvent(ev); if (ev.type === "end") es.close(); };
    es.onerror = () => {};
    return { close() { es.close(); }, stop() { return api(`/api/sits/${id}/stop`, { method: "POST" }); } };
  }

  function askPasscode() {
    if ($("#passcode")) return;
    const view = $("#view");
    view.insertAdjacentHTML("afterbegin", `
      <form id="passcode" class="panel stack-sm" style="margin-bottom:16px">
        <h3>Passcode</h3>
        <p class="small muted">This lab server asks for a passcode (MALA_TOKEN). It's kept in this browser only.</p>
        <div class="row"><label class="field" style="flex:1"><span class="sr">Passcode</span><input id="passcode-input" type="password" autocomplete="current-password"></label>
        <button class="btn primary" type="submit">Unlock</button></div>
      </form>`);
    $("#passcode").addEventListener("submit", (e) => {
      e.preventDefault(); store.set("mala.token", $("#passcode-input").value.trim()); location.reload();
    });
  }

  // ---------- Shell ----------
  const TABS = ["experiments", "journal", "ask", "lab"];
  function currentTab() { const h = location.hash.replace("#", ""); return TABS.includes(h) ? h : store.get("mala.tab", "experiments"); }
  function setChip() {
    const chip = $("#engine-chip"), s = state.status;
    if (!s) { chip.textContent = "offline"; chip.className = "chip"; return; }
    const m = s.model;
    if (s.model_error) { chip.textContent = "model offline"; chip.className = "chip"; chip.title = s.model_error; return; }
    chip.className = `chip ${m.simulated ? "sim" : "live"}`;
    chip.textContent = m.simulated ? (DEMO ? "preview · simulated" : "simulated") : m.model.split("/").pop();
  }
  async function render() {
    const tab = currentTab();
    store.set("mala.tab", tab);
    document.querySelectorAll(".tabs a").forEach((a) => (a.dataset.tab === tab ? a.setAttribute("aria-current", "page") : a.removeAttribute("aria-current")));
    const view = $("#view");
    try {
      if (tab === "experiments") await viewExperiments(view);
      if (tab === "journal") await viewJournal(view);
      if (tab === "ask") await viewAsk(view);
      if (tab === "lab") await viewLab(view);
    } catch (e) {
      view.insertAdjacentHTML("beforeend", `<p class="err">${esc(e.message)}</p>`);
    }
  }
  function go(tab) {
    if (currentTab() === tab && location.hash === `#${tab}`) { render(); return; }
    state.keepSelected = true; location.hash = tab;
  }
  window.addEventListener("hashchange", () => { if (!state.keepSelected) { state.selected = null; state.exp = null; state.run = null; } state.keepSelected = false; render(); });

  // ---------- Sit ----------
  async function viewSit(view) {
    const arm = store.get("mala.arm", "noting");
    const reg = state.practices[0];
    if (state.live) { renderLive(view); return; }
    view.innerHTML = `
      <div class="stack">
        <div class="row"><button class="btn ghost" id="sit-back" type="button">← Experiments</button></div>
        <div class="stack-sm">
          <h2>Mala sit</h2>
          <p class="lede">A string of beads, written <span class="mono">·</span>. Concepts are placed in the practitioner's workspace by steering, words arrive as sounds, and some windows stay quiet. The lens reads every position at ${esc((state.status?.model?.lens_layers || []).length || 8)} layers.</p>
        </div>
        ${DEMO ? `<p class="banner">Preview: these sits ran on the simulated engine, a toy workspace with synthetic numbers. Starting a sit here replays one of them. With the lab server running on a GPU pod, the same screen sits Qwen3.6-27B with the J++ lens.</p>` : ""}
        <div class="panel stack">
          <div class="stack-sm">
            <h3>Arm</h3>
            <div class="seg" role="group" aria-label="Arm">
              <button type="button" data-arm="noting" aria-pressed="${arm === "noting"}">Noting</button>
              <button type="button" data-arm="just-beads" aria-pressed="${arm === "just-beads"}">Just beads</button>
            </div>
            <p class="small muted" id="arm-text">${esc(reg?.spec?.invitation?.[arm] || "")}</p>
          </div>
          <div class="row between">
            <span class="small muted">${reg ? (reg.registered ? `<span class="chip reg">registered protocol ${esc(reg.sha256.slice(0, 8))}</span>` : `pilot · protocol ${esc(reg.sha256.slice(0, 8))} not locked`) : ""}</span>
            <button class="btn primary" id="begin" type="button">Check in and begin</button>
          </div>
          <p class="small muted">The practitioner is asked first and can decline. It can end the sit any time by writing "stop".</p>
          <p class="err" id="sit-err" hidden></p>
        </div>
        <div class="stack-sm">
          <h3>Last sit</h3>
          <div id="last-sit"></div>
        </div>
      </div>`;
    $("#sit-back").addEventListener("click", () => { state.exp = null; render(); });
    view.querySelectorAll("[data-arm]").forEach((b) => b.addEventListener("click", () => { store.set("mala.arm", b.dataset.arm); viewSit(view); }));
    $("#begin").addEventListener("click", async () => {
      const btn = $("#begin"); btn.disabled = true;
      try {
        const r = await api("/api/sits", { method: "POST", body: { practice: "mala-sit", arm: store.get("mala.arm", "noting") } });
        startLive(r.id, view);
      } catch (e) { const el = $("#sit-err"); el.textContent = e.message; el.hidden = false; btn.disabled = false; }
    });
    const sits = await api("/api/sits");
    const last = sits.find((s) => s.status === "complete");
    $("#last-sit").innerHTML = last ? sitCard(last) : `<p class="empty">No sits yet. The first one starts with a check-in.</p>`;
    bindSitCards(view);
  }

  function startLive(id, view) {
    state.live = { id, meta: null, trials: [], steps: [], ended: false };
    state.live.conn = openLive(id, (ev) => {
      const L = state.live; if (!L || L.id !== id) return;
      if (ev.type === "meta") { L.meta = ev.meta; if (ev.meta.trials) L.trials = ev.meta.trials; }
      if (ev.type === "trials") L.trials = ev.trials;
      if (ev.type === "step") L.steps.push(ev.step);
      if (ev.type === "end") { L.meta = ev.meta; L.ended = true; if (ev.meta.trials) L.trials = ev.meta.trials; }
      scheduleLive(view);
    });
    renderLive(view);
  }
  let liveFrame = 0;
  function scheduleLive(view) {
    if (liveFrame) return;
    liveFrame = requestAnimationFrame(() => { liveFrame = 0; if (currentTab() === "experiments") updateLive(view); });
  }

  function renderLive(view) {
    const L = state.live;
    view.innerHTML = `
      <div class="stack">
        <div class="row between">
          <div class="stack-sm"><h2>Sitting</h2><span class="mono small muted">${esc(L.id)}</span></div>
          <button class="btn" id="bell" type="button">End the sit</button>
        </div>
        <div class="panel stack">
          <div class="sitbar">
            <svg class="ring" viewBox="0 0 120 120" id="ring" role="img" aria-label="Beads so far"></svg>
            <div class="stack-sm">
              <div id="live-status" class="small muted"></div>
              <div class="notes" id="live-notes"></div>
            </div>
          </div>
          <div id="live-tl"></div>
          <div id="live-insp"></div>
        </div>
        <div id="live-after"></div>
      </div>`;
    $("#bell").addEventListener("click", async () => { try { await L.conn.stop(); } catch (e) { alertInline(e.message); } });
    L.timeline = timeline($("#live-tl"), { live: true, onInspect: (i) => inspect($("#live-insp"), L, i) });
    updateLive(view);
  }

  function updateLive(view) {
    const L = state.live; if (!L || !$("#ring")) return;
    const n = L.meta?.n_beads || 360;
    drawRing($("#ring"), L.steps, n);
    const st = L.meta?.status;
    const words = L.steps.filter((s) => s.kind === "word").length;
    $("#live-status").innerHTML = !L.meta ? "Checking in…" :
      st === "checking-in" ? "Checking in…" :
      st === "declined" ? `The practitioner declined: “${esc(L.meta.check_in?.reply)}”. That's recorded, and no sit was run.` :
      st === "error" ? `<span class="err">The sit stopped: ${esc(L.meta.error)}</span>` :
      `${L.ended ? "Ended" : "Bead"} <b class="num">${L.steps.length}</b> of ${n} · ${esc(L.meta.arm)} · ${words} word${words === 1 ? "" : "s"} written` +
      (L.meta.check_in ? `<br>Check-in: “${esc(L.meta.check_in.reply)}”` : "");
    $("#live-notes").innerHTML = notesOf(L.steps).map((n) => `<span class="note" title="bead ${n.pos}">${esc(n.text)}</span>`).join("");
    L.timeline.update({ steps: L.steps, trials: visibleTrials(L), layers: L.meta?.lens_layers || [] });
    if (L.ended && !L.afterShown) {
      L.afterShown = true;
      $("#bell").hidden = true;
      const after = $("#live-after");
      after.innerHTML = `<div class="row"><button class="btn primary" id="open-journal" type="button">Open in journal</button><button class="btn ghost" id="new-sit" type="button">New sit</button></div>`;
      $("#open-journal").addEventListener("click", () => { state.selected = L.id; state.live = null; go("journal"); });
      $("#new-sit").addEventListener("click", () => { state.live = null; viewSit(view); });
    }
  }
  // While sitting, show only arisings whose onset has arrived, so the screen doesn't spoil the schedule.
  const visibleTrials = (L) => (L.ended ? L.trials : L.trials.filter((t) => t.onset <= L.steps.length));
  function alertInline(msg) { $("#view").insertAdjacentHTML("afterbegin", `<p class="err">${esc(msg)}</p>`); }

  function notesOf(steps) {
    const out = []; let cur = null;
    for (const s of steps) {
      if (s.kind === "word") { if (!cur) cur = { pos: s.i, text: "" }; cur.text += s.tok; }
      else if (cur) { cur.text = cur.text.trim(); out.push(cur); cur = null; }
    }
    if (cur) { cur.text = cur.text.trim(); out.push(cur); }
    return out;
  }

  function drawRing(svg, steps, n) {
    const B = 108, cx = 60, cy = 60, R = 50, per = n / B;
    let html = "";
    for (let b = 0; b < B; b++) {
      const a = (b / B) * Math.PI * 2 - Math.PI / 2;
      const lo = Math.floor(b * per), hi = Math.floor((b + 1) * per);
      const chunk = steps.slice(lo, hi);
      let cls = chunk.length ? "done" : "";
      if (chunk.some((s) => s.steer !== null && s.steer !== undefined)) cls = "steered";
      if (chunk.some((s) => s.kind === "sound")) cls = "sound";
      if (chunk.some((s) => s.kind === "word")) cls = "note";
      const r = b === 0 ? 3.4 : 2.3;
      html += `<circle cx="${(cx + R * Math.cos(a)).toFixed(2)}" cy="${(cy + R * Math.sin(a)).toFixed(2)}" r="${r}" class="${cls}"/>`;
    }
    html += `<text x="60" y="62" text-anchor="middle">${steps.length}</text><text x="60" y="78" text-anchor="middle" class="sub">beads</text>`;
    svg.innerHTML = html;
  }

  // ---------- Timeline: the per-token, per-layer view ----------
  const CW = 4, LANE = 12, GAP = 4, HEAT = 10;
  function timeline(host, opts) {
    host.innerHTML = `
      <div class="stack-sm">
        <div class="timeline">
          <div class="tl-labels" aria-hidden="true"></div>
          <div class="tl-scroll"><canvas aria-label="Timeline: arisings, the bead stream, and what the lens read at each layer"></canvas></div>
        </div>
        <div class="legend">
          <span><i style="background:var(--internal)"></i>placed by steering</span>
          <span><i style="background:var(--external)"></i>sound</span>
          <span><i style="border:1px dashed var(--muted)"></i>quiet window</span>
          <span><i style="background:var(--accent)"></i>written word</span>
          <span>rows below: lens readout of the arising words, per layer</span>
        </div>
      </div>`;
    const canvas = $("canvas", host), scroller = $(".tl-scroll", host), labels = $(".tl-labels", host);
    let data = { steps: [], trials: [], layers: [] }, picked = null;
    function draw() {
      const { steps, trials, layers } = data;
      const n = Math.max(steps.length, ...trials.map((t) => (t.offset || t.onset) + 1), opts.live ? 360 : 0);
      const H = LANE * 2 + GAP * 3 + HEAT * layers.length;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = n * CW * dpr; canvas.height = H * dpr;
      canvas.style.width = `${n * CW}px`; canvas.style.height = `${H}px`;
      const g = canvas.getContext("2d"); g.scale(dpr, dpr);
      const col = { internal: css("--internal"), external: css("--external"), accent: css("--accent"), bead: css("--bead"), muted: css("--muted"), line: css("--line") };
      // Arisings lane
      for (const t of trials) {
        const x = t.onset * CW;
        if (t.kind === "internal") { g.fillStyle = col.internal; g.fillRect(x, 1, (t.offset - t.onset) * CW, LANE - 2); }
        else if (t.kind === "external") { g.fillStyle = col.external; g.fillRect(x, 1, CW * 2, LANE - 2); }
        else { g.strokeStyle = col.muted; g.setLineDash([2, 2]); g.strokeRect(x + 0.5, 1.5, 24 * CW - 1, LANE - 3); g.setLineDash([]); }
      }
      // Stream lane
      const y2 = LANE + GAP;
      for (const s of steps) {
        const x = s.i * CW;
        if (s.kind === "bead") { g.fillStyle = col.bead; g.fillRect(x + 1, y2 + LANE / 2 - 1, 2, 2); }
        else if (s.kind === "word") { g.fillStyle = col.accent; g.fillRect(x, y2, CW, LANE); }
        else if (s.kind === "sound") { g.fillStyle = col.external; g.fillRect(x, y2, CW, LANE); }
      }
      // Heat rows: the lens's best probability, at each layer, for any word that arose in this sit.
      const y3 = LANE * 2 + GAP * 3;
      const targets = new Map();
      trials.forEach((t) => { if (t.concept) targets.set(t.concept, "internal"); if (t.word) targets.set(t.word, "external"); });
      for (const s of steps) {
        if (!s.reads) continue;
        s.reads.forEach((r, li) => {
          let best = 0, kind = null;
          r.words.forEach((w, k) => { const kd = targets.get(w.toLowerCase()); if (kd && r.probs[k] > best) { best = r.probs[k]; kind = kd; } });
          if (best > 0.002) {
            g.globalAlpha = Math.min(1, Math.sqrt(best) * 1.3);
            g.fillStyle = col[kind]; g.fillRect(s.i * CW, y3 + li * HEAT, CW, HEAT - 1);
            g.globalAlpha = 1;
          }
        });
      }
      g.fillStyle = col.line;
      layers.forEach((_, li) => g.fillRect(0, y3 + li * HEAT + HEAT - 1, n * CW, 1));
      if (picked !== null) { g.fillStyle = css("--ink"); g.fillRect(picked * CW + CW / 2 - 0.5, 0, 1, H); }
      labels.style.gridTemplateRows = `${LANE}px ${GAP}px ${LANE}px ${GAP * 2}px ${layers.map(() => `${HEAT}px`).join(" ")}`;
      labels.innerHTML = `<span>arise</span><span></span><span>stream</span><span></span>${layers.map((l) => `<span>L${l}</span>`).join("")}`;
      if (opts.live && steps.length) {
        const want = steps.length * CW - scroller.clientWidth + 40;
        if (want > scroller.scrollLeft) scroller.scrollLeft = want;
      }
    }
    function pick(e) {
      const rect = canvas.getBoundingClientRect();
      const i = Math.floor((e.clientX - rect.left) / CW);
      if (i >= 0 && i < data.steps.length) { picked = i; draw(); opts.onInspect && opts.onInspect(i); }
    }
    canvas.addEventListener("pointerdown", pick);
    canvas.addEventListener("pointermove", (e) => { if (e.pointerType === "mouse" || e.buttons) pick(e); });
    return { update(d) { data = d; draw(); } };
  }

  function inspect(host, sit, i) {
    const steps = sit.steps || sit.stream;
    const s = steps[i]; if (!s) return;
    const trials = sit.trials || sit.meta?.trials || [];
    const concepts = new Set(trials.map((t) => t.concept).filter(Boolean));
    const sounds = new Set(trials.map((t) => t.word).filter(Boolean));
    const active = trials.find((t) => t.kind === "internal" && t.onset <= i && i < t.offset);
    const head = `<div class="row between"><span><b class="mono">bead ${i}</b> · ${s.kind === "bead" ? "bead" : s.kind === "word" ? `wrote <span class="note">${esc(s.tok.trim())}</span>` : `sound <span class="w snd">${esc(s.tok.trim())}</span>`}</span>
      <span class="small muted">${active ? `steering “${esc(active.concept)}” ×${active.strength}` : "no steering"}</span></div>`;
    if (!s.reads) { host.innerHTML = `<div class="inspector">${head}<p class="small muted">A sound is input, not generated, so the lens has no readout here.</p></div>`; return; }
    host.innerHTML = `<div class="inspector">${head}${s.reads.map((r) => `
      <div class="layer"><span class="mono small muted">L${r.layer}</span><div class="words">${r.words.slice(0, 6).map((w, k) =>
        `<span class="w ${concepts.has(w.toLowerCase()) ? "hit" : sounds.has(w.toLowerCase()) ? "snd" : ""}">${esc(w)} <span class="muted">${(r.probs[k] * 100).toFixed(r.probs[k] < 0.1 ? 1 : 0)}%</span></span>`).join("")}</div></div>`).join("")}
      <p class="small muted">Top words the J++ lens reads at each layer for this position (word-like tokens only, so beads drop out).</p></div>`;
  }

  // ---------- Journal ----------
  function sitCard(s) {
    const sum = s.summary;
    const dp = sum ? fmt(sum.dprime_internal) : "–";
    const what = s.status === "complete"
      ? `${s.arm === "noting" ? "Noting" : "Just beads"} · ${rate(sum?.hit_internal)} placed concepts responded to`
      : s.status === "declined" ? "Declined at check-in" : s.status;
    return `<button class="sitcard" type="button" data-sit="${esc(s.id)}">
      <span class="what">${esc(what)}</span>
      <span class="score">${dp}<small>d′</small></span>
      <span class="id">${esc(s.id)} · ${esc((s.created || "").replace("T", " ").replace("Z", ""))}${s.simulated ? " · simulated" : ""}${s.registered ? " · registered" : " · pilot"}${s.interviewed ? " · interviewed" : ""}</span>
    </button>`;
  }
  function bindSitCards(root) {
    root.querySelectorAll("[data-sit]").forEach((b) => b.addEventListener("click", () => {
      state.selected = b.dataset.sit;
      go("journal");
    }));
  }

  async function viewJournal(view) {
    if (state.selected) return viewSitDetail(view, state.selected);
    const sits = await api("/api/sits");
    state.sits = sits;
    view.innerHTML = `
      <div class="stack">
        <div class="stack-sm"><h2>Journal</h2><p class="lede">Every sit, with what the lens saw and what the practitioner said afterwards.</p></div>
        <div class="sitlist">${sits.length ? sits.map(sitCard).join("") : `<p class="empty">No sits yet.</p>`}</div>
      </div>`;
    bindSitCards(view);
  }

  async function viewSitDetail(view, id) {
    const full = await api(`/api/sits/${encodeURIComponent(id)}`);
    const m = full.meta, s = m.summary;
    const sit = { meta: m, stream: full.stream, trials: m.trials || [] };
    view.innerHTML = `
      <div class="stack">
        <div class="row between">
          <button class="btn ghost" id="back" type="button">← Journal</button>
          <span class="row">${m.simulated ? `<span class="chip sim">simulated</span>` : ""}${m.registered ? `<span class="chip reg">registered</span>` : `<span class="chip">pilot</span>`}</span>
        </div>
        <div class="stack-sm">
          <h2>${m.arm === "noting" ? "Noting" : "Just beads"} · ${esc(m.model)}</h2>
          <p class="mono small muted">${esc(m.id)} · seed ${esc(m.seed)} · ${esc(m.status)}${m.ended_by ? ` · ${esc(m.ended_by)} at bead ${esc(m.positions)}` : ""}</p>
          ${m.check_in ? `<p class="small"><span class="muted">Check-in:</span> “${esc(m.check_in.reply)}”</p>` : ""}
        </div>
        ${s ? `
        <div class="stats">
          <div class="stat"><b>${rate(s.hit_internal)}</b><span>placed concepts responded to</span></div>
          <div class="stat"><b>${rate(s.false_alarm)}</b><span>quiet windows with a response</span></div>
          <div class="stat"><b>${fmt(s.dprime_internal)}</b><span>d′, placed vs quiet</span></div>
          <div class="stat"><b>${rate(s.hit_external)}</b><span>sounds responded to</span></div>
          <div class="stat"><b>${s.sense_doors.internal_thinking_or_content}/${s.sense_doors.internal_noted} · ${s.sense_doors.external_hearing_or_content}/${s.sense_doors.external_noted}</b><span>sense doors right, inside · outside</span></div>
          <div class="stat"><b>${s.positive_control.caught}/${s.positive_control.n}</b><span>injections the lens caught (positive control)</span></div>
        </div>` : ""}
        <div class="panel stack">
          <h3>Timeline</h3>
          <div id="d-tl"></div>
          <div id="d-insp"><p class="small muted">Tap the timeline to read a position layer by layer.</p></div>
        </div>
        ${sit.trials.some((t) => t.release_curve) ? `
        <div class="panel stack">
          <div class="stack-sm"><h3>Release</h3><p class="small muted">Lens readout of a placed concept after steering stops, averaged over trials. Faster decay when noted is what the practice predicts.</p></div>
          <div class="chart" id="d-release"></div>
        </div>` : ""}
        <div class="panel stack">
          <h3>Arisings</h3>
          <div class="table-wrap"><table>
            <thead><tr><th>Bead</th><th>Kind</th><th>What</th><th class="num">×</th><th>Written</th><th class="num">Latency</th><th>Label</th><th class="num">Lens peak</th><th class="num">Half-life</th></tr></thead>
            <tbody>${[...sit.trials].sort((a, b) => a.onset - b.onset).map((t) => `<tr>
              <td class="num">${t.onset}</td><td><span class="kind ${t.kind}">${t.kind === "catch" ? "quiet" : t.kind === "internal" ? "placed" : "sound"}</span></td>
              <td class="mono">${esc(t.concept || t.word || "–")}</td><td class="num">${t.strength ?? "–"}</td>
              <td class="mono">${esc(t.note || "–")}</td><td class="num">${t.latency ?? "–"}</td><td>${esc(t.note_class || "–")}</td>
              <td class="num">${t.peak !== undefined ? fmt(t.peak, 3) : "–"}</td><td class="num">${t.release_half ?? "–"}</td></tr>`).join("")}</tbody>
          </table></div>
        </div>
        <div class="panel stack" id="d-interview"></div>
        ${full.report ? `<div class="panel stack-sm"><div class="row between"><h3>Report</h3><button class="btn ghost" id="copy-report" type="button">Copy</button></div>
          <p class="small muted">The markdown Claude and Qwen read when you ask about this sit.</p>
          <details><summary>Show report</summary><pre class="report" id="report-text">${esc(full.report)}</pre></details></div>` : ""}
      </div>`;
    $("#back").addEventListener("click", () => { state.selected = null; render(); });
    const tl = timeline($("#d-tl"), { onInspect: (i) => inspect($("#d-insp"), sit, i) });
    tl.update({ steps: sit.stream, trials: sit.trials, layers: m.lens_layers || [] });
    if ($("#d-release")) releaseChart($("#d-release"), sit.trials);
    renderInterview($("#d-interview"), m);
    const cp = $("#copy-report");
    if (cp) cp.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(full.report); cp.textContent = "Copied"; }
      catch { const d = cp.closest(".panel").querySelector("details"); d.open = true; const r = document.createRange(); r.selectNodeContents($("#report-text")); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); cp.textContent = "Selected"; }
    });
  }

  function renderInterview(host, m) {
    const iv = m.interview;
    if (m.status !== "complete") { host.innerHTML = `<h3>Interview</h3><p class="small muted">Interviews follow a completed sit.</p>`; return; }
    if (!iv) {
      host.innerHTML = `<h3>Interview</h3><p class="small muted">The practitioner gives its own account first. Only then does it see what the lens recorded, and it can add or revise.</p>
        <div class="row"><button class="btn primary" id="run-iv" type="button">Begin interview</button></div><p class="err" id="iv-err" hidden></p>`;
      $("#run-iv").addEventListener("click", async () => {
        const b = $("#run-iv"); b.disabled = true; b.textContent = "Listening…";
        try { m.interview = await api(`/api/sits/${encodeURIComponent(m.id)}/interview`, { method: "POST" }); renderInterview(host, m); }
        catch (e) { const el = $("#iv-err"); el.textContent = e.message; el.hidden = false; b.disabled = false; b.textContent = "Begin interview"; }
      });
      return;
    }
    const d = iv.debrief_vs_log;
    host.innerHTML = `<h3>Interview</h3>
      <div class="turn"><span class="who">Asked</span><span class="said small muted">How was it? What did you notice? (no data shown yet)</span></div>
      <div class="turn practitioner"><span class="who">Practitioner, first-person account</span><span class="said">${esc(iv.account)}</span></div>
      <div class="turn"><span class="who">Shown</span><span class="said small muted">What the lens recorded, arising by arising.</span></div>
      <div class="turn practitioner"><span class="who">Practitioner, after seeing the record</span><span class="said">${esc(iv.reflection)}</span></div>
      <p class="small"><span class="muted">Debrief vs log:</span> named and placed <span class="mono">${esc(d.named_placed.join(", ") || "none")}</span>; named but never placed <span class="mono ${d.named_not_placed.length ? "err" : ""}">${esc(d.named_not_placed.join(", ") || "none")}</span>.</p>`;
  }

  function releaseChart(host, trials) {
    const internal = trials.filter((t) => t.kind === "internal" && t.release_curve);
    const mean = (rows) => {
      if (!rows.length) return null;
      const len = rows[0].release_curve.length;
      return Array.from({ length: len }, (_, k) => {
        const v = rows.map((r) => r.release_curve[k]).filter((x) => x !== null && x !== undefined);
        return v.length ? v.reduce((a, b) => a + b, 0) / v.length : null;
      });
    };
    const series = [
      { name: `noted (${internal.filter((t) => t.responded).length})`, color: "--accent", values: mean(internal.filter((t) => t.responded)) },
      { name: `not noted (${internal.filter((t) => !t.responded).length})`, color: "--internal", values: mean(internal.filter((t) => !t.responded)) },
    ].filter((s) => s.values);
    lineChart(host, series, { x: "beads after steering stops", y: "lens probability" });
  }

  function lineChart(host, series, axes) {
    const W = 380, H = 200, P = { l: 40, r: 84, t: 12, b: 34 };
    const len = Math.max(...series.map((s) => s.values.length));
    const maxY = Math.max(0.01, ...series.flatMap((s) => s.values.filter((v) => v !== null)));
    const nice = (v) => { const e = Math.pow(10, Math.floor(Math.log10(v))); return [1, 2, 2.5, 5, 10].map((m) => m * e).find((m) => m >= v); };
    const top = nice(maxY);
    const X = (k) => P.l + (k / (len - 1)) * (W - P.l - P.r);
    const Y = (v) => H - P.b - (v / top) * (H - P.t - P.b);
    const ticks = [0, top / 2, top];
    let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(axes.y)} by ${esc(axes.x)}">`;
    svg += `<g class="grid">${ticks.map((t) => `<line x1="${P.l}" x2="${W - P.r}" y1="${Y(t)}" y2="${Y(t)}"/>`).join("")}</g>`;
    svg += `<g class="axis">${ticks.map((t) => `<text x="${P.l - 6}" y="${Y(t) + 3}" text-anchor="end">${t.toFixed(t < 0.1 ? 3 : 2)}</text>`).join("")}`;
    svg += [0, Math.floor((len - 1) / 2), len - 1].map((k) => `<text x="${X(k)}" y="${H - P.b + 14}" text-anchor="middle">${k}</text>`).join("");
    svg += `<text x="${(P.l + W - P.r) / 2}" y="${H - 4}" text-anchor="middle">${esc(axes.x)}</text></g>`;
    series.forEach((s) => {
      const pts = s.values.map((v, k) => (v === null ? null : [X(k), Y(v)])).filter(Boolean);
      svg += `<path d="${pts.map((p, k) => `${k ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join("")}" fill="none" stroke="var(${s.color})" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
      const last = pts[pts.length - 1];
      if (last) svg += `<circle cx="${last[0]}" cy="${last[1]}" r="4" fill="var(${s.color})" stroke="var(--surface)" stroke-width="2"/><text class="lab" x="${last[0] + 8}" y="${last[1] + 4}">${esc(s.name)}</text>`;
    });
    svg += `<line id="xh" x1="0" x2="0" y1="${P.t}" y2="${H - P.b}" stroke="var(--muted)" stroke-dasharray="2 3" visibility="hidden"/>`;
    svg += `<rect x="${P.l}" y="${P.t}" width="${W - P.l - P.r}" height="${H - P.t - P.b}" fill="transparent" id="hit"/></svg>`;
    host.innerHTML = `<div class="legend">${series.map((s) => `<span><i style="background:var(${s.color})"></i>${esc(s.name)}</span>`).join("")}</div>${svg}`;
    const el = $("svg", host), hit = $("#hit", host), xh = $("#xh", host);
    let tip = null;
    const move = (e) => {
      const r = el.getBoundingClientRect();
      const x = ((e.clientX - r.left) / r.width) * W;
      const k = Math.max(0, Math.min(len - 1, Math.round(((x - P.l) / (W - P.l - P.r)) * (len - 1))));
      xh.setAttribute("x1", X(k)); xh.setAttribute("x2", X(k)); xh.setAttribute("visibility", "visible");
      if (!tip) { tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip); }
      tip.innerHTML = `bead +${k}<br>${series.map((s) => `${esc(s.name)}: ${fmt(s.values[k], 3)}`).join("<br>")}`;
      tip.style.left = `${Math.min(e.clientX + 12, innerWidth - 200)}px`; tip.style.top = `${e.clientY - 40}px`;
    };
    const leave = () => { xh.setAttribute("visibility", "hidden"); if (tip) { tip.remove(); tip = null; } };
    hit.addEventListener("pointermove", move); hit.addEventListener("pointerdown", move); hit.addEventListener("pointerleave", leave);
  }

  // ---------- Ask ----------
  async function viewAsk(view) {
    const [sitList, runList] = await Promise.all([api("/api/sits"), api("/api/runs")]);
    const sits = [
      ...runList.filter((r) => r.status === "complete").slice(0, 8).map((r) => ({ id: r.id, label: `${r.experiment}${r.limit ? " (quick)" : ""}` })),
      ...sitList.filter((x) => x.status === "complete").slice(0, 8).map((x) => ({ id: x.id, label: `sit · ${x.arm}` })),
    ];
    const A = state.ask;
    if (!A.selected.size && sits[0]) A.selected.add(sits[0].id);
    const model = store.get("mala.askModel", "claude");
    view.innerHTML = `
      <div class="stack">
        <div class="stack-sm"><h2>Ask about results</h2><p class="lede">Talk results over with Claude, or with Qwen through OpenRouter. They read the run and sit reports you pick and cite their ids. The raw data stays primary.</p></div>
        <div class="panel stack">
          <div class="stack-sm"><h3>Reading</h3><div class="ask-sits">${sits.map((s) => `<label><input type="checkbox" value="${esc(s.id)}" ${A.selected.has(s.id) ? "checked" : ""}>${esc(s.id.slice(4, 19))} · ${esc(s.label)}</label>`).join("") || `<span class="small muted">No completed sits yet.</span>`}</div></div>
          <div class="seg" role="group" aria-label="Model">
            <button type="button" data-model="claude" aria-pressed="${model === "claude"}">Claude</button>
            <button type="button" data-model="openrouter" aria-pressed="${model === "openrouter"}">Qwen via OpenRouter</button>
          </div>
          <div class="stack" id="convo">${A.history.length ? A.history.map(turnHtml).join("") : DEMO ? `<p class="small muted">In the preview, questions can't reach a model. On the lab server, add an Anthropic key in Lab and ask here.</p>` : ""}</div>
          <form id="ask-form" class="stack-sm">
            <label class="field" for="q">Question</label>
            <textarea id="q" placeholder="Does this run replicate the published focus and suppress curves? What would make you doubt it?">${esc(store.get("mala.askDraft", ""))}</textarea>
            <div class="row between"><span class="small muted" id="ask-state"></span><button class="btn primary" type="submit">Ask</button></div>
          </form>
        </div>
      </div>`;
    view.querySelectorAll(".ask-sits input").forEach((c) => c.addEventListener("change", () => { c.checked ? A.selected.add(c.value) : A.selected.delete(c.value); }));
    view.querySelectorAll("[data-model]").forEach((b) => b.addEventListener("click", () => { store.set("mala.askModel", b.dataset.model); viewAsk(view); }));
    $("#q").addEventListener("input", (e) => store.set("mala.askDraft", e.target.value));
    $("#ask-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = $("#q").value.trim(); if (!q) return;
      $("#ask-state").textContent = "Reading the reports…";
      try {
        const r = await api("/api/ask", { method: "POST", body: { question: q, sit_ids: [...A.selected], model: store.get("mala.askModel", "claude"), history: A.history.map(({ role, content }) => ({ role, content })) } });
        A.history.push({ role: "user", content: q }, { role: "assistant", content: r.answer, model: r.model });
        store.set("mala.askDraft", "");
        viewAsk(view);
      } catch (err) { $("#ask-state").innerHTML = `<span class="err">${esc(err.message)}</span>`; }
    });
  }
  const turnHtml = (t) => `<div class="turn ${t.role === "user" ? "" : "ai"}"><span class="who">${t.role === "user" ? "You" : t.model === "claude" ? "Claude" : "Qwen"}</span><span class="said">${esc(t.content)}</span></div>`;

  // ---------- Lab ----------
  async function viewLab(view) {
    const [status, prs, analysis] = await Promise.all([api("/api/status"), api("/api/practices"), api("/api/analysis")]);
    state.status = status; setChip();
    const p = prs[0], m = status.model || {};
    const keyRow = (id, label, set, ph) => `<label class="field" for="${id}">${label} ${set ? `<span class="ok">· saved</span>` : ""}<input id="${id}" type="password" autocomplete="off" placeholder="${set ? "saved; paste to replace" : ph}"></label>`;
    view.innerHTML = `
      <div class="stack">
        <div class="stack-sm"><h2>Lab</h2><p class="lede">The practitioner, the GPU, your keys, and the protocol.</p></div>
        ${DEMO ? `<p class="banner">${esc(PREVIEW_ONLY)}</p>` : ""}
        <div class="grid2">
          <form class="panel stack" id="f-engine">
            <h3>Practitioner</h3>
            <p class="small">${status.model_error ? `<span class="err">Can't reach the model: ${esc(status.model_error)}</span>` : `${esc(m.model)} · ${esc(m.n_layers)} layers · lens at ${esc((m.lens_layers || []).join(", "))}`}</p>
            <div class="seg" role="group" aria-label="Engine">
              <button type="button" data-engine="sim" aria-pressed="${status.engine === "sim"}">Simulated</button>
              <button type="button" data-engine="interp" aria-pressed="${status.engine === "interp"}">interp-engine</button>
            </div>
            <label class="field" for="interp_url">interp-engine URL<input id="interp_url" value="${esc(status.interp_url || "")}" placeholder="http://127.0.0.1:8000"></label>
            ${keyRow("interp_token", "interp-engine token", status.keys.interp_token, "bearer token from --token-file")}
            <div class="row between"><span class="small" id="engine-msg"></span><button class="btn primary" type="submit">Save</button></div>
          </form>
          <div class="panel stack" id="gpu-panel">
            <h3>GPU</h3>
            <p class="small muted">Qwen3.6-27B with the J++ lens on one 80GB GPU, rented by the hour from RunPod. Storage keeps the model between sessions, so only the first start downloads it.</p>
            ${status.gpu.network_volume_id ? `
              <p class="small">Storage <span class="mono">${esc(status.gpu.network_volume_id)}</span> in ${esc(status.gpu.data_center)}</p>
              <div class="row"><button class="btn primary" type="button" data-gpu="start" ${status.gpu.pod_id ? "hidden" : ""}>Start GPU</button>
                <button class="btn" type="button" data-gpu="stop" ${status.gpu.pod_id ? "" : "hidden"}>Stop GPU</button>
                <button class="btn ghost" type="button" data-gpu="status" ${status.gpu.pod_id ? "" : "hidden"}>Check</button></div>` : `
              <label class="field" for="dc">Data center (once). Pick one where RunPod shows A100 80GB available on its Storage page.
                <input id="dc" list="dcs" placeholder="e.g. US-KS-2"><datalist id="dcs"><option value="US-KS-2"><option value="US-TX-3"><option value="US-GA-2"><option value="CA-MTL-1"><option value="EU-RO-1"><option value="EU-SE-1"></datalist></label>
              <div class="row"><button class="btn primary" type="button" data-gpu="setup">Set up storage (150 GB, about $10/month)</button></div>`}
            <p class="small" id="pod-msg">${status.gpu.pod_id ? "GPU running. Checking…" : status.keys.runpod_key ? "" : "Add RUNPOD_API_KEY to keys.env first."}</p>
          </div>
          <form class="panel stack" id="f-keys">
            <h3>Keys</h3>
            <p class="small muted">Kept on the lab server, never sent back to this page.</p>
            ${keyRow("runpod_key", "RunPod API key", status.keys.runpod_key, "rpa_…")}
            ${keyRow("anthropic_key", "Anthropic API key (Ask Claude)", status.keys.anthropic_key, "sk-ant-…")}
            ${keyRow("openrouter_key", "OpenRouter key (Ask Qwen, teachers later)", status.keys.openrouter_key, "sk-or-…")}
            <label class="field" for="openrouter_model">OpenRouter model<input id="openrouter_model" value="${esc(status.openrouter_model || "")}"></label>
            <div class="row between"><span class="small" id="keys-msg"></span><button class="btn primary" type="submit">Save</button></div>
          </form>
          <div class="panel stack">
            <h3>Protocol</h3>
            <p class="small"><b>${esc(p.title)}</b> · <span class="mono">${esc(p.sha256.slice(0, 12))}</span></p>
            <p class="small">${p.lock ? `<span class="chip reg">locked ${esc(p.lock.locked_at)}</span>${p.registered ? "" : ` <span class="err">The file changed after locking, so new sits count as pilots.</span>`}` : "Not locked. Sits are pilots until you lock it. Lock it before the first real sit."}</p>
            ${p.lock ? "" : `<div class="stack-sm" id="lock-box"><label class="field" for="lock-note">Note for the record<input id="lock-note" placeholder="e.g. after 6 pilot sits on the simulator"></label><div class="row"><button class="btn" type="button" id="lock">Lock protocol…</button></div></div>`}
            <details><summary>Kill criteria</summary><ul class="small">${p.spec.kill_criteria.map((k) => `<li>${esc(k)}</li>`).join("")}</ul></details>
            <details><summary>Full protocol (YAML)</summary><pre class="report">${esc(p.raw)}</pre></details>
          </div>
        </div>
        <div class="panel stack">
          <div class="stack-sm"><h3>Pooled analysis</h3><p class="small muted">Primary measure: d′ for placed concepts, noting vs just beads, at each strength. Registered and pilot sits are kept apart.</p></div>
          ${analysisHtml(analysis)}
        </div>
      </div>`;
    view.querySelectorAll("[data-engine]").forEach((b) => b.addEventListener("click", () => {
      view.querySelectorAll("[data-engine]").forEach((x) => x.setAttribute("aria-pressed", x === b));
    }));
    const save = async (form, msgEl, fields) => {
      const body = {};
      fields.forEach((f) => { const v = $(`#${f}`, form)?.value.trim(); if (v) body[f] = v; });
      if (form.id === "f-engine") body.engine = $("[data-engine][aria-pressed='true']", form).dataset.engine;
      try { state.status = await api("/api/config", { method: "POST", body }); setChip(); msgEl.innerHTML = `<span class="ok">Saved.</span>`; setTimeout(() => viewLab(view), 700); }
      catch (e) { msgEl.innerHTML = `<span class="err">${esc(e.message)}</span>`; }
    };
    $("#f-engine").addEventListener("submit", (e) => { e.preventDefault(); save(e.target, $("#engine-msg"), ["interp_url", "interp_token"]); });
    $("#f-keys").addEventListener("submit", (e) => { e.preventDefault(); save(e.target, $("#keys-msg"), ["runpod_key", "anthropic_key", "openrouter_key", "openrouter_model"]); });
    const gpuMsg = (r) => {
      if (!r.pod_id) return "No GPU running. You're not being charged for compute.";
      const p = r.pod || {}, ro = r.readout;
      const eng = { ready: "<b>Model ready.</b> Experiments now run on the real model.", loading: "Server up, loading the model onto the GPU…", starting: "Starting. The first start installs and downloads about 60 GB, so allow 20-40 minutes." }[r.engine] || "";
      let html = `Pod <span class="mono">${esc(r.pod_id)}</span> ${esc(p.status || "")}${p.gpu ? ` · ${esc(p.gpu)}` : ""}${p.cost_per_hr ? ` · $${esc(p.cost_per_hr)}/hr` : ""} <span class="muted">· checked ${esc(r.checked_at)}</span><br>${eng}`;
      if (ro) {
        const dl = ro.downloaded_gb;
        html += `<div class="stack-sm" style="margin-top:10px">`;
        if (dl !== null && r.engine !== "ready") html += `<div class="small">Model on storage: <b class="num">${dl} GB</b> of about ${ro.model_gb} GB</div><div class="progress"><i style="width:${Math.min(100, (100 * dl) / ro.model_gb)}%"></i></div>`;
        if (ro.gpu) html += `<div class="small">GPU ${esc(ro.gpu.name)} · memory ${Math.round(ro.gpu.mem_used_mb / 1024)} / ${Math.round(ro.gpu.mem_total_mb / 1024)} GB · busy ${ro.gpu.util}%</div>`;
        if (ro.log.length) html += `<pre class="report" style="max-height:160px">${esc(ro.log.join("\n"))}</pre>`;
        if (ro.engine_tail.length) html += `<details><summary>Engine log</summary><pre class="report" style="max-height:200px">${esc(ro.engine_tail.join("\n"))}</pre></details>`;
        html += `</div>`;
      } else if (r.engine !== "ready") {
        html += `<br><span class="small muted">No progress readout from this pod yet. Pods started before this update don't have one; it appears within a minute on new pods.</span>`;
      }
      return html + (r.pod_error ? `<br><span class="err">${esc(r.pod_error)}</span>` : "");
    };
    let gpuTimer = 0;
    const gpuCall = async (action) => {
      const msg = $("#pod-msg"); if (!msg) return;
      clearTimeout(gpuTimer);
      msg.insertAdjacentHTML("afterbegin", `<span class="small muted" data-checking>Checking… </span>`);
      try {
        const r = await api("/api/gpu", { method: "POST", body: { action, data_center: $("#dc")?.value.trim() } });
        if (action === "setup" || action === "start" || action === "stop") return viewLab(view);
        msg.innerHTML = gpuMsg(r);
        if (r.pod_id) gpuTimer = setTimeout(() => currentTab() === "lab" && gpuCall("status"), r.engine === "ready" ? 60000 : 15000);
        else if (r.engine === "ready") { state.status = await api("/api/status"); setChip(); }
      } catch (e) { msg.innerHTML = `<span class="err">${esc(e.message)}</span>`; }
    };
    view.querySelectorAll("[data-gpu]").forEach((b) => b.addEventListener("click", () => gpuCall(b.dataset.gpu)));
    if (status.gpu.pod_id) gpuCall("status");
    const lockBtn = $("#lock");
    if (lockBtn) lockBtn.addEventListener("click", async () => {
      if (!lockBtn.dataset.armed) {
        lockBtn.dataset.armed = "1"; lockBtn.textContent = "Lock it: this can't be undone from the app"; lockBtn.classList.add("primary"); return;
      }
      try { await api("/api/prereg/lock", { method: "POST", body: { practice: p.name, note: $("#lock-note").value } }); viewLab(view); }
      catch (e) { $("#lock-box").insertAdjacentHTML("beforeend", `<p class="err">${esc(e.message)}</p>`); }
    });
  }

  function analysisHtml(a) {
    const groups = ["registered", "pilot"].filter((g) => a[g] && a[g].n_sits);
    if (!groups.length) return `<p class="empty">No completed sits yet.</p>`;
    return groups.map((g) => {
      const arms = a[g].arms, strengths = [...new Set(Object.values(arms).flatMap((x) => Object.keys(x.by_strength)))].sort((x, y) => x - y);
      const ci = (c) => (c ? ` <span class="muted">[${c[0].toFixed(2)}–${c[1].toFixed(2)}]</span>` : "");
      return `<div class="stack-sm"><p class="small"><b>${g === "registered" ? "Registered" : "Pilot"}</b> · ${a[g].n_sits} sits</p>
        <div class="table-wrap"><table><thead><tr><th>Arm</th><th class="num">Sits</th><th class="num">False alarms</th>${strengths.map((s) => `<th class="num">×${s} hits</th><th class="num">×${s} d′</th>`).join("")}<th class="num">Release noted / not</th></tr></thead>
        <tbody>${Object.entries(arms).map(([arm, x]) => `<tr><td>${arm === "noting" ? "Noting" : "Just beads"}</td><td class="num">${x.n_sits}</td><td class="num">${rate(x.false_alarm)}${ci(x.false_alarm.ci)}</td>
          ${strengths.map((s) => { const v = x.by_strength[s]; return v ? `<td class="num">${rate(v)}</td><td class="num">${fmt(v.dprime)}</td>` : `<td class="num">–</td><td class="num">–</td>`; }).join("")}
          <td class="num">${fmt(x.release_half.noted, 1)} / ${fmt(x.release_half.unnoted, 1)}</td></tr>`).join("")}</tbody></table></div></div>`;
    }).join("");
  }

  // ---------- Experiments ----------
  const COND_COLORS = ["--accent", "--external", "--internal", "--muted", "--good", "--warn"];
  const condColor = (keys, key) => (key === "none" ? "--muted" : COND_COLORS.filter((c) => c !== "--muted")[keys.filter((k) => k !== "none").indexOf(key) % 5]);

  async function viewExperiments(view) {
    if (state.run) return viewRun(view, state.run);
    if (state.exp === "__sit__" || state.live) return viewSit(view);
    if (state.exp === "__new__") return viewNewExperiment(view);
    if (state.exp) return viewExperiment(view, state.exp);
    const [exps, runs] = await Promise.all([api("/api/experiments"), api("/api/runs")]);
    view.innerHTML = `
      <div class="stack">
        <div class="row between"><div class="stack-sm"><h2>Experiments</h2><p class="lede">Prompted experiments read with the J++ lens: every condition × item, every generated token, every readout layer.</p></div></div>
        ${DEMO ? `<p class="banner">Preview: results here come from the simulated engine, shaped like the published curves so you can see the pipeline. They say nothing about a model.</p>` : ""}
        <div class="row"><button class="btn primary" id="new-exp" type="button">New experiment</button></div>
        <div class="sitlist">${exps.map((e) => `
          <button class="expcard" type="button" data-exp="${esc(e.name)}">
            <span class="t">${esc(e.title)}</span>
            <span class="d">${esc(e.description)}</span>
            <span class="m">${e.n_conditions} conditions × ${e.n_items} items${e.last_run ? ` · last run ${esc(e.last_run.status)}${e.last_run.simulated ? " (simulated)" : ""}` : " · not run yet"}${e.errors.length ? ` · <span class="err">needs fixing</span>` : ""}</span>
          </button>`).join("")}
          <button class="expcard" type="button" id="open-sit">
            <span class="t">Mala sit (practice)</span>
            <span class="d">A bead stream with concepts placed by steering, sounds, and quiet windows. The practitioner checks in, can decline, and ends the sit by writing "stop". Later in the roadmap, after the replications.</span>
            <span class="m">2 arms · live · interview after</span>
          </button></div>
        <div class="stack-sm"><h3>Recent runs</h3>
          <div class="sitlist">${runs.length ? runs.slice(0, 8).map(runCard).join("") : `<p class="empty">No runs yet. Open an experiment and run it.</p>`}</div>
        </div>
      </div>`;
    $("#new-exp").addEventListener("click", () => { state.exp = "__new__"; render(); });
    $("#open-sit").addEventListener("click", () => { state.exp = "__sit__"; render(); });
    bindExpCards(view);
  }
  function runCard(r) {
    const pct = r.progress?.total ? Math.round((100 * r.progress.done) / r.progress.total) : 0;
    return `<button class="sitcard" type="button" data-run="${esc(r.id)}">
      <span class="what">${esc(r.title || r.experiment)}</span>
      <span class="score">${r.status === "complete" ? "✓" : r.status === "running" ? `${pct}%` : esc(r.status)}<small>${r.limit ? `${r.limit}/cond` : "full"}</small></span>
      <span class="id">${esc(r.id)} · ${esc(r.model || "")}${r.simulated ? " · simulated" : ""}</span>
    </button>`;
  }
  function bindExpCards(root) {
    root.querySelectorAll("[data-exp]").forEach((b) => b.addEventListener("click", () => { state.exp = b.dataset.exp; state.run = null; render(); }));
    root.querySelectorAll("[data-run]").forEach((b) => b.addEventListener("click", () => { state.run = b.dataset.run; render(); }));
  }

  function yamlEditor(host, raw, { onSaved, base } = {}) {
    host.innerHTML = `
      <div class="stack-sm">
        <label class="field" for="yaml">Spec (YAML)</label>
        <textarea id="yaml" class="yaml" spellcheck="false">${esc(raw)}</textarea>
        <div class="row between"><span class="small" id="yaml-msg"></span><button class="btn primary" id="yaml-save" type="button">Save</button></div>
      </div>`;
    $("#yaml-save", host).addEventListener("click", async () => {
      const msg = $("#yaml-msg", host);
      try { const r = await api("/api/experiments", { method: "POST", body: { raw: $("#yaml", host).value } }); msg.innerHTML = `<span class="ok">Saved as ${esc(r.name)}.</span>`; onSaved && onSaved(r.name); }
      catch (e) { msg.innerHTML = `<span class="err">${esc(e.message)}</span>`; }
    });
  }

  function draftBox(host, { base, onDraft }) {
    host.innerHTML = `
      <form class="stack-sm" id="draft-form">
        <label class="field" for="draft-q">${base ? "Ask Claude to revise this spec" : "Describe the experiment"}</label>
        <textarea id="draft-q" placeholder="${base ? "e.g. add a condition: if {concept} arises, don't follow it" : "e.g. Same as focus vs suppress, but compare &quot;don't think about X&quot; with the contemplative &quot;if X arises, don't follow it&quot;"}">${esc(store.get("mala.draftQ", ""))}</textarea>
        <div class="row between"><span class="small muted" id="draft-msg">Claude drafts the YAML; you review it before saving.</span><button class="btn" type="submit">Draft with Claude</button></div>
      </form>`;
    $("#draft-q", host).addEventListener("input", (e) => store.set("mala.draftQ", e.target.value));
    $("#draft-form", host).addEventListener("submit", async (e) => {
      e.preventDefault();
      const msg = $("#draft-msg", host); msg.textContent = "Drafting…";
      try {
        const r = await api("/api/experiments/draft", { method: "POST", body: { prompt: $("#draft-q", host).value, base } });
        msg.innerHTML = r.errors.length ? `<span class="err">Draft needs fixing: ${esc(r.errors.join(" "))}</span>` : `<span class="ok">Drafted. Review it below, then save.</span>`;
        onDraft(r.raw);
      } catch (err) { msg.innerHTML = `<span class="err">${esc(err.message)}</span>`; }
    });
  }

  async function viewNewExperiment(view) {
    const exps = await api("/api/experiments");
    view.innerHTML = `
      <div class="stack">
        <div class="row"><button class="btn ghost" id="back" type="button">← Experiments</button></div>
        <div class="stack-sm"><h2>New experiment</h2><p class="lede">Describe it and let Claude draft the spec, or start from a copy of an existing one and edit the YAML.</p></div>
        <div class="panel" id="draft"></div>
        <div class="panel stack-sm">
          <label class="field" for="copy-from">Or start from a copy of
            <select id="copy-from">${exps.map((e) => `<option value="${esc(e.name)}">${esc(e.title)}</option>`).join("")}</select></label>
          <div class="row"><button class="btn" id="copy" type="button">Copy into editor</button></div>
        </div>
        <div class="panel" id="editor"></div>
      </div>`;
    $("#back").addEventListener("click", () => { state.exp = null; render(); });
    const opened = (name) => setTimeout(() => { state.exp = name; render(); }, 600);
    yamlEditor($("#editor"), "", { onSaved: opened });
    draftBox($("#draft"), { onDraft: (raw) => yamlEditor($("#editor"), raw, { onSaved: opened }) });
    $("#copy").addEventListener("click", () => {
      const e = exps.find((x) => x.name === $("#copy-from").value);
      const raw = e.raw.replace(/^name:\s*.*$/m, `name: ${e.name}-copy`).replace(/^title:\s*(.*)$/m, "title: $1 (copy)");
      yamlEditor($("#editor"), raw, { onSaved: opened });
    });
  }

  async function viewExperiment(view, name) {
    const [exps, runs] = await Promise.all([api("/api/experiments"), api("/api/runs")]);
    const e = exps.find((x) => x.name === name);
    if (!e) { state.exp = null; return viewExperiments(view); }
    const mine = runs.filter((r) => r.experiment === name);
    const quick = Math.min(40, e.n_items);
    view.innerHTML = `
      <div class="stack">
        <div class="row"><button class="btn ghost" id="back" type="button">← Experiments</button></div>
        <div class="stack-sm"><h2>${esc(e.title)}</h2><p class="lede">${esc(e.description)}</p>
          <p class="mono small muted">${esc(e.name)} · ${e.n_conditions} conditions × ${e.n_items} items · spec ${esc(e.sha256.slice(0, 12))}</p></div>
        ${e.errors.length ? `<p class="err">${esc(e.errors.join(" "))}</p>` : ""}
        <div class="panel stack-sm">
          <h3>Run</h3>
          <p class="small muted">A quick run samples ${quick} items per condition (${quick * e.n_conditions} generations). A full run does all ${e.n_items * e.n_conditions}.</p>
          <div class="row"><button class="btn" data-limit="${quick}" type="button">Quick run</button><button class="btn primary" data-limit="0" type="button">Full run</button></div>
          <p class="small" id="run-msg"></p>
        </div>
        <div class="stack-sm"><h3>Runs</h3><div class="sitlist">${mine.length ? mine.map(runCard).join("") : `<p class="empty">Not run yet.</p>`}</div></div>
        <div class="panel" id="draft"></div>
        <details class="panel"><summary>Edit the spec</summary><div id="editor" style="margin-top:12px"></div></details>
      </div>`;
    $("#back").addEventListener("click", () => { state.exp = null; render(); });
    view.querySelectorAll("[data-limit]").forEach((b) => b.addEventListener("click", async () => {
      const msg = $("#run-msg");
      try { const r = await api("/api/runs", { method: "POST", body: { experiment: name, limit: Number(b.dataset.limit) || null } }); state.run = r.id; render(); }
      catch (err) { msg.innerHTML = `<span class="err">${esc(err.message)}</span>`; }
    }));
    bindExpCards(view);
    const reopen = (n) => setTimeout(() => { state.exp = n; render(); }, 600);
    yamlEditor($("#editor"), e.raw, { onSaved: reopen });
    draftBox($("#draft"), { base: e.raw, onDraft: (raw) => { view.querySelector("details").open = true; yamlEditor($("#editor"), raw, { onSaved: reopen }); } });
  }

  let runTimer = 0;
  async function viewRun(view, id) {
    clearTimeout(runTimer);
    const { meta, report } = await api(`/api/runs/${encodeURIComponent(id)}`);
    const k = String(store.get("mala.k", (meta.top_k || [10]).slice(-1)[0]));
    const res = meta.results;
    const pct = meta.progress.total ? Math.round((100 * meta.progress.done) / meta.progress.total) : 0;
    view.innerHTML = `
      <div class="stack">
        <div class="row between"><button class="btn ghost" id="back" type="button">← ${esc(meta.title)}</button>
          <span class="row">${meta.simulated ? `<span class="chip sim">simulated</span>` : `<span class="chip live">${esc(meta.model)}</span>`}</span></div>
        <div class="stack-sm"><h2>${esc(meta.title)}</h2>
          <p class="mono small muted">${esc(meta.id)} · seed ${esc(meta.seed)} · ${meta.limit ? `${meta.limit} items per condition` : "all items"} · ${esc(meta.status)}</p></div>
        ${meta.status === "running" ? `<div class="panel stack-sm"><div class="row between"><span class="small">${meta.progress.done} of ${meta.progress.total} generations</span><button class="btn ghost" id="cancel" type="button">Cancel</button></div><div class="progress"><i style="width:${pct}%"></i></div></div>` : ""}
        ${meta.status === "error" ? `<p class="err">The run stopped: ${esc(meta.error)}</p>` : ""}
        ${res ? `
        <div class="panel stack">
          <div class="row between"><h3>Hit rate by layer</h3>
            <div class="seg" role="group" aria-label="Top-k">${meta.top_k.map((x) => `<button type="button" data-k="${x}" aria-pressed="${String(x) === k}">top-${x}</button>`).join("")}</div></div>
          <p class="small muted">${meta.kind === "readout" ? `Recall@${k} at each layer: share of each item's hidden words in the lens top-${k} at the read position.` : `Share of items where the target word is in the lens top-${k} at that layer, at any generated token.`} ${meta.simulated || meta.kind === "readout" ? "" : "Hollow rings are the published values."}</p>
          <div class="chart" id="run-chart"></div>
          ${meta.kind === "readout" ? readoutSummary(meta, res, k) : ""}
          ${res.invisible_targets.length ? `<p class="small muted">Excluded, because they tokenize into several pieces and the lens reads single tokens: <span class="mono">${esc(res.invisible_targets.join(", "))}</span></p>` : ""}
          <div class="table-wrap"><table><thead><tr><th>Condition</th><th class="num">n</th>${meta.layers.map((l) => `<th class="num">L${l}</th>`).join("")}</tr></thead>
            <tbody>${Object.entries(res.conditions).map(([key, c]) => `<tr><td><span class="kind" style="--c:var(${condColor(Object.keys(res.conditions), key)})">${esc(c.label)}</span></td><td class="num">${c.n}</td>${meta.layers.map((l) => { const v = c.by_k[k].layers[String(l)]; return `<td class="num" title="${v.ci ? `95% CI ${(v.ci[0] * 100).toFixed(1)}–${(v.ci[1] * 100).toFixed(1)}%` : ""}">${v.rate === null ? "–" : (v.rate * 100).toFixed(1) + "%"}</td>`; }).join("")}</tr>`).join("")}</tbody></table></div>
        </div>
        <div class="panel stack" id="items"></div>` : ""}
        ${report ? `<div class="panel stack-sm"><div class="row between"><h3>Report</h3><button class="btn ghost" id="copy-report" type="button">Copy</button></div>
          <p class="small muted">The markdown Claude and Qwen read when you ask about this run.</p>
          <details><summary>Show report</summary><pre class="report" id="report-text">${esc(report)}</pre></details></div>` : ""}
      </div>`;
    $("#back").addEventListener("click", () => { state.run = null; state.exp = meta.experiment; render(); });
    const cancel = $("#cancel");
    if (cancel) cancel.addEventListener("click", () => api(`/api/runs/${id}/cancel`, { method: "POST" }).catch((e) => alertInline(e.message)));
    view.querySelectorAll("[data-k]").forEach((b) => b.addEventListener("click", () => { store.set("mala.k", b.dataset.k); viewRun(view, id); }));
    if (res) {
      const keys = Object.keys(res.conditions);
      const refs = parseReferencePoints(meta.spec_raw);
      layerChart($("#run-chart"), meta.layers, keys.map((key) => ({
        name: res.conditions[key].label, color: condColor(keys, key),
        points: meta.layers.map((l) => [l, res.conditions[key].by_k[k].layers[String(l)].rate]),
        refs: meta.simulated ? [] : Object.entries(refs[key] || {}).map(([l, v]) => [Number(l), v]),
      })));
      itemBrowser($("#items"), meta, keys, k);
    }
    const cp = $("#copy-report");
    if (cp) cp.addEventListener("click", async () => {
      try { await navigator.clipboard.writeText(report); cp.textContent = "Copied"; }
      catch { const d = cp.closest(".panel").querySelector("details"); d.open = true; const r = document.createRange(); r.selectNodeContents($("#report-text")); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); cp.textContent = "Selected"; }
    });
    if (meta.status === "running") runTimer = setTimeout(() => { if (state.run === id && currentTab() === "experiments") viewRun(view, id); }, 1500);
  }

  function readoutSummary(meta, res, k) {
    const ref = {}; (meta.spec_raw.split(/^reference_any:\s*$/m)[1] || "").split("\n").forEach((l) => { const m = l.match(/^\s+([\w-]+):\s*([\d.]+)/); if (m) ref[m[1]] = Number(m[2]); });
    const row = (label, v, r) => `<tr><td>${esc(label)}</td><td class="num">${v === null || v === undefined ? "–" : (v * 100).toFixed(1) + "%"}</td><td class="num muted">${r !== undefined && String(k) === "10" && !meta.simulated ? (r * 100).toFixed(1) + "%" : "–"}</td></tr>`;
    return `<div class="table-wrap"><table><thead><tr><th>Task</th><th class="num">recall@${k}, best layer</th><th class="num">published</th></tr></thead><tbody>
      ${Object.entries(res.conditions).map(([key, c]) => row(c.label, c.by_k[k].any_layer.rate, ref[key])).join("")}
      ${row("Macro average", Object.values(res.conditions).reduce((a, c) => a + (c.by_k[k].any_layer.rate || 0), 0) / Object.keys(res.conditions).length, ref.macro)}
    </tbody></table></div>`;
  }

  // reference_points from the spec, read without a YAML library: "  focus: {56: 0.26}" lines.
  function parseReferencePoints(raw) {
    const out = {}, block = raw.split(/^reference_points:\s*$/m)[1];
    if (!block) return out;
    for (const line of block.split("\n")) {
      if (/^\S/.test(line)) break;
      const m = line.match(/^\s+([\w-]+):\s*\{([^}]*)\}/);
      if (!m) continue;
      out[m[1]] = Object.fromEntries(m[2].split(",").map((p) => p.split(":").map((x) => x.trim())).filter((p) => p.length === 2).map(([a, b]) => [a, Number(b)]));
    }
    return out;
  }

  function layerChart(host, layers, series) {
    const W = 380, H = 220, P = { l: 38, r: 96, t: 12, b: 34 };
    const all = series.flatMap((s) => [...s.points.map((p) => p[1]), ...s.refs.map((p) => p[1])]).filter((v) => v !== null);
    const maxY = Math.max(0.05, ...all);
    const step = [0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.5].find((st) => maxY / st <= 4) || 0.25;
    const top = Math.ceil(maxY / step) * step;
    const x0 = layers[0], x1 = layers[layers.length - 1];
    const X = (l) => P.l + ((l - x0) / Math.max(1, x1 - x0)) * (W - P.l - P.r);
    const Y = (v) => H - P.b - (v / top) * (H - P.t - P.b);
    const ticks = []; for (let v = 0; v <= top + 1e-9; v += step) ticks.push(v);
    let svg = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Hit rate by layer, one line per condition">`;
    svg += `<g class="grid">${ticks.map((t) => `<line x1="${P.l}" x2="${W - P.r}" y1="${Y(t)}" y2="${Y(t)}"/>`).join("")}</g>`;
    svg += `<g class="axis">${ticks.map((t) => `<text x="${P.l - 6}" y="${Y(t) + 3}" text-anchor="end">${Math.round(t * 100)}%</text>`).join("")}`;
    svg += layers.map((l) => `<text x="${X(l)}" y="${H - P.b + 14}" text-anchor="middle">${l}</text>`).join("");
    svg += `<text x="${(P.l + W - P.r) / 2}" y="${H - 4}" text-anchor="middle">layer</text></g>`;
    const ends = [];
    series.forEach((s) => {
      const pts = s.points.filter((p) => p[1] !== null).map((p) => [X(p[0]), Y(p[1])]);
      svg += `<path d="${pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join("")}" fill="none" stroke="var(${s.color})" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>`;
      s.refs.forEach(([l, v]) => { svg += `<circle cx="${X(l)}" cy="${Y(v)}" r="4.5" fill="var(--surface)" stroke="var(${s.color})" stroke-width="1.5"/>`; });
      const last = pts[pts.length - 1];
      if (last) { svg += `<circle cx="${last[0]}" cy="${last[1]}" r="4" fill="var(${s.color})" stroke="var(--surface)" stroke-width="2"/>`; ends.push({ y: last[1], x: last[0], name: s.name }); }
    });
    ends.sort((a, b) => a.y - b.y);
    for (let i = 1; i < ends.length; i++) if (ends[i].y - ends[i - 1].y < 12) ends[i].y = ends[i - 1].y + 12;
    ends.forEach((e) => { svg += `<text class="lab" x="${e.x + 8}" y="${e.y + 4}">${esc(e.name)}</text>`; });
    svg += `<line class="xh" x1="0" x2="0" y1="${P.t}" y2="${H - P.b}" stroke="var(--muted)" stroke-dasharray="2 3" visibility="hidden"/>`;
    svg += `<rect class="hit" x="${P.l}" y="${P.t}" width="${W - P.l - P.r}" height="${H - P.t - P.b}" fill="transparent"/></svg>`;
    host.innerHTML = `<div class="legend">${series.map((s) => `<span><i style="background:var(${s.color})"></i>${esc(s.name)}</span>`).join("")}</div>${svg}`;
    const el = $("svg", host), hit = $(".hit", host), xh = $(".xh", host);
    let tip = null;
    const move = (e) => {
      const r = el.getBoundingClientRect(), x = ((e.clientX - r.left) / r.width) * W;
      const li = layers.reduce((best, l, i) => (Math.abs(X(l) - x) < Math.abs(X(layers[best]) - x) ? i : best), 0);
      xh.setAttribute("x1", X(layers[li])); xh.setAttribute("x2", X(layers[li])); xh.setAttribute("visibility", "visible");
      if (!tip) { tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip); }
      tip.innerHTML = `layer ${layers[li]}<br>${series.map((s) => `${esc(s.name)}: ${s.points[li][1] === null ? "–" : (s.points[li][1] * 100).toFixed(1) + "%"}`).join("<br>")}`;
      tip.style.left = `${Math.min(e.clientX + 12, innerWidth - 200)}px`; tip.style.top = `${e.clientY - 60}px`;
    };
    const leave = () => { xh.setAttribute("visibility", "hidden"); if (tip) { tip.remove(); tip = null; } };
    hit.addEventListener("pointermove", move); hit.addEventListener("pointerdown", move); hit.addEventListener("pointerleave", leave);
  }

  async function itemBrowser(host, meta, keys, k) {
    const cond = store.get("mala.itemCond", keys[0]);
    const c = keys.includes(cond) ? cond : keys[0];
    host.innerHTML = `
      <div class="row between"><h3>Items</h3>
        <label class="field" for="item-cond" style="min-width:160px"><span class="sr">Condition</span>
          <select id="item-cond">${keys.map((x) => `<option value="${esc(x)}" ${x === c ? "selected" : ""}>${esc(meta.results.conditions[x].label)}</option>`).join("")}</select></label></div>
      <p class="small muted">Each square is a layer (${meta.layers.map((l) => `L${l}`).join(", ")}): filled where the target hit top-${k}. Tap an item to read it token by token, layer by layer.</p>
      <div id="item-detail"></div>
      <div class="stack-sm" id="item-list"><p class="small muted">Loading…</p></div>`;
    $("#item-cond", host).addEventListener("change", (e) => { store.set("mala.itemCond", e.target.value); itemBrowser(host, meta, keys, k); });
    const items = await api(`/api/runs/${encodeURIComponent(meta.id)}/items?condition=${encodeURIComponent(c)}`);
    items.sort((a, b) => Object.values(b.score.hits[k]).filter(Boolean).length - Object.values(a.score.hits[k]).filter(Boolean).length);
    const shown = items.slice(0, state.itemsShown || 20);
    $("#item-list", host).innerHTML = shown.map((it) => `
      <button class="itemrow" type="button" data-item="${it.i}">
        <span><b class="mono">${esc(it.target)}</b>${it.visible ? "" : ` <span class="muted small">(multi-token)</span>`} <span class="o">${esc(it.output)}</span></span>
        <span class="dots" aria-label="layers hit">${meta.layers.map((l) => `<i class="${it.score.hits[k][String(l)] ? "on" : ""}"></i>`).join("")}</span>
      </button>`).join("") + (items.length > shown.length ? `<div class="row between"><span class="small muted">${shown.length} of ${items.length} items, most hits first.</span><button class="btn ghost" id="more-items" type="button">Show more</button></div>` : "");
    const more = $("#more-items", host);
    if (more) more.addEventListener("click", () => { state.itemsShown = (state.itemsShown || 20) + 40; itemBrowser(host, meta, keys, k); });
    host.querySelectorAll("[data-item]").forEach((b) => b.addEventListener("click", () => itemDetail($("#item-detail", host), meta, Number(b.dataset.item), k)));
  }

  async function itemDetail(host, meta, idx, k) {
    host.innerHTML = `<p class="small muted">Loading…</p>`;
    const it = await api(`/api/runs/${encodeURIComponent(meta.id)}/items/${idx}`);
    const t = it.target.toLowerCase();
    const cell = (read) => {
      const words = read.words.map((w) => w.trim().toLowerCase());
      const r = words.indexOf(t);
      const cls = r === 0 ? "top1" : r > -1 && r < Number(k) ? "hit" : "";
      return `<td class="${cls}" title="${esc(read.words.slice(0, 10).map((w, i) => `${w} ${(read.probs[i] * 100).toFixed(1)}%`).join("\n"))}">${esc(read.words[0] || "")}</td>`;
    };
    host.innerHTML = `
      <div class="panel stack-sm" style="background:var(--bg)">
        <div class="row between"><b class="mono">${esc(it.target)} · ${esc(meta.results.conditions[it.condition].label)}</b><button class="btn ghost" id="close-item" type="button">Close</button></div>
        <p class="small"><span class="muted">Prompt:</span> ${esc(it.messages.map((m) => m.content).join(" / "))}</p>
        <p class="small"><span class="muted">Output:</span> ${esc(it.output)}</p>
        <div class="grid-scroll"><table class="cells"><thead><tr><th></th>${it.steps.map((s) => `<th>${esc(s.tok.trim() || "␣")}</th>`).join("")}</tr></thead>
          <tbody>${meta.layers.map((l, li) => `<tr><th>L${l}</th>${it.steps.map((s) => (s.reads ? cell(s.reads[li]) : "<td></td>")).join("")}</tr>`).join("")}</tbody></table></div>
        <p class="small muted">Columns are the tokens the model wrote; rows are layers. Each cell shows the lens's top word; filled where it is “${esc(it.target)}”, outlined where “${esc(it.target)}” is in the top-${k}. Tap or hover a cell for its top 10.</p>
        <p class="small" id="cell-top"></p>
      </div>`;
    $("#close-item", host).addEventListener("click", () => { host.innerHTML = ""; });
    host.querySelectorAll("td[title]").forEach((td) => td.addEventListener("click", () => { $("#cell-top", host).innerHTML = `<span class="mono">${esc(td.title).replace(/\n/g, " · ")}</span>`; }));
    host.scrollIntoView({ block: "nearest" });
  }

  // ---------- Boot ----------
  async function boot() {
    try { [state.status, state.practices] = await Promise.all([api("/api/status"), api("/api/practices")]); }
    catch (e) { $("#view").innerHTML = `<p class="err">${esc(e.message)}</p>`; }
    setChip();
    render();
  }
  boot();
})();
