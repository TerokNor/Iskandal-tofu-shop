const Auth = {
  async _hash(password) {
    const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password));
    return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
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
