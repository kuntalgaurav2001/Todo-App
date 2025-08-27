let currentEditId = null;

// Add new todo
async function addTodo() {
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    if (!title) {
        alert('Please enter a todo title');
        return;
    }
    
    try {
        const response = await fetch('/api/todos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description })
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to add todo');
        }
    } catch (error) {
        alert('Error adding todo');
    }
}

// Toggle todo completion
async function toggleComplete(todoId) {
    try {
        const response = await fetch(`/api/todos/${todoId}/toggle/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to toggle todo');
        }
    } catch (error) {
        alert('Error toggling todo');
    }
}

// Edit todo
function editTodo(todoId) {
    const todoItem = document.querySelector(`[data-id="${todoId}"]`);
    const title = todoItem.querySelector('.todo-title').textContent;
    const description = todoItem.querySelector('.todo-description')?.textContent || '';
    
    document.getElementById('editTitle').value = title;
    document.getElementById('editDescription').value = description;
    currentEditId = todoId;
    
    document.getElementById('editModal').style.display = 'block';
}

// Save edit
async function saveEdit() {
    const title = document.getElementById('editTitle').value.trim();
    const description = document.getElementById('editDescription').value.trim();
    
    if (!title) {
        alert('Please enter a todo title');
        return;
    }
    
    try {
        const response = await fetch(`/api/todos/${currentEditId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description })
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const error = await response.json();
            alert(error.error || 'Failed to update todo');
        }
    } catch (error) {
        alert('Error updating todo');
    }
}

// Delete todo
async function deleteTodo(todoId) {
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/todos/${todoId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Failed to delete todo');
        }
    } catch (error) {
        alert('Error deleting todo');
    }
}

// Close modal
document.querySelector('.close').onclick = function() {
    document.getElementById('editModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Enter key support for adding todos
document.getElementById('todoTitle').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTodo();
    }
});