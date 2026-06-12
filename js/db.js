const DB = {
  _key: k => 'iskandal_' + k,

  getUsers()        { return JSON.parse(localStorage.getItem(this._key('users'))  || '[]'); },
  saveUsers(u)      { localStorage.setItem(this._key('users'),  JSON.stringify(u)); },
  getScores()       { return JSON.parse(localStorage.getItem(this._key('scores')) || '[]'); },
  saveScores(s)     { localStorage.setItem(this._key('scores'), JSON.stringify(s)); },
  getSession()      { return localStorage.getItem(this._key('session')); },
  setSession(uid)   { localStorage.setItem(this._key('session'), uid); },
  clearSession()    { localStorage.removeItem(this._key('session')); },

  addScore(userId, money, days, won) {
    const scores = this.getScores();
    scores.push({
      userId,
      money,
      days,
      won,
      date: new Date().toLocaleDateString('ja-JP'),
    });
    scores.sort((a, b) => b.money - a.money);
    this.saveScores(scores.slice(0, 100));
  },
};
