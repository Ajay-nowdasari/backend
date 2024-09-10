// api.js
const API_URL = 'http://localhost:8000/api/todos/';

export const fetchTodos = () => fetch(API_URL).then(response => response.json());

export const createTodo = (todo) => fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(todo)
}).then(response => response.json());

export const updateTodo = (id, updates) => fetch(`${API_URL}${id}/`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
}).then(response => response.json());

export const deleteTodo = (id) => fetch(`${API_URL}${id}/`, {
    method: 'DELETE'
});
