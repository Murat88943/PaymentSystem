<template>
  <div class="payment-page">
    <div class="club-info">
      <h1>фитнес-клуб «iron fit»</h1>
      <p>современный зал с профессиональным оборудованием</p>
      <p>групповые программы, персональные тренировки, зона функционального фитнеса</p>
      <p>работаем с 2015 года — более 5000 довольных клиентов</p>
    </div>

    <div class="divider"></div>

    <h2>оформление абонемента</h2>

    <div class="payment-card" v-if="plan">
      <h3>{{ plan.name }}</h3>
      <div class="price">{{ plan.price }} ₽</div>
      <div class="period">за {{ plan.period }}</div>

      <div class="features">
        <p class="features-title">входит в абонемент:</p>
        <ul>
          <li v-for="feature in plan.features" :key="feature">
            {{ feature }}
          </li>
        </ul>
      </div>

      <div class="total">
        <span>итого:</span>
        <span class="total-price">{{ plan.price }} ₽</span>
      </div>

      <button class="pay-btn" @click="pay" :disabled="loading">
        {{ loading ? 'обработка...' : 'оплатить' }}
      </button>

      <p class="secure">безопасная оплата через юкасса</p>
    </div>

    <div v-if="statusMessage" class="status" :class="statusType">
      {{ statusMessage }}
    </div>

    <button class="back-btn" @click="goHome">← вернуться к тарифам</button>
  </div>
</template>

<script>
export default {
  name: 'PaymentView',
  data() {
    return {
      plan: null,
      loading: false,
      statusMessage: '',
      statusType: ''
    }
  },
  created() {
    const planData = this.$route.query.plan
    if (planData) {
      try {
        this.plan = JSON.parse(planData)
      } catch {
        this.plan = null
      }
    }
    if (!this.plan) {
      this.$router.push('/')
    }
  },
  methods: {
    async pay() {
      const user = JSON.parse(localStorage.getItem('user'))
      
      if (!user || !user.id) {
        this.statusMessage = 'необходимо войти в аккаунт для оплаты'
        this.statusType = 'error'
        setTimeout(() => {
          this.$router.push('/login')
        }, 1500)
        return
      }

      this.loading = true
      this.statusMessage = 'создание платежа...'
      this.statusType = 'info'

      try {
        const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${baseUrl}/payment/create-link/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: user.id,
            plan_name: this.plan.name,
            amount: this.plan.price,
            currency: 'RUB',
            return_url: 'http://localhost:5173/',
            description: `оплата тарифа ${this.plan.name}`
          })
        })

        const data = await response.json()

        if (data.success) {
          this.statusMessage = 'платёж создан, открываем страницу оплаты...'
          this.statusType = 'success'

          if (data.payment_url) {
            setTimeout(() => {
              window.open(data.payment_url, '_blank')
            }, 1000)
          }
        } else {
          this.statusMessage = data.message || 'ошибка при создании платежа'
          this.statusType = 'error'
        }
      } catch (err) {
        this.statusMessage = 'не удалось подключиться к серверу'
        this.statusType = 'error'
        console.error('ошибка:', err)
      } finally {
        setTimeout(() => {
          this.loading = false
        }, 2000)
      }
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

.payment-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.club-info {
  text-align: center;
  margin-bottom: 20px;
}

.club-info h1 {
  font-size: 22px;
  font-weight: 300;
  letter-spacing: 2px;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 8px;
}

.club-info p {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  max-width: 440px;
  margin: 0 auto;
}

.divider {
  height: 1px;
  background: #2a2a2a;
  margin: 20px 0 30px;
}

h2 {
  text-align: center;
  font-size: 20px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  margin-bottom: 24px;
  text-transform: lowercase;
}

.payment-card {
  background: #131313;
  border: 1px solid #2a2a2a;
  border-radius: 20px;
  padding: 30px 24px 24px;
  text-align: center;
}

.payment-card h3 {
  font-size: 20px;
  font-weight: 400;
  color: #e8e8e8;
  text-transform: lowercase;
  letter-spacing: 1px;
  margin-bottom: 4px;
}

.payment-card .price {
  font-size: 38px;
  font-weight: 300;
  color: #ffffff;
  margin: 8px 0 2px;
}

.payment-card .period {
  font-size: 14px;
  color: #666;
  text-transform: lowercase;
}

.features {
  margin: 18px 0 20px;
  text-align: left;
}

.features-title {
  font-size: 13px;
  color: #888;
  text-transform: lowercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.features ul {
  list-style: none;
  padding: 0;
}

.features ul li {
  font-size: 14px;
  color: #aaa;
  padding: 5px 0;
  border-bottom: 1px solid #1f1f1f;
  text-transform: lowercase;
}

.features ul li:last-child {
  border-bottom: none;
}

.total {
  display: flex;
  justify-content: space-between;
  padding: 14px 0 10px;
  font-size: 16px;
  color: #aaa;
  border-top: 1px solid #2a2a2a;
  margin-top: 8px;
}

.total-price {
  font-weight: 400;
  color: #ffffff;
  font-size: 20px;
}

.pay-btn {
  background: transparent;
  color: #e8e8e8;
  border: 1px solid #3a3a3a;
  padding: 12px 0;
  border-radius: 40px;
  font-size: 15px;
  font-weight: 300;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
  letter-spacing: 0.5px;
  width: 100%;
  margin-top: 16px;
}

.pay-btn:hover:not(:disabled) {
  background: #e8e8e8;
  color: #0d0d0d;
  border-color: #e8e8e8;
}

.pay-btn:disabled {
  color: #444;
  border-color: #222;
  cursor: not-allowed;
}

.secure {
  color: #444;
  font-size: 12px;
  margin-top: 12px;
  text-transform: lowercase;
  letter-spacing: 0.3px;
}

.status {
  margin-top: 18px;
  padding: 12px;
  border-radius: 12px;
  text-align: center;
  font-size: 14px;
  font-weight: 300;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.status.success {
  color: #8bc34a;
  border: 1px solid #2a3a1a;
  background: #0d1a0a;
}

.status.error {
  color: #e57373;
  border: 1px solid #3a1a1a;
  background: #1a0a0a;
}

.status.info {
  color: #888;
  border: 1px solid #2a2a2a;
  background: #111111;
}

.back-btn {
  background: transparent;
  color: #444;
  border: none;
  padding: 14px;
  cursor: pointer;
  margin-top: 12px;
  font-size: 13px;
  width: 100%;
  text-transform: lowercase;
  letter-spacing: 0.3px;
}

.back-btn:hover {
  color: #888;
}
</style>