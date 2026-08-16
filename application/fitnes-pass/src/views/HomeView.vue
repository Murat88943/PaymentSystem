<template>
  <div class="home">
    <div class="nav">
      <div class="nav-left">
        <button class="profile-btn" @click="goToProfile">профиль</button>
      </div>
      <div class="nav-right" v-if="!isAuthenticated">
        <router-link to="/login" class="nav-link">войти</router-link>
        <router-link to="/register" class="nav-link register-link">регистрация</router-link>
      </div>
      <div class="nav-right" v-else>
        <button class="profile-btn" @click="logout">выйти</button>
      </div>
    </div>

    <section class="hero">
      <div class="hero-content">
        <span class="hero-tag">с 2015 года</span>
        <h1>фитнес-клуб<br>«iron fit»</h1>
        <p>
          современный зал с профессиональным оборудованием,<br>
          групповые программы и персональные тренировки
        </p>
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-number">5000+</span>
            <span class="stat-label">довольных клиентов</span>
          </div>
          <div class="stat">
            <span class="stat-number">12</span>
            <span class="stat-label">лет на рынке</span>
          </div>
          <div class="stat">
            <span class="stat-number">4.9</span>
            <span class="stat-label">средняя оценка</span>
          </div>
        </div>
      </div>
    </section>

    <section class="reviews">
      <h2>что говорят клиенты</h2>
      <div class="reviews-grid">
        <div class="review-card">
          <p>«отличный зал, современное оборудование, чистые раздевалки. тренеры профессионалы своего дела»</p>
          <span class="review-author">— анна, 3 года в клубе</span>
        </div>
        <div class="review-card">
          <p>«групповые тренировки на высшем уровне. хожу на йогу и пилатес, очень довольна»</p>
          <span class="review-author">— екатерина, 1,5 года</span>
        </div>
        <div class="review-card">
          <p>«персональный тренер помог сбросить 15 кг за 4 месяца. рекомендую всем!»</p>
          <span class="review-author">— михаил, 8 месяцев</span>
        </div>
      </div>
    </section>

    <section class="plans-section">
      <h2>выбери абонемент</h2>
      <div class="plans">
        <div
          v-for="plan in plans"
          :key="plan.name"
          class="plan"
          :class="{ popular: plan.is_popular }"
        >
          <div v-if="plan.is_popular" class="badge">популярный</div>
          <h3>{{ plan.name }}</h3>
          <p class="price">{{ plan.sum }} ₽</p>
          <span class="period">{{ plan.period }}</span>
          <ul>
            <li v-for="feature in plan.features" :key="feature">
              {{ feature }}
            </li>
          </ul>
          <button @click="handleBuy(plan)">оформить</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      plans: [
        {
          name: 'базовый',
          sum: 1500.0,
          currency: 'RUB',
          return_url: 'http://localhost:5173/',
          description: 'доступ в тренажерный зал, раздевалка, душ. период: в месяц.',
          period: 'месяц',
          features: ['доступ в тренажерный зал', 'раздевалка', 'душ'],
          is_popular: false
        },
        {
          name: 'оптимальный',
          sum: 3000.0,
          currency: 'RUB',
          return_url: 'http://localhost:5173/',
          description: 'доступ в тренажерный зал, групповые тренировки, раздевалка, вода, душ. период: в месяц.',
          period: 'месяц',
          features: ['доступ в тренажерный зал', 'групповые тренировки', 'раздевалка', 'вода', 'душ'],
          is_popular: true
        },
        {
          name: 'премиум',
          sum: 5000.0,
          currency: 'RUB',
          return_url: 'http://localhost:5173/',
          description: 'доступ в зал, групповые, персональный тренер, раздевалка, полотенце, душ. период: в месяц.',
          period: 'месяц',
          features: ['доступ в тренажерный зал', 'групповые тренировки', 'персональный тренер', 'раздевалка', 'полотенце', 'душ'],
          is_popular: false
        }
      ]
    }
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    }
  },
  methods: {
    handleBuy(plan) {
      this.$router.push({
        path: '/payment',
        query: {
          plan: JSON.stringify({
            name: plan.name,
            price: plan.sum,
            period: plan.period,
            features: plan.features
          })
        }
      })
    },
    goToProfile() {
      this.$router.push('/profile')
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
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

.home {
  max-width: 1000px;
  margin: 0 auto;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0 8px;
}

.nav-left {
  display: flex;
  gap: 12px;
}

.nav-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.nav-link {
  color: #666;
  text-decoration: none;
  font-size: 13px;
  transition: 0.3s;
  text-transform: lowercase;
  padding: 6px 16px;
  border-radius: 20px;
  border: 1px solid transparent;
}

.nav-link:hover {
  color: #e8e8e8;
}

.register-link {
  border-color: #2a2a2a;
}

.register-link:hover {
  border-color: #4a4a4a;
}

.profile-btn {
  background: transparent;
  color: #666;
  border: 1px solid #2a2a2a;
  padding: 6px 20px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
}

.profile-btn:hover {
  color: #e8e8e8;
  border-color: #4a4a4a;
}

.hero {
  background: #111111;
  border: 1px solid #2a2a2a;
  border-radius: 20px;
  padding: 40px 36px 36px;
  margin-bottom: 48px;
  text-align: center;
}

.hero-tag {
  display: inline-block;
  font-size: 11px;
  color: #666;
  text-transform: lowercase;
  letter-spacing: 1px;
  border: 1px solid #2a2a2a;
  padding: 3px 14px;
  border-radius: 20px;
  margin-bottom: 16px;
}

.hero h1 {
  font-size: 36px;
  font-weight: 300;
  letter-spacing: 2px;
  color: #e8e8e8;
  text-transform: lowercase;
  line-height: 1.2;
  margin-bottom: 12px;
}

.hero p {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  max-width: 500px;
  margin: 0 auto 24px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
}

.stat {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 24px;
  font-weight: 300;
  color: #e8e8e8;
}

.stat-label {
  font-size: 11px;
  color: #555;
  text-transform: lowercase;
  letter-spacing: 0.3px;
}

.reviews {
  margin-bottom: 48px;
}

.reviews h2 {
  text-align: center;
  font-size: 22px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 24px;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.review-card {
  background: #111111;
  border: 1px solid #2a2a2a;
  border-radius: 16px;
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
}

.review-card p {
  font-size: 14px;
  color: #aaa;
  line-height: 1.6;
  font-style: italic;
  flex: 1;
}

.review-author {
  font-size: 12px;
  color: #555;
  margin-top: 12px;
  text-transform: lowercase;
}

.plans-section h2 {
  text-align: center;
  font-size: 22px;
  font-weight: 300;
  letter-spacing: 1px;
  color: #e8e8e8;
  text-transform: lowercase;
  margin-bottom: 28px;
}

.plans {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
}

.plan {
  background: #131313;
  border: 1px solid #2a2a2a;
  border-radius: 20px;
  padding: 32px 24px 28px;
  width: 220px;
  text-align: center;
  transition: 0.4s ease;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1 1 200px;
}

.plan:hover {
  border-color: #4a4a4a;
  transform: translateY(-6px);
}

.plan.popular {
  border-color: #888888;
  background: #1a1a1a;
}

.badge {
  position: absolute;
  top: -10px;
  background: #888888;
  color: #0d0d0d;
  font-size: 10px;
  font-weight: 600;
  padding: 3px 16px;
  border-radius: 20px;
  text-transform: lowercase;
  letter-spacing: 0.5px;
}

.plan h3 {
  font-size: 18px;
  font-weight: 400;
  color: #e8e8e8;
  text-transform: lowercase;
  letter-spacing: 1px;
  margin-bottom: 6px;
}

.plan .price {
  font-size: 34px;
  font-weight: 300;
  color: #ffffff;
  margin: 8px 0 2px;
}

.plan .period {
  font-size: 13px;
  color: #666;
  text-transform: lowercase;
}

.plan ul {
  list-style: none;
  padding: 0;
  margin: 18px 0 24px;
  width: 100%;
  flex: 1;
}

.plan ul li {
  font-size: 13px;
  color: #aaa;
  padding: 5px 0;
  border-bottom: 1px solid #1f1f1f;
  text-transform: lowercase;
}

.plan ul li:last-child {
  border-bottom: none;
}

.plan button {
  background: transparent;
  color: #e8e8e8;
  border: 1px solid #3a3a3a;
  padding: 10px 32px;
  border-radius: 40px;
  font-size: 13px;
  font-weight: 300;
  cursor: pointer;
  transition: 0.3s;
  text-transform: lowercase;
  letter-spacing: 0.5px;
  width: 100%;
  margin-top: auto;
}

.plan button:hover {
  background: #e8e8e8;
  color: #0d0d0d;
  border-color: #e8e8e8;
}

.plan.popular button {
  border-color: #666;
}

.plan.popular button:hover {
  background: #e8e8e8;
  color: #0d0d0d;
}

@media (max-width: 768px) {
  .hero {
    padding: 30px 20px;
  }

  .hero h1 {
    font-size: 28px;
  }

  .hero-stats {
    gap: 24px;
    flex-wrap: wrap;
  }

  .reviews-grid {
    grid-template-columns: 1fr;
  }

  .plans {
    flex-direction: column;
    align-items: center;
  }

  .plan {
    width: 100%;
    max-width: 280px;
  }
}
</style>