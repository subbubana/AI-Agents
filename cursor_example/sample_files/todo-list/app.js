const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');

function addTodo() {
    const text = todoInput.value.trim();
    if (text === "") return;
    const li = document.createElement('li');
    const span = document.createElement('span');
    span.textContent = text;
    span.onclick = () => li.classList.toggle('completed');
    li.appendChild(span);
    const removeBtn = document.createElement('button');
    removeBtn.textContent = 'Remove';
    removeBtn.onclick = () => li.remove();
    li.appendChild(removeBtn);
    todoList.appendChild(li);
    todoInput.value = '';
}
todoInput.addEventListener('keyup', function(event) {
    if (event.key === "Enter") {
        addTodo();
    }
});
