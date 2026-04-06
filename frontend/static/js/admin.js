// App Alpine.js para o painel admin

function adminApp() {
  return {
    logout() {
      localStorage.removeItem('token');
      window.location.href = '/admin/login';
    },
    authHeader() {
      const token = localStorage.getItem('token');
      return token ? { Authorization: `Bearer ${token}` } : {};
    },
  };
}

function dashboard() {
  return {
    resumo: {},
    async init() {
      const token = localStorage.getItem('token');
      const resp = await fetch('/api/v1/relatorios/resumo', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (resp.ok) this.resumo = await resp.json();
    },
  };
}
