document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const expenseForm = document.getElementById('expense-form');

    // Basic form validation example
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();
            if (username === '' || password === '') {
                e.preventDefault();
                alert('All fields are required!');
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const username = document.getElementById('login-username').value.trim();
            const password = document.getElementById('login-password').value.trim();
            if (username === '' || password === '') {
                e.preventDefault();
                alert('All fields are required!');
            }
        });
    }

    if (expenseForm) {
        expenseForm.addEventListener('submit', (e) => {
            const amount = document.getElementById('amount').value.trim();
            const category = document.getElementById('category').value.trim();
            const date = document.getElementById('date').value.trim();
            if (amount === '' || category === '' || date === '') {
                e.preventDefault();
                alert('All fields are required!');
            }
        });
    }
});
