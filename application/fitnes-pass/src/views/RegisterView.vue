<template>
  <div class="register-page">
    <div class="register-card">
      <div class="register-header">
        <router-link to="/" class="home-link">← на главную</router-link>
        <h1>регистрация</h1>
        <p>создайте аккаунт в фитнес-клубе «iron fit»</p>
      </div>

      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label for="name">имя и фамилия</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            placeholder="например: алексей иванов"
            required
          />
        </div>

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
          <label for="phone">телефон</label>
          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            placeholder="+7 (999) 123-45-67"
          />
        </div>

        <div class="form-group">
          <label for="password">пароль</label>
          <div class="password-wrapper">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="минимум 6 символов"
              required
              minlength="6"
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

        <div class="form-group">
          <label for="confirmPassword">подтверждение пароля</label>
          <div class="password-wrapper">
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              placeholder="повторите пароль"
              required
              minlength="6"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showConfirmPassword = !showConfirmPassword"
            >
              {{ showConfirmPassword ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <div class="form-group checkbox">
          <input
            id="agree"
            v-model="form.agree"
            type="checkbox"
            required
          />
          <label for="agree">
            я соглашаюсь с
            <a href="#" @click.prevent>условиями использования</a>
            и
            <a href="#" @click.prevent>политикой конфиденциальности</a>
          </label>
        </div>

        <button
          type="submit"
          class="register-btn"
          :disabled="loading"
        >
          {{ loading ? 'регистрация...' : 'создать аккаунт' }}
        </button>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div v-if="success" class="success-message">
          {{ success }}
        </div>
      </form>

      <div class="register-footer">
        <p>
          уже есть аккаунт?
          <router-link to="/login">войти</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        name: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        agree: false
      },
      showPassword: false,
      showConfirmPassword: false,
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async handleRegister() {
      this.error = null
      this.success = null

      if (this.form.password !== this.form.confirmPassword) {
        this.error = 'пароли не совпадают'
        return
      }

      if (this.form.password.length < 6) {
        this.error = 'пароль должен содержать минимум 6 символов'
        return
      }

      if (!this.form.agree) {
        this.error = 'необходимо согласиться с условиями'
        return
      }

      this.loading = true

      try {
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${baseUrl}/auth/register/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.form.name,
            email: this.form.email,
            phone: this.form.phone,
            password: this.form.password
          })
        })

        const data = await response.json()

        if (data.success) {
          this.success = 'регистрация успешна! перенаправление...'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        } else {
          this.error = data.message || 'ошибка регистрации'
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

.register-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #0d0d0d;
  overflow: hidden;
}

.register-card {
  background: #131313;
  border: 1px solid #2a2a2a;
  border-radius: 24px;
  padding: 24px 28px;
  width: 100%;
  max-width: 440px;
  max-height: 95vh;
  overflow-y: auto;
}

.register-header {
  text-align: center;
  margin-bottom: 20px;
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

.register-header h1 {
  font-size: 24px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 4px;
}

.register-header p {
  font-size: 13px;
  color: #666;
  text-transform: lowercase;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
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

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"],
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

.form-group.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 8px;
  margin-top: 2px;
}

.form-group.checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #888;
  cursor: pointer;
  flex-shrink: 0;
}

.form-group.checkbox label {
  font-size: 12px;
  color: #666;
  cursor: pointer;
  text-transform: lowercase;
}

.form-group.checkbox label a {
  color: #888;
  text-decoration: none;
  transition: 0.3s;
}

.form-group.checkbox label a:hover {
  color: #e8e8e8;
}

.register-btn {
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

.register-btn:hover:not(:disabled) {
  background: #e8e8e8;
  color: #0d0d0d;
  border-color: #e8e8e8;
}

.register-btn:disabled {
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

.success-message {
  color: #8bc34a;
  font-size: 13px;
  text-align: center;
  padding: 6px;
  border: 1px solid #2a3a1a;
  border-radius: 10px;
  background: #0d1a0a;
}

.register-footer {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #1f1f1f;
}

.register-footer p {
  font-size: 13px;
  color: #666;
  text-transform: lowercase;
}

.register-footer a {
  color: #888;
  text-decoration: none;
  transition: 0.3s;
}

.register-footer a:hover {
  color: #e8e8e8;
}

@media (max-height: 700px) {
  .register-card {
    padding: 16px 20px;
  }
  
  .register-header {
    margin-bottom: 12px;
  }
  
  .register-form {
    gap: 10px;
  }
  
  .form-group input[type="text"],
  .form-group input[type="email"],
  .form-group input[type="tel"],
  .form-group input[type="password"] {
    padding: 8px 12px;
  }
}
</style>