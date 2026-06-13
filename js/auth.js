// Copyright (C) 1978-2026 by N.Tsuda
const Auth = {
  // crypto.subtle は HTTPS / localhost 限定。HTTP LAN アクセス用に純粋JS実装で補完。
  async _hash(password) {
    if (typeof crypto !== 'undefined' && crypto.subtle) {
      const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
      return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
    }
    return this._sha256js(password);
  },

  _sha256js(str) {
    const K = [
      0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
      0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
      0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
      0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
      0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
      0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
      0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
      0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
    ];
    // UTF-8 encode manually（TextEncoder と等価、非セキュアコンテキストでも動作）
    const bytes = [];
    for (let i = 0; i < str.length; i++) {
      const c = str.charCodeAt(i);
      if      (c < 0x80)   bytes.push(c);
      else if (c < 0x800)  bytes.push((c >> 6) | 192, (c & 63) | 128);
      else                 bytes.push((c >> 12) | 224, ((c >> 6) & 63) | 128, (c & 63) | 128);
    }
    const msgLen = bytes.length;
    bytes.push(0x80);
    while (bytes.length % 64 !== 56) bytes.push(0);
    const bitLen = msgLen * 8;
    bytes.push(0, 0, 0, 0, (bitLen >>> 24) & 0xff, (bitLen >>> 16) & 0xff, (bitLen >>> 8) & 0xff, bitLen & 0xff);

    let h = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    const add = (a, b) => (a + b) >>> 0;
    const rot = (x, n) => ((x >>> n) | (x << (32 - n))) >>> 0;

    for (let i = 0; i < bytes.length; i += 64) {
      const W = [];
      for (let t = 0; t < 16; t++)
        W[t] = ((bytes[i+t*4]<<24)|(bytes[i+t*4+1]<<16)|(bytes[i+t*4+2]<<8)|bytes[i+t*4+3]) >>> 0;
      for (let t = 16; t < 64; t++) {
        const s0 = rot(W[t-15],7) ^ rot(W[t-15],18) ^ (W[t-15]>>>3);
        const s1 = rot(W[t-2],17) ^ rot(W[t-2],19)  ^ (W[t-2]>>>10);
        W[t] = add(add(W[t-16], s0 >>> 0), add(W[t-7], s1 >>> 0));
      }
      let [a,b,c,d,e,f,g,hh] = h;
      for (let t = 0; t < 64; t++) {
        const S1 = (rot(e,6)  ^ rot(e,11)  ^ rot(e,25))  >>> 0;
        const ch = ((e & f)   ^ (~e & g))                 >>> 0;
        const t1 = add(add(add(add(hh, S1), ch), K[t]), W[t]);
        const S0 = (rot(a,2)  ^ rot(a,13)  ^ rot(a,22))  >>> 0;
        const mj = ((a & b)   ^ (a & c)    ^ (b & c))    >>> 0;
        const t2 = add(S0, mj);
        hh=g; g=f; f=e; e=add(d,t1); d=c; c=b; b=a; a=add(t1,t2);
      }
      h = [add(h[0],a),add(h[1],b),add(h[2],c),add(h[3],d),
           add(h[4],e),add(h[5],f),add(h[6],g),add(h[7],hh)];
    }
    return h.map(x => x.toString(16).padStart(8,'0')).join('');
  },

  async register(userId, email, password) {
    if (!userId || userId.length < 3)        throw new Error('ユーザーIDは3文字以上にしてください');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) throw new Error('メールアドレスの形式が正しくありません');
    if (!password || password.length < 4)    throw new Error('パスワードは4文字以上にしてください');

    const users = DB.getUsers();
    if (users.find(u => u.id === userId)) throw new Error('このユーザーIDはすでに使用されています');

    const hash = await this._hash(password);
    users.push({ id: userId, email, passwordHash: hash });
    DB.saveUsers(users);
    DB.setSession(userId);
    return { id: userId, email };
  },

  async login(userId, password) {
    if (!userId || !password) throw new Error('ユーザーIDとパスワードを入力してください');

    const user = DB.getUsers().find(u => u.id === userId);
    if (!user) throw new Error('ユーザーIDまたはパスワードが正しくありません');

    const hash = await this._hash(password);
    if (hash !== user.passwordHash) throw new Error('ユーザーIDまたはパスワードが正しくありません');

    DB.setSession(userId);
    return user;
  },

  logout() {
    DB.clearSession();
  },

  currentUser() {
    const uid = DB.getSession();
    if (!uid) return null;
    return DB.getUsers().find(u => u.id === uid) || null;
  },

  async deleteAccount(userId, password) {
    const users = DB.getUsers();
    const user = users.find(u => u.id === userId);
    if (!user) throw new Error('ユーザーが見つかりません');

    const hash = await this._hash(password);
    if (hash !== user.passwordHash) throw new Error('パスワードが正しくありません');

    DB.saveUsers(users.filter(u => u.id !== userId));
    DB.clearSession();
  },
};
