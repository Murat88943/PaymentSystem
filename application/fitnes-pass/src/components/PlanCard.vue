<template>
  <div class="plan-card">
    <h3>{{ plan.name }}</h3>
    <p class="price">{{ plan.price }} ₽ <span class="period">/ {{ plan.period }}</span></p>
    <ul>
      <li v-for="feature in plan.features" :key="feature">
        {{ feature }}
      </li>
    </ul>
    <button @click="$emit('buy', plan)">оформить</button>
  </div>
</template>

<script>
export default {
  name: 'PlanCard',
  props: {
    plan: {
      type: Object,
      required: true
    }
  },
  emits: ['buy']
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.plan-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  padding: 28px 24px 24px;
  text-align: center;
  transition: 0.3s ease;
  width: 100%;
  max-width: 220px;
}

.plan-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transform: translateY(-4px);
}

.plan-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #111111;
  margin-bottom: 4px;
  text-transform: lowercase;
}

.plan-card .price {
  font-size: 26px;
  font-weight: 700;
  color: #000000;
  margin: 8px 0 2px;
}

.plan-card .period {
  font-size: 14px;
  font-weight: 400;
  color: #888888;
}

.plan-card ul {
  list-style: none;
  padding: 0;
  margin: 14px 0 18px;
  text-align: left;
}

.plan-card ul li {
  font-size: 14px;
  color: #444444;
  padding: 5px 0;
  border-bottom: 1px solid #f0f0f0;
}

.plan-card ul li:last-child {
  border-bottom: none;
}

.plan-card button {
  background: #111111;
  color: #ffffff;
  border: none;
  padding: 10px 28px;
  border-radius: 30px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s ease;
  text-transform: lowercase;
  letter-spacing: 0.3px;
}

.plan-card button:hover {
  background: #333333;
  transform: scale(1.02);
}

.plan-card button:active {
  transform: scale(0.97);
}
</style>