// Copyright (C) 1978-2026 by N.Tsuda
/* ── App (SPA ルーター + ビュー) ──────── */
const App = {
  game: null,

  init() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('./sw.js').catch(() => {});
    }
    window.addEventListener('hashchange', () => this.route());
    this.route();
  },

  route() {
    const hash = location.hash || '#/';
    const user = Auth.currentUser();

    if (!user && hash !== '#/' && hash !== '#/register' && hash !== '#/rules') {
      location.hash = '#/';
      return;
    }

    if      (hash.startsWith('#/register'))   this._renderRegister();
    else if (hash.startsWith('#/account'))    this._renderAccount();
    else if (hash.startsWith('#/game'))       this._renderGame();
    else if (hash.startsWith('#/highscores')) this._renderHighScores();
    else if (hash.startsWith('#/rules'))      this._renderRules();
    else                                       this._renderTop();
  },

  _html(html) {
    document.getElementById('app').innerHTML = html;
  },

  /* ── ナビゲーションバー ─────────── */
  _nav(active) {
    return `
      <nav class="nav-bar">
        <div class="nav-item ${active==='home'       ?'active':''}" onclick="App._go('home')">
          <span class="nav-icon">🏠</span>ホーム
        </div>
        <div class="nav-item ${active==='game'       ?'active':''}" onclick="App._go('game')">
          <span class="nav-icon">🎮</span>ゲーム
        </div>
        <div class="nav-item ${active==='rules'      ?'active':''}" onclick="App._go('rules')">
          <span class="nav-icon">📖</span>ルール
        </div>
        <div class="nav-item ${active==='highscores' ?'active':''}" onclick="App._go('highscores')">
          <span class="nav-icon">🏆</span>スコア
        </div>
        <div class="nav-item ${active==='account'    ?'active':''}" onclick="App._go('account')">
          <span class="nav-icon">👤</span>アカウント
        </div>
      </nav>`;
  },

  _go(dest) {
    if (dest === 'game') {
      if (!this.game || this.game.phase === 'gameover') this.game = new GameState();
      location.hash = '#/game';
    } else if (dest === 'home')       { location.hash = '#/'; }
    else if (dest === 'rules')        { location.hash = '#/rules'; }
    else if (dest === 'highscores')   { location.hash = '#/highscores'; }
    else if (dest === 'account')      { location.hash = '#/account'; }
  },

  /* ═══════════════════════════════════
     トップページ
  ═══════════════════════════════════ */
  _renderTop() {
    const user = Auth.currentUser();
    if (!user) { this._renderLogin(); return; }

    this._html(`
      <div class="screen">
        <div class="page-header">
          <div class="page-title">ISKANDAL</div>
          <div class="page-subtitle">イスカンダルのトーフ屋ゲーム</div>
          <div class="page-copyright">Copyright (C) 1978-2026 by N.Tsuda</div>
          <div class="page-copyright">Ported with &quot;Claude Code (Sonnet 4.6)&quot;</div>
        </div>
        <div class="card ani" style="text-align:center;padding:20px 16px">
          <div style="position:relative;display:inline-block;width:100%;max-width:360px;margin-bottom:12px">
            <img src="images/hero.png" style="width:100%;border-radius:16px;display:block">
            <div style="position:absolute;bottom:0;left:0;right:0;padding:8px 8px 14px;border-radius:0 0 16px 16px;background:linear-gradient(transparent,rgba(8,3,18,0.72));text-align:center;font-style:italic;font-size:0.82rem;letter-spacing:0.06em;color:#f0c840;text-shadow:0 1px 6px rgba(0,0,0,0.9)">
              Sell your TOFU, Reach your EARTH
            </div>
          </div>
          <div class="catchphrase">トーフを売って、地球に還ろう</div>
          <p style="color:var(--text-dim);font-size:.85rem;margin:12px 0 16px">
            ユーザー: <span style="color:var(--accent)">${this._esc(user.id)}</span>
          </p>
          <button class="btn btn-primary" onclick="App._startGame()">ゲームスタート</button>
          <button class="btn btn-secondary mt-8" onclick="App._go('rules')">遊び方</button>
        </div>
      </div>
      ${this._nav('home')}
    `);
  },

  _startGame() {
    this.game = new GameState();
    location.hash = '#/game';
  },

  /* ── ログインフォーム ─────────── */
  _renderLogin(err = '') {
    this._html(`
      <div class="screen">
        <div class="page-header">
          <div class="page-title">ISKANDAL</div>
          <div class="page-subtitle">イスカンダルのトーフ屋ゲーム</div>
          <div class="page-copyright">Copyright (C) 1978-2026 by N.Tsuda</div>
          <div class="page-copyright">Ported with &quot;Claude Code (Sonnet 4.6)&quot;</div>
        </div>
        ${err ? `<div class="msg msg-error">${err}</div>` : ''}
        <div class="card ani">
          <div class="card-title">ログイン</div>
          <div class="form-group">
            <label class="form-label">ユーザーID</label>
            <input class="form-input" id="uid" type="text" autocomplete="username" placeholder="ユーザーID">
          </div>
          <div class="form-group">
            <label class="form-label">パスワード</label>
            <input class="form-input" id="pass" type="password" autocomplete="current-password" placeholder="パスワード">
          </div>
          <button class="btn btn-primary" id="btn-login">ログイン</button>
        </div>
        <div class="text-center mt-8">
          <a class="link" onclick="location.hash='#/register'">アカウント登録はこちら →</a>
        </div>
      </div>
    `);

    const doLogin = async () => {
      const btn = document.getElementById('btn-login');
      btn.disabled = true;
      try {
        await Auth.login(
          document.getElementById('uid').value.trim(),
          document.getElementById('pass').value
        );
        this._renderTop();
      } catch (e) {
        this._renderLogin(e.message);
      }
    };

    document.getElementById('btn-login').onclick = doLogin;
    document.getElementById('pass').addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });
  },

  /* ═══════════════════════════════════
     アカウント登録画面
  ═══════════════════════════════════ */
  _renderRegister(err = '') {
    this._html(`
      <div class="screen">
        <div class="page-header">
          <div class="page-title" style="font-size:1.6rem">アカウント登録</div>
        </div>
        ${err ? `<div class="msg msg-error">${err}</div>` : ''}
        <div class="card ani">
          <div class="card-title">新規アカウント登録</div>
          <div class="form-group">
            <label class="form-label">ユーザーID（3文字以上）</label>
            <input class="form-input" id="uid"   type="text"     autocomplete="username"     placeholder="ユーザーID">
          </div>
          <div class="form-group">
            <label class="form-label">メールアドレス</label>
            <input class="form-input" id="email" type="email"    autocomplete="email"        placeholder="example@mail.com">
          </div>
          <div class="form-group">
            <label class="form-label">パスワード（4文字以上）</label>
            <input class="form-input" id="pass"  type="password" autocomplete="new-password" placeholder="パスワード">
          </div>
          <button class="btn btn-primary" id="btn-reg">登録する</button>
        </div>
        <div class="text-center mt-8">
          <a class="link" onclick="location.hash='#/'">ログインはこちら →</a>
        </div>
      </div>
    `);

    document.getElementById('btn-reg').onclick = async () => {
      const btn = document.getElementById('btn-reg');
      btn.disabled = true;
      try {
        await Auth.register(
          document.getElementById('uid').value.trim(),
          document.getElementById('email').value.trim(),
          document.getElementById('pass').value
        );
        location.hash = '#/';
        this._renderTop();
      } catch (e) {
        this._renderRegister(e.message);
      }
    };
  },

  /* ═══════════════════════════════════
     アカウント設定画面
  ═══════════════════════════════════ */
  _renderAccount(err = '', ok = '') {
    const user = Auth.currentUser();
    if (!user) { location.hash = '#/'; return; }

    this._html(`
      <div class="screen">
        <div class="page-header">
          <div class="page-title" style="font-size:1.5rem">アカウント設定</div>
        </div>
        ${err ? `<div class="msg msg-error">${err}</div>` : ''}
        ${ok  ? `<div class="msg msg-success">${ok}</div>` : ''}
        <div class="card ani">
          <div class="card-title">アカウント情報</div>
          <p style="font-size:.85rem;color:var(--text-dim)">
            ユーザーID: <span style="color:var(--text)">${this._esc(user.id)}</span>
          </p>
          <p style="font-size:.85rem;color:var(--text-dim);margin-top:6px">
            メールアドレス: <span style="color:var(--text)">${this._esc(user.email)}</span>
          </p>
        </div>
        <div class="card ani">
          <div class="card-title">アカウント削除</div>
          <p class="hint" style="margin-bottom:10px">削除するには現在のパスワードを入力してください。</p>
          <div class="form-group">
            <input class="form-input" id="del-pass" type="password" placeholder="現在のパスワード">
          </div>
          <button class="btn btn-danger" id="btn-del">アカウントを削除する</button>
        </div>
        <div class="card ani">
          <div class="card-title">ログアウト</div>
          <button class="btn btn-secondary" id="btn-logout">ログアウトする</button>
        </div>
        <button class="btn btn-secondary" onclick="location.hash='#/'" style="margin-top:4px">← 戻る</button>
      </div>
      ${this._nav('account')}
    `);

    document.getElementById('btn-logout').onclick = () => {
      Auth.logout();
      location.hash = '#/';
      this._renderTop();
    };

    document.getElementById('btn-del').onclick = async () => {
      if (!confirm('本当にアカウントを削除しますか？この操作は取り消せません。')) return;
      const btn = document.getElementById('btn-del');
      btn.disabled = true;
      try {
        await Auth.deleteAccount(user.id, document.getElementById('del-pass').value);
        location.hash = '#/';
        this._renderTop();
      } catch (e) {
        this._renderAccount(e.message);
      }
    };
  },

  /* ═══════════════════════════════════
     ゲーム画面
  ═══════════════════════════════════ */
  _renderGame() {
    if (!this.game) this.game = new GameState();
    const g = this.game;

    const pPct = Math.min(100, (g.playerMoney   / GOAL) * 100).toFixed(1);
    const cPct = Math.min(100, (g.computerMoney / GOAL) * 100).toFixed(1);

    const moneyCard = `
      <div class="card">
        <div class="card-title">所持金（目標: ${GOAL.toLocaleString()}円）</div>
        <div class="money-row">
          <span class="money-label">あなた</span>
          <div class="money-bar"><div class="money-bar-fill player"   style="width:${pPct}%"></div></div>
          <span class="money-amount player">${g.playerMoney.toLocaleString()}円</span>
        </div>
        <div class="money-row">
          <span class="money-label">相手</span>
          <div class="money-bar"><div class="money-bar-fill computer" style="width:${cPct}%"></div></div>
          <span class="money-amount computer">${g.computerMoney.toLocaleString()}円</span>
        </div>
      </div>`;

    let body = '';
    if      (g.phase === 'input')    body = this._gameInput(g);
    else if (g.phase === 'reveal')   body = this._gameReveal(g);
    else if (g.phase === 'result')   body = this._gameResult(g);
    else if (g.phase === 'gameover') body = this._gameOver(g);

    this._html(`
      <div class="game-screen">
        <div class="day-badge"><span class="day-badge-inner">DAY ${g.day}</span></div>
        ${moneyCard}
        ${body}
      </div>
      ${this._nav('game')}
    `);

    this._bindGame(g);
  },

  _weatherForecast(w) {
    return ['sunny','cloudy','rainy'].map(k => {
      const wi = WEATHER_INFO[k];
      return `
        <div class="weather-item ${wi.cls}">
          <span class="w-icon">${wi.icon}</span>
          <span class="w-name">${wi.label}</span>
          <div class="w-bar-bg"><div class="w-bar-fill" style="width:${w[k]}%"></div></div>
          <span class="w-pct">${w[k]}%</span>
          <span class="w-demand">最大${wi.demand}個</span>
        </div>`;
    }).join('');
  },

  _gameInput(g) {
    const max = g.playerMax();
    return `
      <div class="card ani">
        <div class="card-title">明日の天気予報</div>
        ${this._weatherForecast(g.weather)}
      </div>
      <div class="card ani">
        <div class="card-title">トーフを何個作りますか？（最大 ${max}個）</div>

        <div style="display:flex;gap:10px;align-items:center;margin-bottom:4px">
          <button class="btn-zero" id="btn-zero">C</button>
          <input class="form-input" id="inp-tofu" type="number"
            inputmode="numeric" min="0" max="${max}" value="0"
            style="flex:1;font-size:1.4rem;text-align:center">
          <button class="btn-max" id="btn-max">MAX<br><span style="font-size:.7rem">${max}個</span></button>
        </div>

        <input type="range" class="tofu-slider" id="tofu-slider" min="0" max="${max}" value="0">

        <div class="adj-btns">
          <button class="adj-btn" data-delta="-100">−100</button>
          <button class="adj-btn" data-delta="-10">−10</button>
          <button class="adj-btn" data-delta="-1">−1</button>
          <button class="adj-btn" data-delta="1">＋1</button>
          <button class="adj-btn" data-delta="10">＋10</button>
          <button class="adj-btn" data-delta="100">＋100</button>
        </div>

        <button class="btn btn-primary" id="btn-make" style="margin-top:14px">作る</button>
        <p class="hint">仕入れ ${TOFU_COST}円/個 → 販売 ${TOFU_PRICE}円/個</p>
      </div>
      <button class="btn btn-giveup ani" id="btn-giveup">ギブアップ</button>`;
  },

  _gameReveal(g) {
    return `
      <div class="card ani">
        <div class="card-title">明日の天気予報</div>
        ${this._weatherForecast(g.weather)}
      </div>
      <div class="card ani">
        <div class="card-title">今日の生産数</div>
        <div class="prod-row">
          <span class="prod-label">あなた</span>
          <span class="prod-value player">${g.playerTofu}個</span>
        </div>
        <div class="prod-row">
          <span class="prod-label">相手（コンピュータ）</span>
          <span class="prod-value computer">${g.computerTofu}個</span>
        </div>
      </div>
      <button class="btn btn-primary ani" id="btn-reveal">次の日へ →</button>
      <button class="btn btn-giveup ani" id="btn-giveup">ギブアップ</button>`;
  },

  _gameResult(g) {
    const r  = g.lastResult;
    const wi = WEATHER_INFO[r.weather];
    const over = g.isGameOver();
    const wColor = r.weather === 'sunny' ? 'var(--gold)' : r.weather === 'rainy' ? '#42a5f5' : 'var(--text-dim)';

    return `
      <div class="card ani">
        <div class="result-weather-icon">${wi.icon}</div>
        <div class="result-weather-label" style="color:${wColor}">
          ${wi.label}
          <span style="font-size:.7rem;color:var(--text-dim);margin-left:8px">（需要: 最大${wi.demand}個）</span>
        </div>
        <table class="result-table">
          <thead>
            <tr><th></th><th>生産</th><th>販売</th><th>損益</th></tr>
          </thead>
          <tbody>
            <tr>
              <td>あなた</td>
              <td>${r.playerTofu}個</td>
              <td>${r.playerSold}個</td>
              <td class="${r.playerEarn >= 0 ? 'pos' : 'neg'}">
                ${r.playerEarn >= 0 ? '+' : ''}${r.playerEarn.toLocaleString()}円
              </td>
            </tr>
            <tr>
              <td>相手</td>
              <td>${r.computerTofu}個</td>
              <td>${r.computerSold}個</td>
              <td class="${r.computerEarn >= 0 ? 'pos' : 'neg'}">
                ${r.computerEarn >= 0 ? '+' : ''}${r.computerEarn.toLocaleString()}円
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="btn btn-primary ani" id="btn-next">
        ${over ? 'ゲーム終了' : '次のターンへ →'}
      </button>`;
  },

  _gameOver(g) {
    const cls  = g.winner === 'player' ? 'win' : g.winner === 'computer' ? 'lose' : 'draw';
    const text = g.winner === 'player' ? '🎉 あなたの勝ち！' :
                 g.winner === 'computer' ? '💀 コンピュータの勝ち' : '🤝 引き分け';
    return `
      <div class="card ani">
        <div class="gameover-box">
          <div class="gameover-result ${cls}">${text}</div>
          <div class="gameover-sub">${g.day}日間の営業</div>
        </div>
        <div class="prod-row">
          <span class="prod-label">あなた</span>
          <span class="prod-value player">${g.playerMoney.toLocaleString()}円</span>
        </div>
        <div class="prod-row">
          <span class="prod-label">相手</span>
          <span class="prod-value computer">${g.computerMoney.toLocaleString()}円</span>
        </div>
      </div>
      <button class="btn btn-primary  ani" id="btn-again">もう一度プレイ</button>
      <button class="btn btn-secondary ani mt-8" id="btn-scores">スコアを見る</button>`;
  },

  _bindGame(g) {
    const $ = id => document.getElementById(id);

    // ギブアップ（input / reveal フェーズ共通）
    const giveupBtn = $('btn-giveup');
    if (giveupBtn) {
      giveupBtn.onclick = () => {
        if (!confirm('本当にギブアップしますか？')) return;
        const user = Auth.currentUser();
        g.giveUp();
        if (user) DB.addScore(user.id, g.playerMoney, g.computerMoney, g.day, false);
        this._renderGame();
      };
    }

    if (g.phase === 'input') {
      const input  = $('inp-tofu');
      const slider = $('tofu-slider');
      const btn    = $('btn-make');
      if (!input || !btn) return;

      const max = g.playerMax();

      const clamp = v => Math.min(Math.max(0, Math.floor(v)), max);
      const sync  = v => { input.value = v; slider.value = v; };

      // スライダー ↔ 数値入力 の同期
      slider.addEventListener('input', () => sync(clamp(Number(slider.value))));
      input.addEventListener('input',  () => sync(clamp(Number(input.value))));

      // ０ボタン・MAXボタン
      const zeroBtn = $('btn-zero');
      if (zeroBtn) zeroBtn.onclick = () => sync(0);
      const maxBtn = $('btn-max');
      if (maxBtn) maxBtn.onclick = () => sync(max);

      // 増減ボタン
      document.querySelectorAll('.adj-btn[data-delta]').forEach(b => {
        b.onclick = () => sync(clamp((clamp(Number(input.value))) + Number(b.dataset.delta)));
      });

      input.focus();

      const submit = () => {
        const val = clamp(Number(input.value));
        if (val === 0 && !confirm('今日は１個も作らずに休業しますか？')) return;
        btn.disabled = true;
        g.submitPlayerTofu(val);
        this._renderGame();
      };
      btn.onclick = submit;
      input.addEventListener('keydown', e => { if (e.key === 'Enter') submit(); });

    } else if (g.phase === 'reveal') {
      const btn = $('btn-reveal');
      if (!btn) return;
      btn.onclick = () => {
        btn.disabled = true;
        g.revealWeather();
        this._renderGame();
      };

    } else if (g.phase === 'result') {
      const btn = $('btn-next');
      if (!btn) return;
      btn.onclick = () => {
        btn.disabled = true;
        g.nextTurn();
        if (g.phase === 'gameover') {
          const user = Auth.currentUser();
          if (user) DB.addScore(user.id, g.playerMoney, g.computerMoney, g.day, g.winner === 'player');
        }
        this._renderGame();
      };

    } else if (g.phase === 'gameover') {
      const btnAgain  = $('btn-again');
      const btnScores = $('btn-scores');
      if (btnAgain)  btnAgain.onclick  = () => { this.game = new GameState(); this._renderGame(); };
      if (btnScores) btnScores.onclick = () => { location.hash = '#/highscores'; };
    }
  },

  /* ═══════════════════════════════════
     ルール（遊び方）
  ═══════════════════════════════════ */
  _renderRules() {
    this._html(`
      <div class="screen">
        <div class="page-header">
          <div class="page-title" style="font-size:1.6rem">遊び方</div>
        </div>
        <div class="card ani" style="font-size:.82rem;line-height:1.75">
          <div class="card-title">ゲームルール</div>
          <p style="color:var(--text-dim)">
            イスカンダル星でトーフ屋を経営して、地球への帰還費用を稼ごう！<br>
            コンピュータも向かいでトーフ屋を経営中。先に目標金額を超えた方が勝ち！
          </p>
          <table style="width:100%;margin-top:12px;border-collapse:collapse;font-size:.78rem">
            <tr style="color:var(--text-dim);border-bottom:1px solid var(--border)">
              <th style="text-align:left;padding:4px 0;font-weight:normal">項目</th>
              <th style="text-align:right;padding:4px 8px;font-weight:normal">金額</th>
            </tr>
            <tr><td style="padding:5px 0;color:var(--text-dim)">開始所持金</td><td style="text-align:right;padding:5px 8px;color:var(--gold)">5,000円</td></tr>
            <tr><td style="padding:5px 0;color:var(--text-dim)">勝利目標</td><td style="text-align:right;padding:5px 8px;color:var(--accent)">30,000円</td></tr>
            <tr><td style="padding:5px 0;color:var(--text-dim)">仕入れ原価</td><td style="text-align:right;padding:5px 8px">40円/個</td></tr>
            <tr><td style="padding:5px 0;color:var(--text-dim)">販売価格</td><td style="text-align:right;padding:5px 8px">50円/個</td></tr>
          </table>
          <div style="margin-top:14px;color:var(--text-dim);font-size:.78rem;margin-bottom:6px">天候別・最大販売数（需要）</div>
          <div style="display:flex;flex-direction:column;gap:6px">
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-size:1.1rem">☀️</span>
              <span style="color:var(--text-dim);min-width:52px">晴れ</span>
              <div class="w-bar-bg" style="flex:1;height:8px;background:var(--border);border-radius:4px;overflow:hidden">
                <div style="height:100%;width:100%;background:#ffd700;border-radius:4px"></div>
              </div>
              <span style="min-width:56px;text-align:right;color:var(--gold);font-weight:bold">最大500個</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-size:1.1rem">⛅</span>
              <span style="color:var(--text-dim);min-width:52px">くもり</span>
              <div class="w-bar-bg" style="flex:1;height:8px;background:var(--border);border-radius:4px;overflow:hidden">
                <div style="height:100%;width:60%;background:#90a4ae;border-radius:4px"></div>
              </div>
              <span style="min-width:56px;text-align:right;color:#90a4ae;font-weight:bold">最大300個</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px">
              <span style="font-size:1.1rem">🌧️</span>
              <span style="color:var(--text-dim);min-width:52px">雨</span>
              <div class="w-bar-bg" style="flex:1;height:8px;background:var(--border);border-radius:4px;overflow:hidden">
                <div style="height:100%;width:20%;background:#42a5f5;border-radius:4px"></div>
              </div>
              <span style="min-width:56px;text-align:right;color:#42a5f5;font-weight:bold">最大100個</span>
            </div>
          </div>
          <p style="margin-top:10px;color:var(--text-dim)">
            ※ 売れ残ったトーフは廃棄。翌日に持ち越せません。<br>
            ※ 天気予報は確率表示。実際の天気は翌日に判明します。
          </p>
        </div>
      </div>
      ${this._nav('rules')}
    `);
  },

  /* ═══════════════════════════════════
     スコア一覧
  ═══════════════════════════════════ */
  _renderHighScores() {
    const scores = DB.getScores();
    let rows = '';

    if (scores.length === 0) {
      rows = `<tr><td colspan="7" class="score-none">まだスコアがありません</td></tr>`;
    } else {
      scores.forEach((s, i) => {
        const rc   = i === 0 ? 'gold' : i === 1 ? 'silver' : i === 2 ? 'bronze' : '';
        const comp = s.computerMoney != null ? s.computerMoney.toLocaleString() + '円' : '—';
        const days = s.days != null ? s.days + '日' : '—';
        rows += `
          <tr>
            <td class="rank ${rc}">${i + 1}</td>
            <td class="sc-player">${this._esc(s.userId)}</td>
            <td class="sc-num">${s.money.toLocaleString()}円</td>
            <td class="sc-num sc-dim">${comp}</td>
            <td class="sc-num sc-dim">${days}</td>
            <td class="${s.won ? 'score-win' : 'score-lose'}">${s.won ? '勝' : '敗'}</td>
            <td class="sc-date">${s.date}</td>
          </tr>`;
      });
    }

    this._html(`
      <div class="screen">
        <div class="page-header">
          <div class="page-title" style="font-size:1.5rem">SCORES</div>
          <div class="page-subtitle">スコア一覧（${scores.length}件）</div>
        </div>
        <div class="card ani" style="padding:12px 8px">
          <div class="score-scroll">
            <table class="score-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>プレイヤー</th>
                  <th class="sc-num">あなた</th>
                  <th class="sc-num">相手</th>
                  <th class="sc-num">DAY</th>
                  <th>結果</th>
                  <th class="sc-date">日付</th>
                </tr>
              </thead>
              <tbody>${rows}</tbody>
            </table>
          </div>
        </div>
      </div>
      ${this._nav('highscores')}
    `);
  },

  /* ── ユーティリティ ─────────── */
  _esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  },
};

document.addEventListener('DOMContentLoaded', () => App.init());
