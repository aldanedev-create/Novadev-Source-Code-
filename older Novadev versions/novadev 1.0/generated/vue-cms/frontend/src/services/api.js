const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}/api/${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.error || `Request failed: ${response.status}`)
  }
  return data
}

export default {
  list(resource) {
    return request(resource)
  },
  create(resource, payload) {
    return request(resource, {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  },
  remove(resource, id) {
    return request(`${resource}/${id}`, { method: 'DELETE' })
  }
}
