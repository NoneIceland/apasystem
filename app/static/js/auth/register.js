document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.password-toggle').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.querySelector('svg').innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                `;
            } else {
                input.type = 'password';
                this.querySelector('svg').innerHTML = `
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                `;
            }
        });
    });
    
    // 验证码发送功能
    const sendBtn = document.getElementById('send-code-btn');
    const emailInput = document.getElementById('email');
    
    // 邮箱验证正则
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // 更新发送按钮状态
    function updateSendButtonState() {
        if (!emailInput || !emailInput.value || !emailRegex.test(emailInput.value)) {
            sendBtn.disabled = true;
            sendBtn.classList.add('disabled:bg-gray-400');
        } else {
            sendBtn.disabled = false;
            sendBtn.classList.remove('disabled:bg-gray-400');
        }
    }
    
    // 初始状态检查
    if (emailInput && sendBtn) {
        updateSendButtonState();
        
        // 邮箱输入变化时更新按钮状态
        emailInput.addEventListener('input', updateSendButtonState);
        
        sendBtn.addEventListener('click', async function() {
            const email = emailInput.value;
            
            if (!email) {
                alert('请输入邮箱地址');
                return;
            }
            
            // 邮箱格式验证
            if (!emailRegex.test(email)) {
                alert('请输入有效的邮箱地址');
                return;
            }
            
            // 禁用按钮防止重复点击
            sendBtn.disabled = true;
            sendBtn.textContent = '发送中...';
            
            try {
                const response = await fetch('/api/send-code', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email })
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    // 开始倒计时
                    let countdown = 60;
                    const timer = setInterval(() => {
                        sendBtn.textContent = `${countdown}秒后重试`;
                        countdown--;
                        
                        if (countdown <= 0) {
                            clearInterval(timer);
                            sendBtn.disabled = false;
                            sendBtn.textContent = '发送验证码';
                            updateSendButtonState();
                        }
                    }, 1000);
                    
                    // 开发环境显示验证码
                    if (result.debug_code) {
                        console.log(`测试用验证码: ${result.debug_code}`);
                    }
                    
                    alert('验证码已发送，请查看邮箱');
                } else {
                    alert(result.message || '发送验证码失败');
                    sendBtn.disabled = false;
                    sendBtn.textContent = '发送验证码';
                    updateSendButtonState();
                }
            } catch (error) {
                console.error('发送验证码失败:', error);
                alert('请求失败，请重试');
                sendBtn.disabled = false;
                sendBtn.textContent = '发送验证码';
                updateSendButtonState();
            }
        });
    }
});