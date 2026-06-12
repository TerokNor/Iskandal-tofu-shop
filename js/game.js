/* ── 定数 ───────────────────────────── */
const TOFU_COST  = 40;
const TOFU_PRICE = 50;
const DEMAND     = { sunny: 500, cloudy: 300, rainy: 100 };
const GOAL       = 30000;
const START      = 5000;

const WEATHER_INFO = {
  sunny:  { icon: '☀️',  label: '晴れ',    cls: 'w-sunny',  demand: 500 },
  cloudy: { icon: '⛅',  label: 'くもり',  cls: 'w-cloudy', demand: 300 },
  rainy:  { icon: '🌧️', label: '雨',      cls: 'w-rainy',  demand: 100 },
};

/* ── Weather ─────────────────────────── */
class Weather {
  constructor() {
    const p0 = Math.floor(Math.random() * 101);
    const p1 = Math.floor(Math.random() * 101);
    if (p0 >= p1) {
      this.sunny = 100 - p0;
      this.rainy = p1;
    } else {
      this.sunny = 100 - p1;
      this.rainy = p0;
    }
    this.cloudy = 100 - this.sunny - this.rainy;
  }

  roll() {
    const r = Math.floor(Math.random() * 101);
    if (r <= this.rainy)              return 'rainy';
    if (r <= this.rainy + this.cloudy) return 'cloudy';
    return 'sunny';
  }
}

/* ── GameState ───────────────────────── */
class GameState {
  constructor() {
    this.playerMoney   = START;
    this.computerMoney = START;
    this.weather       = new Weather();
    this.day           = 1;
    this.phase         = 'input'; // 'input' | 'reveal' | 'result' | 'gameover'
    this.playerTofu    = 0;
    this.computerTofu  = 0;
    this.weatherResult = null;
    this.lastResult    = null;
    this.winner        = null;
  }

  playerMax()   { return Math.floor(this.playerMoney   / TOFU_COST); }
  computerMax() { return Math.floor(this.computerMoney / TOFU_COST); }

  isGameOver() {
    return (
      this.playerMoney   >= GOAL         ||
      this.computerMoney >= GOAL         ||
      this.playerMoney   <  TOFU_COST    ||
      this.computerMoney <  TOFU_COST
    );
  }

  submitPlayerTofu(count) {
    this.playerTofu = Math.min(Math.max(0, Math.floor(count)), this.playerMax());

    // Computer AI (Python オリジナル準拠)
    const maxC = this.computerMax();
    let n;
    if (this.weather.rainy > 30) {
      n = DEMAND.rainy;
    } else if (this.weather.sunny > 49) {
      n = Math.min(DEMAND.sunny, maxC);
    } else {
      n = Math.min(DEMAND.cloudy, maxC);
    }
    this.computerTofu = Math.min(n, maxC);

    this.phase = 'reveal';
  }

  revealWeather() {
    this.weatherResult = this.weather.roll();
    const demand = DEMAND[this.weatherResult];

    const playerSold   = Math.min(this.playerTofu,   demand);
    const computerSold = Math.min(this.computerTofu, demand);

    const playerEarn   = playerSold   * TOFU_PRICE - this.playerTofu   * TOFU_COST;
    const computerEarn = computerSold * TOFU_PRICE - this.computerTofu * TOFU_COST;

    this.playerMoney   += playerEarn;
    this.computerMoney += computerEarn;

    this.lastResult = {
      weather:       this.weatherResult,
      playerTofu:    this.playerTofu,
      playerSold,
      playerEarn,
      computerTofu:  this.computerTofu,
      computerSold,
      computerEarn,
    };

    this.phase = 'result';
  }

  nextTurn() {
    if (this.isGameOver()) {
      this.phase  = 'gameover';
      this.winner = this._winner();
      return;
    }
    this.day++;
    this.weather       = new Weather();
    this.playerTofu    = 0;
    this.computerTofu  = 0;
    this.weatherResult = null;
    this.lastResult    = null;
    this.phase         = 'input';
  }

  _winner() {
    if (this.playerMoney > this.computerMoney) return 'player';
    if (this.playerMoney < this.computerMoney) return 'computer';
    return 'draw';
  }
}
