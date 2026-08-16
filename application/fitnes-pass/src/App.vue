<template>
  <div id="app">
    <header>
      <h1>фитнес-абонемент</h1>
      <p>выбери свой тариф и начни тренировки</p>
    </header>
    
    <main>
      <router-view />
    </main>
  
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  background: #0d0d0d;
  color: #e8e8e8;
  min-height: 100vh;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background: #111111;
  padding: 28px 20px 20px;
  text-align: center;
  border-bottom: 1px solid #2a2a2a;
}

header h1 {
  font-size: 26px;
  font-weight: 300;
  letter-spacing: 2px;
  color: #e8e8e8;
  margin-bottom: 4px;
  text-transform: lowercase;
}

header p {
  color: #666666;
  font-size: 14px;
  font-weight: 300;
  letter-spacing: 0.5px;
}

main {
  flex: 1;
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  width: 100%;
}

</style>