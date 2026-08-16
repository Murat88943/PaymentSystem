<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <router-link to="/" class="home-link">← на главную</router-link>
        <h1>вход</h1>
        <p>войдите в свой аккаунт</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="example@mail.ru"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">пароль</label>
          <div class="password-wrapper">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="введите пароль"
              required
            />
            <button
              type="button"
              class="toggle-password"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <button
          type="submit"
          class="login-btn"
          :disabled="loading"
        >
          {{ loading ? 'вход...' : 'войти' }}
        </button>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>
      </form>

      <div class="login-footer">
        <p>
          нет аккаунта?
          <router-link to="/register">зарегистрироваться</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      showPassword: false,
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.error = null
      this.loading = true

      try {
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${baseUrl}/auth/login/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.form.email,
            password: this.form.password
          })
        })

        const data = await response.json()

        if (data.success) {
          localStorage.setItem('token', data.token)
          localStorage.setItem('user', JSON.stringify(data.user))
          this.$router.push('/')
        } else {
          this.error = data.message || 'ошибка входа'
        }
      } catch (err) {
        this.error = 'не удалось подключиться к серверу'
        console.error('ошибка:', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #0d0d0d;
  overflow: hidden;
}

.login-card {
  background: #131313;
  border: 1px solid #2a2a2a;
  border-radius: 24px;
  padding: 32px 28px;
  width: 100%;
  max-width: 400px;
  max-height: 95vh;
  overflow-y: auto;
}

.login-header {
  text-align: center;
  margin-bottom: 24px;
}

.home-link {
  display: inline-block;
  margin-bottom: 12px;
  color: #666;
  text-decoration: none;
  font-size: 13px;
  text-transform: lowercase;
  transition: 0.3s;
  letter-spacing: 0.5px;
}

.home-link:hover {
  color: #e8e8e8;
}

.login-header h1 {
  font-size: 24px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 4px;
}

.login-header p {
  font-size: 13px;
  color: #666;
  text-transform: lowercase;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-size: 12px;
  color: #888;
  text-transform: lowercase;
  letter-spacing: 0.3px;
}

.form-group input[type="email"],
.form-group input[type="password"] {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 10px;
  padding: 10px 14px;
  font-size: 14px;
  color: #e8e8e8;
  transition: 0.3s;
  outline: none;
  width: 100%;
}

.form-group input:focus {
  border-color: #4a4a4a;
}

.form-group input::placeholder {
  color: #444;
}

.password-wrapper {
  position: relative;
  width: 100%;
}

.password-wrapper input {
  padding-right: 44px;
}

.toggle-password {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 16px;
  padding: 2px;
}

.toggle-password:hover {
  color: #e8e8e8;
}

.login-btn {
  background: transparent;
  color: #e8e8e8;
  border: 1px solid #3a3a3a;
  padding: 12px;
  border-radius: 40px;
  font-size: 14px;
  font-weight: 300;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
  letter-spacing: 0.5px;
  margin-top: 4px;
  width: 100%;
}

.login-btn:hover:not(:disabled) {
  background: #e8e8e8;
  color: #0d0d0d;
  border-color: #e8e8e8;
}

.login-btn:disabled {
  color: #444;
  border-color: #222;
  cursor: not-allowed;
}

.error-message {
  color: #e57373;
  font-size: 13px;
  text-align: center;
  padding: 6px;
  border: 1px solid #3a1a1a;
  border-radius: 10px;
  background: #1a0a0a;
}

.login-footer {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #1f1f1f;
}

.login-footer p {
  font-size: 13px;
  color: #666;
  text-transform: lowercase;
}

.login-footer a {
  color: #888;
  text-decoration: none;
  transition: 0.3s;
}

.login-footer a:hover {
  color: #e8e8e8;
}

@media (max-height: 700px) {
  .login-card {
    padding: 16px 20px;
  }
  
  .login-header {
    margin-bottom: 12px;
  }
  
  .login-form {
    gap: 10px;
  }
  
  .form-group input[type="email"],
  .form-group input[type="password"] {
    padding: 8px 12px;
  }
}
</style>