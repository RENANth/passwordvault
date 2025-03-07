document.addEventListener('DOMContentLoaded', function() {
    // Inicializa todos os tooltips
    const tooltips = [].slice.call(document.querySelectorAll('[title]'))
    tooltips.map(tooltip => new bootstrap.Tooltip(tooltip));

    // Toggle de visibilidade da senha
    document.querySelectorAll('.toggle-password, .toggle-new-password').forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');

            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.setAttribute('data-feather', 'eye-off');
            } else {
                passwordField.type = 'password';
                icon.setAttribute('data-feather', 'eye');
            }
            feather.replace();
        });
    });

    // Copiar senha para a área de transferência
    document.querySelectorAll('.copy-password').forEach(button => {
        button.addEventListener('click', function() {
            const password = this.dataset.password;
            navigator.clipboard.writeText(password).then(() => {
                // Mostra feedback visual
                const originalHtml = this.innerHTML;
                this.innerHTML = '<i data-feather="check"></i>';
                feather.replace();

                // Mostra toast de sucesso
                const toast = new bootstrap.Toast(document.getElementById('successToast'));
                document.querySelector('.toast-body').textContent = 'Senha copiada com sucesso!';
                toast.show();

                setTimeout(() => {
                    this.innerHTML = originalHtml;
                    feather.replace();
                }, 1000);
            });
        });
    });

    // Gerador de senhas
    document.querySelector('.generate-password').addEventListener('click', function() {
        const length = 16;
        const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?';
        let password = '';

        // Garante pelo menos um caractere de cada tipo
        password += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[Math.floor(Math.random() * 26)];
        password += 'abcdefghijklmnopqrstuvwxyz'[Math.floor(Math.random() * 26)];
        password += '0123456789'[Math.floor(Math.random() * 10)];
        password += '!@#$%^&*()_+-=[]{}|;:,.<>?'[Math.floor(Math.random() * 23)];

        // Completa o resto da senha
        for (let i = password.length; i < length; i++) {
            password += charset.charAt(Math.floor(Math.random() * charset.length));
        }

        // Embaralha a senha
        password = password.split('').sort(() => Math.random() - 0.5).join('');

        const passwordField = document.getElementById('password');
        passwordField.value = password;
        passwordField.type = 'text';
        setTimeout(() => {
            passwordField.type = 'password';
        }, 2000);

        // Atualiza o indicador de força
        checkPasswordStrength(password);

        // Mostra feedback
        const toast = new bootstrap.Toast(document.getElementById('successToast'));
        document.querySelector('.toast-body').textContent = 'Senha segura gerada com sucesso!';
        toast.show();
    });

    // Verificador de força da senha
    function checkPasswordStrength(password) {
        const progressBar = document.querySelector('#addPasswordModal .progress-bar');
        const feedback = document.querySelector('.password-feedback');
        let strength = 0;
        let message = '';

        // Critérios de força
        if (password.length >= 8) strength += 20;
        if (password.match(/[a-z]/)) strength += 20;
        if (password.match(/[A-Z]/)) strength += 20;
        if (password.match(/[0-9]/)) strength += 20;
        if (password.match(/[^a-zA-Z0-9]/)) strength += 20;

        // Feedback visual
        if (strength <= 20) {
            progressBar.className = 'progress-bar bg-danger';
            message = 'Senha muito fraca';
        } else if (strength <= 40) {
            progressBar.className = 'progress-bar bg-warning';
            message = 'Senha fraca';
        } else if (strength <= 60) {
            progressBar.className = 'progress-bar bg-info';
            message = 'Senha média';
        } else if (strength <= 80) {
            progressBar.className = 'progress-bar bg-primary';
            message = 'Senha forte';
        } else {
            progressBar.className = 'progress-bar bg-success';
            message = 'Senha muito forte';
        }

        progressBar.style.width = strength + '%';
        feedback.textContent = message;
    }

    // Monitora mudanças na senha
    document.getElementById('password').addEventListener('input', function() {
        checkPasswordStrength(this.value);
    });

    // Animação de sucesso ao adicionar senha
    document.getElementById('addPasswordForm').addEventListener('submit', function() {
        const toast = new bootstrap.Toast(document.getElementById('successToast'));
        document.querySelector('.toast-body').textContent = 'Senha adicionada com sucesso!';
        toast.show();
    });
});