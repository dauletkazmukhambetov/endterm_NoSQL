const API_URL = 'http://127.0.0.1:8000';

const api = {
  async signup(name, email, password) {
    const res = await fetch(`${API_URL}/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Signup failed');
    }
    return res.json();
  },

  async login(email, password) {
    const params = new URLSearchParams({ email, password });
    const res = await fetch(`${API_URL}/users/login/?${params}`, { method: 'POST' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async getCars() {
    const res = await fetch(`${API_URL}/cars/`);
    if (!res.ok) throw new Error('Failed to fetch cars');
    return res.json();
  },

  async getCar(id) {
    const res = await fetch(`${API_URL}/cars/${id}`);
    if (!res.ok) throw new Error('Car not found');
    return res.json();
  },

  async createCar(data) {
    const res = await fetch(`${API_URL}/cars/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to add car');
    }
    return res.json();
  },

  async updateCar(id, data) {
    const res = await fetch(`${API_URL}/cars/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to update car');
    }
    return res.json();
  },

  async deleteCar(id) {
    const res = await fetch(`${API_URL}/cars/${id}`, { method: 'DELETE' });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to delete car');
    }
    return res.json();
  },

  async createOrder(carId, userId, price, status = 'Completed') {
    const res = await fetch(`${API_URL}/orders/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        car_id: carId,
        user_id: userId,
        price: Number(price),
        status,
      }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to create order');
    }
    return res.json();
  },

  async getOrders(userId) {
    const res = await fetch(`${API_URL}/orders/?user_id=${encodeURIComponent(userId)}`);
    if (!res.ok) throw new Error('Failed to fetch orders');
    return res.json();
  },

  async getCarsStats() {
    const res = await fetch(`${API_URL}/cars/stats/aggregation`);
    if (!res.ok) throw new Error('Failed to fetch stats');
    return res.json();
  },
};
