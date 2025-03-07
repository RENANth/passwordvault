document.addEventListener('DOMContentLoaded', function() {
    const masterPassword = document.getElementById('master_password');
    const confirmPassword = document.getElementById('confirm_password');
    const submitBtn = document.getElementById('submitBtn');
    const progressBar = document.querySelector('.progress-bar');
    const passwordFeedback = document.getElementById('passwordFeedback');
    const passwordMatch = document.getElementById('passwordMatch');

    function checkPasswordStrength(password) {
        let strength = 0;
        const feedback = [];

        if (password.length < 8) {
            feedback.push('Password should be at least 8 characters long');
        } else {
            strength += 20;
        }

        if (password.match(/[a-z]/)) strength += 20;
        if (password.match(/[A-Z]/)) strength += 20;
        if (password.match(/[0-9]/)) strength += 20;
        if (password.match(/[^a-zA-Z0-9]/)) strength += 20;

        if (strength < 40) {
            progressBar.className = 'progress-bar bg-danger';
            feedback.push('Password is weak');
        } else if (strength < 80) {
            progressBar.className = 'progress-bar bg-warning';
            feedback.push('Password is moderate');
        } else {
            progressBar.className = 'progress-bar bg-success';
            feedback.push('Password is strong');
        }

        return { strength, feedback: feedback.join(', ') };
    }

    function updatePasswordStrength() {
        const { strength, feedback } = checkPasswordStrength(masterPassword.value);
        progressBar.style.width = strength + '%';
        passwordFeedback.textContent = feedback;
    }

    function checkPasswordsMatch() {
        if (masterPassword.value && confirmPassword.value) {
            if (masterPassword.value === confirmPassword.value) {
                passwordMatch.textContent = 'Passwords match';
                passwordMatch.className = 'form-text text-success';
                submitBtn.disabled = false;
            } else {
                passwordMatch.textContent = 'Passwords do not match';
                passwordMatch.className = 'form-text text-danger';
                submitBtn.disabled = true;
            }
        } else {
            passwordMatch.textContent = '';
            submitBtn.disabled = true;
        }
    }

    masterPassword.addEventListener('input', () => {
        updatePasswordStrength();
        checkPasswordsMatch();
    });

    confirmPassword.addEventListener('input', checkPasswordsMatch);
});
