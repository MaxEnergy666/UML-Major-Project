<template>
  <div class="login-page">
    <!-- 左侧插画区 -->
    <div class="login-left">
      <div class="illustration">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="portal"></div>
        <div class="rings">
          <div class="ring ring-1"></div>
          <div class="ring ring-2"></div>
          <div class="ring ring-3"></div>
        </div>
        <div class="astronaut"></div>
        <div class="stars">
          <span v-for="i in 20" :key="i" class="star" :style="starStyle(i)"></span>
        </div>
      </div>
      <!-- 品牌标识 -->
      <div class="brand">
        <div class="logo-icon">
          <div class="logo-sail"></div>
          <div class="logo-arrow"></div>
        </div>
        <span class="brand-text">启航</span>
      </div>
    </div>

    <!-- 右侧登录区 -->
    <div class="login-right">
      <div class="login-card">
        <!-- 二维码角标 -->
        <div class="qr-corner">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="#999">
            <rect x="2" y="2" width="7" height="7" rx="1"/>
            <rect x="15" y="2" width="7" height="7" rx="1"/>
            <rect x="2" y="15" width="7" height="7" rx="1"/>
            <rect x="15" y="15" width="3" height="3" rx="0.5"/>
            <rect x="19" y="19" width="3" height="3" rx="0.5"/>
            <rect x="15" y="19" width="3" height="3" rx="0.5"/>
            <rect x="19" y="15" width="3" height="3" rx="0.5"/>
          </svg>
        </div>

        <!-- Tab 切换 -->
        <div class="tabs">
          <div class="tab active" @click="switchTab('login')">登录</div>
          <div class="tab" @click="switchTab('register')">注册</div>
        </div>

        <!-- 登录表单 -->
        <div class="form-area">
          <div class="input-group">
            <input
              v-model="form.username"
              type="text"
              placeholder="邮箱/手机号码/小米 ID"
              class="form-input"
              @keyup.enter="handleLogin"
            />
          </div>
          <div class="input-group">
            <input
              v-model="form.password"
              type="password"
              placeholder="密码"
              class="form-input"
              @keyup.enter="handleLogin"
            />
          </div>

          <button class="login-btn" :disabled="loading" @click="handleLogin">
            {{ loading ? '登录中...' : '登录' }}
          </button>

          <!-- 辅助链接 -->
          <div class="help-links">
            <a href="javascript:void(0)" @click="showTip('忘记密码功能暂未开放')">忘记密码？</a>
            <a href="javascript:void(0)" @click="showTip('手机号登录功能暂未开放')">手机号登录</a>
          </div>

          <!-- 分隔线 -->
          <div class="divider">
            <span>其他方式登录</span>
          </div>

          <!-- 第三方登录占位 -->
          <div class="third-party">
            <div class="third-icon" title="微信登录">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="#bbb">
                <path d="M8.5 13a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm4 0a1 1 0 1 1 0-2 1 1 0 0 1 0 2zM12 2C6.48 2 2 6.03 2 11c0 2.76 1.36 5.22 3.48 6.86L4.5 21l3.65-1.82C9.4 19.72 10.67 20 12 20c5.52 0 10-4.03 10-9S17.52 2 12 2z"/>
              </svg>
            </div>
            <div class="third-icon" title="支付宝登录">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="#bbb">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-2h2v2zm0-4h-2V7h2v6zm4 4h-2v-2h2v2zm0-4h-2V7h2v6z"/>
              </svg>
            </div>
            <div class="third-icon" title="微博登录">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="#bbb">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-.79.76.29 1.97 1.01 2.14 1.14.17.13.34.09.42-.11.18-.47.63-1.87.87-2.71.14-.48.07-.72-.24-.88-.53-.27-1.3-.46-2.03-.72-1.39-.49-2.48-1.06-2.19-2.23.23-.92 1.13-1.41 2.59-1.41.44 0 .92.06 1.37.17 1.08.28 1.71.44 1.98 1.26.13.4.24 1.22.06 1.93z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cookie 提示条 -->
    <div v-if="showCookie" class="cookie-bar">
      <p>本网站使用 cookie，用于在您的设备中储存资讯。这些 cookie 可以使网站正常运行，以及帮助我们改进用户体验。</p>
      <button class="cookie-btn" @click="showCookie = false">同意并关闭提醒</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const showCookie = ref(true)

const form = reactive({
  username: '',
  password: '',
})

function starStyle(i: number) {
  const top = Math.sin(i * 1.7) * 40 + 50
  const left = Math.cos(i * 2.3) * 40 + 50
  const size = (i % 3) + 1
  const delay = (i * 0.3) % 3
  return {
    top: `${top}%`,
    left: `${left}%`,
    width: `${size}px`,
    height: `${size}px`,
    animationDelay: `${delay}s`,
  }
}

function switchTab(tab: string) {
  if (tab === 'register') {
    ElMessage.info('注册功能暂未开放')
  }
}

function showTip(msg: string) {
  ElMessage.info(msg)
}

async function handleLogin() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    await authStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.error || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* ===== 左侧插画区 ===== */
.login-left {
  width: 380px;
  min-width: 380px;
  height: 100vh;
  position: relative;
  background: linear-gradient(160deg, #0a0e27 0%, #1a1040 30%, #2d1b69 60%, #1e3a5f 100%);
  overflow: hidden;
}

.illustration {
  position: absolute;
  inset: 0;
}

/* 光球 */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
}

.orb-1 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(100, 140, 255, 0.6), transparent);
  top: 20%;
  left: 30%;
  animation: float 8s ease-in-out infinite;
}

.orb-2 {
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(180, 100, 255, 0.5), transparent);
  bottom: 25%;
  left: 20%;
  animation: float 6s ease-in-out infinite reverse;
}

.orb-3 {
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(80, 200, 255, 0.4), transparent);
  top: 55%;
  right: 15%;
  animation: float 10s ease-in-out infinite;
}

/* 空间门 */
.portal {
  position: absolute;
  width: 140px;
  height: 140px;
  border: 2px solid rgba(100, 160, 255, 0.3);
  border-radius: 50%;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow:
    0 0 30px rgba(100, 160, 255, 0.15),
    inset 0 0 30px rgba(100, 160, 255, 0.1);
  animation: pulse 4s ease-in-out infinite;
}

.portal::before {
  content: '';
  position: absolute;
  inset: 15px;
  border: 1.5px solid rgba(180, 140, 255, 0.25);
  border-radius: 50%;
  animation: spin 20s linear infinite;
}

/* 环形轨道 */
.rings {
  position: absolute;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring {
  position: absolute;
  border: 1px solid rgba(100, 160, 255, 0.12);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.ring-1 {
  width: 200px;
  height: 200px;
  animation: spin 15s linear infinite;
}

.ring-2 {
  width: 260px;
  height: 260px;
  border-color: rgba(180, 100, 255, 0.08);
  animation: spin 25s linear infinite reverse;
}

.ring-3 {
  width: 320px;
  height: 320px;
  border-color: rgba(80, 200, 255, 0.06);
  animation: spin 35s linear infinite;
}

/* 宇航员占位 */
.astronaut {
  position: absolute;
  width: 60px;
  height: 80px;
  top: 38%;
  left: 46%;
  transform: translate(-50%, -50%);
  background: radial-gradient(ellipse at center, rgba(255,255,255,0.15), transparent);
  border-radius: 30px 30px 20px 20px;
  animation: float 6s ease-in-out infinite;
}

.astronaut::before {
  content: '';
  position: absolute;
  width: 30px;
  height: 30px;
  background: radial-gradient(circle, rgba(200,220,255,0.3), rgba(100,140,255,0.1));
  border-radius: 50%;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 15px rgba(100,160,255,0.2);
}

/* 星星 */
.star {
  position: absolute;
  background: #fff;
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

/* 品牌标识 */
.brand {
  position: absolute;
  top: 24px;
  right: 24px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 10;
}

.logo-icon {
  width: 36px;
  height: 36px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 船帆 - 三角形 */
.logo-sail {
  width: 0;
  height: 0;
  border-left: 14px solid transparent;
  border-right: 14px solid transparent;
  border-bottom: 22px solid #1677FF;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 0 6px rgba(22, 119, 255, 0.5));
}

/* 底部箭头/船身 */
.logo-arrow {
  position: absolute;
  bottom: 2px;
  width: 28px;
  height: 10px;
  background: linear-gradient(90deg, #1677FF, #5b8def);
  clip-path: polygon(0 0, 100% 0, 80% 100%, 20% 100%);
}

.brand-text {
  color: #fff;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 3px;
}

/* ===== 右侧登录区 ===== */
.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  padding: 40px;
}

.login-card {
  width: 420px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  padding: 40px 36px 32px;
  position: relative;
}

/* 二维码角标 */
.qr-corner {
  position: absolute;
  top: 12px;
  right: 12px;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.qr-corner:hover {
  opacity: 0.8;
}

/* Tab */
.tabs {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
}

.tab {
  font-size: 18px;
  color: #999;
  cursor: pointer;
  padding-bottom: 10px;
  position: relative;
  transition: color 0.2s;
}

.tab.active {
  color: #333;
  font-weight: 600;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: #ff6700;
  border-radius: 2px;
}

/* 表单 */
.form-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-group {
  position: relative;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  font-size: 15px;
  border: none;
  border-radius: 6px;
  background: #f7f7f7;
  color: #333;
  outline: none;
  transition: background 0.2s;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: #bbb;
}

.form-input:focus {
  background: #f0f0f0;
}

.login-btn {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 6px;
  background: #ff6700;
  color: #fff;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 4px;
}

.login-btn:hover {
  background: #e55d00;
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* 辅助链接 */
.help-links {
  display: flex;
  justify-content: space-between;
  margin-top: 4px;
}

.help-links a {
  font-size: 13px;
  color: #999;
  text-decoration: none;
  transition: color 0.2s;
}

.help-links a:hover {
  color: #ff6700;
}

/* 分隔线 */
.divider {
  display: flex;
  align-items: center;
  margin: 8px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #eee;
}

.divider span {
  padding: 0 16px;
  font-size: 13px;
  color: #ccc;
  white-space: nowrap;
}

/* 第三方登录 */
.third-party {
  display: flex;
  justify-content: center;
  gap: 28px;
  padding-top: 4px;
}

.third-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #f7f7f7;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
}

.third-icon:hover {
  background: #eee;
}

/* Cookie 提示条 */
.cookie-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.75);
  color: #fff;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  z-index: 100;
  backdrop-filter: blur(4px);
}

.cookie-bar p {
  margin: 0;
  font-size: 13px;
  line-height: 1.5;
  flex: 1;
}

.cookie-btn {
  flex-shrink: 0;
  padding: 8px 20px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 4px;
  background: transparent;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}

.cookie-btn:hover {
  background: rgba(255,255,255,0.1);
}

/* ===== 动画 ===== */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

@keyframes pulse {
  0%, 100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 1; transform: translate(-50%, -50%) scale(1.05); }
}

@keyframes spin {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .login-left {
    display: none;
  }

  .login-right {
    padding: 20px;
  }

  .login-card {
    width: 100%;
    max-width: 400px;
  }
}
</style>
