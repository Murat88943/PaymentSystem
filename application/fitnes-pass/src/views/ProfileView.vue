<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1>профиль</h1>
      <button class="logout-btn" @click="logout">выйти</button>
    </div>

    <div v-if="loadingUser" class="loading">загрузка...</div>
    <div v-else-if="userError" class="error">{{ userError }}</div>
    <div v-else class="profile-info">
      <div class="avatar">
        <span>{{ initials }}</span>
      </div>
      <div class="user-info">
        <h2>{{ user.name }}</h2>
        <p>{{ user.email }}</p>
        <p v-if="user.phone" class="phone">{{ user.phone }}</p>
        <span class="member-since">в клубе с {{ formatDate(user.created_at) }}</span>
      </div>
    </div>

    <div class="divider"></div>

    <div class="subscriptions-section">
      <h2>мои абонементы</h2>
      
      <div v-if="loadingSubs" class="loading">загрузка...</div>
      <div v-else-if="subsError" class="error">{{ subsError }}</div>
      <div v-else-if="!subscription" class="empty">
        <p>у вас нет активных абонементов</p>
        <button class="buy-btn" @click="goHome">выбрать абонемент</button>
      </div>
      <div v-else class="subscriptions">
        <div class="subscription-card">
          <div class="sub-header">
            <h3>{{ subscription.plan_type }}</h3>
            <span class="status" :class="subscription.status">
              {{ subscription.status === 'active' ? 'активен' : subscription.status }}
            </span>
          </div>
          
          <div class="sub-details">
            <div class="sub-info">
              <span class="label">стоимость:</span>
              <span class="value">{{ subscription.price }} ₽</span>
            </div>
            <div class="sub-info">
              <span class="label">дата начала:</span>
              <span class="value">{{ formatDate(subscription.start_date) }}</span>
            </div>
            <div class="sub-info">
              <span class="label">действует до:</span>
              <span class="value">{{ formatDate(subscription.end_date) }}</span>
            </div>
          </div>

          <button
            v-if="subscription.status === 'active'"
            class="refund-btn"
            @click="handleRefund"
            :disabled="refundLoading"
          >
            {{ refundLoading ? 'обработка...' : 'вернуть средства' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileView',
  data() {
    return {
      user: {},
      subscription: null,
      loadingUser: true,
      loadingSubs: true,
      userError: null,
      subsError: null,
      refundLoading: false
    }
  },
  computed: {
    initials() {
      if (!this.user.name) return ''
      return this.user.name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase()
    }
  },
  mounted() {
    this.fetchProfile()
    this.fetchSubscription()
  },
  methods: {
    async fetchProfile() {
      this.loadingUser = true
      this.userError = null

      try {
        const user = JSON.parse(localStorage.getItem('user'))
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

        if (!user || !user.id) {
          this.userError = 'пользователь не найден'
          return
        }

        const response = await fetch(`${baseUrl}/user/profile/?user_id=${user.id}`)
        const data = await response.json()

        if (data.success) {
          this.user = data.user
        } else {
          this.userError = data.message || 'ошибка загрузки профиля'
        }
      } catch (err) {
        this.userError = 'не удалось подключиться к серверу'
        console.error('ошибка:', err)
      } finally {
        this.loadingUser = false
      }
    },

    async fetchSubscription() {
      this.loadingSubs = true
      this.subsError = null

      try {
        const user = JSON.parse(localStorage.getItem('user'))
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

        if (!user || !user.id) {
          this.subsError = 'пользователь не найден'
          return
        }

        const response = await fetch(`${baseUrl}/subscription/status/?user_id=${user.id}`)
        const data = await response.json()

        if (data.success && data.subscription) {
          this.subscription = data.subscription
        } else {
          this.subscription = null
        }
      } catch (err) {
        this.subsError = 'не удалось подключиться к серверу'
        console.error('ошибка:', err)
      } finally {
        this.loadingSubs = false
      }
    },

    formatDate(dateStr) {
      if (!dateStr) return 'неизвестно'
      const date = new Date(dateStr)
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      })
    },

    async handleRefund() {
      if (!this.subscription) return

      if (!confirm(`вернуть средства за абонемент "${this.subscription.plan_type}"?`)) {
        return
      }

      this.refundLoading = true

      try {
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${baseUrl}/subscription/refund/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            subscription_id: this.subscription.id
          })
        })

        const data = await response.json()

        if (data.success) {
          alert('возврат средств выполнен')
          this.fetchSubscription()
        } else {
          alert(data.message || 'ошибка при возврате')
        }
      } catch (err) {
        alert('не удалось подключиться к серверу')
        console.error('ошибка:', err)
      } finally {
        this.refundLoading = false
      }
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.$router.push('/login')
    },

    goHome() {
      this.$router.push('/')
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

.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.profile-header h1 {
  font-size: 28px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  text-transform: lowercase;
}

.logout-btn {
  background: transparent;
  color: #666;
  border: 1px solid #2a2a2a;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
}

.logout-btn:hover {
  color: #e57373;
  border-color: #e57373;
}

.loading {
  text-align: center;
  color: #666;
  font-size: 14px;
  padding: 20px;
}

.error {
  text-align: center;
  color: #e57373;
  font-size: 14px;
  padding: 20px;
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 24px;
  background: #111111;
  border: 1px solid #2a2a2a;
  border-radius: 16px;
  margin-bottom: 30px;
}

.avatar {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #e8e8e8;
  font-weight: 300;
  flex-shrink: 0;
}

.user-info h2 {
  font-size: 20px;
  font-weight: 400;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 4px;
}

.user-info p {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.user-info .phone {
  font-size: 13px;
  color: #888;
}

.member-since {
  font-size: 12px;
  color: #444;
  text-transform: lowercase;
}

.divider {
  height: 1px;
  background: #2a2a2a;
  margin: 20px 0 30px;
}

.subscriptions-section h2 {
  font-size: 22px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 24px;
}

.empty {
  text-align: center;
  color: #666;
  padding: 40px 0;
}

.empty p {
  margin-bottom: 16px;
  font-size: 14px;
}

.buy-btn {
  background: transparent;
  color: #e8e8e8;
  border: 1px solid #3a3a3a;
  padding: 10px 32px;
  border-radius: 40px;
  font-size: 13px;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
}

.buy-btn:hover {
  background: #e8e8e8;
  color: #0d0d0d;
  border-color: #e8e8e8;
}

.subscriptions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.subscription-card {
  background: #131313;
  border: 1px solid #2a2a2a;
  border-radius: 16px;
  padding: 24px;
  transition: 0.3s;
}

.subscription-card:hover {
  border-color: #4a4a4a;
}

.sub-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.sub-header h3 {
  font-size: 18px;
  font-weight: 400;
  color: #e8e8e8;
  text-transform: lowercase;
}

.status {
  font-size: 12px;
  padding: 4px 14px;
  border-radius: 20px;
  text-transform: lowercase;
}

.status.active {
  color: #8bc34a;
  border: 1px solid #2a3a1a;
  background: #0d1a0a;
}

.status.cancelled,
.status.refunded {
  color: #666;
  border: 1px solid #2a2a2a;
  background: #111111;
}

.sub-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 24px;
  margin-bottom: 16px;
}

.sub-info {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 1px solid #1a1a1a;
}

.sub-info .label {
  font-size: 13px;
  color: #666;
  text-transform: lowercase;
}

.sub-info .value {
  font-size: 13px;
  color: #aaa;
}

.refund-btn {
  background: transparent;
  color: #e57373;
  border: 1px solid #3a1a1a;
  padding: 8px 24px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
  width: 100%;
  margin-top: 8px;
}

.refund-btn:hover:not(:disabled) {
  background: #e57373;
  color: #0d0d0d;
  border-color: #e57373;
}

.refund-btn:disabled {
  color: #444;
  border-color: #222;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .profile-info {
    flex-direction: column;
    text-align: center;
  }

  .sub-details {
    grid-template-columns: 1fr;
  }

  .sub-header {
    flex-direction: column;
    gap: 8px;
  }
}
</style>