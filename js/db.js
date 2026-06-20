// Copyright (C) 1978-2026 by N.Tsuda
const DB = {
  _key: k => 'iskandal_' + k,

  getScores()    { return JSON.parse(localStorage.getItem(this._key('scores')) || '[]'); },
  saveScores(s)  { localStorage.setItem(this._key('scores'), JSON.stringify(s)); },
  getBest3()     { return JSON.parse(localStorage.getItem(this._key('best3'))  || '[]'); },
  saveBest3(s)   { localStorage.setItem(this._key('best3'),  JSON.stringify(s)); },

  addScore(money, computerMoney, days, won) {
    const entry = {
      money,
      computerMoney,
      days,
      won,
      date: new Date().toLocaleString('ja-JP', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit',
      }),
    };

    const scores = this.getScores();
    scores.unshift(entry);
    this.saveScores(scores.slice(0, 100));

    const best3 = this.getBest3();
    best3.push(entry);
    best3.sort((a, b) => b.money - a.money);
    this.saveBest3(best3.slice(0, 3));
  },
};
