<template>
  <div class="login-wrapper" :style="'background-image:url('+ Background +')'">
    <div class="form-box">
      <div class="form-title">
        <img src="../assets/img/Logo2.png" alt="icon" class="img">
        <h3 class="title">数据集标注网站</h3>
<!--        <p>数据集标注网站</p>-->
      </div>
      <el-form ref="loginForm" :model="loginForm" :rules="loginRules" label-width="0px" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" type="text" auto-complete="off" placeholder="用户名/邮箱" prefix-icon="el-icon-user" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" auto-complete="off" placeholder="密码" prefix-icon="el-icon-lock" @keyup.enter.native="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button :loading="loading" size="small" type="primary" style="width:100%;" @click.native.prevent="handleLogin">
            <span v-if="!loading">登 录</span>
            <span v-else>登 录 中...</span>
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="primary" style = "float:right" @click="signup('loginForm')">前往注册</el-link>
<!--          <el-checkbox v-model="loginForm.rememberMe">记住我</el-checkbox>-->
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
import { login } from '../api/login'
import { setToken } from '../utils/cookie'
import Background from '../assets/img/login-background.jpg'

export default {
  name: 'Login',
  data() {
    return {
      Background,
      loginForm: {
        username: '',
        password: '',
        rememberMe: true
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', message: '用户名或邮箱不能为空' }],
        password: [{ required: true, trigger: 'blur', message: '密码不能为空' }]
      },
      loading: false,
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        const data = {
          username: this.loginForm.username,
          password: this.loginForm.password
        }
        if (valid) {
          const _this = this
          console.log(valid)
          var element = Qs.stringify({ 'username': this.loginForm.username, 'password': this.loginForm.password })
          console.log(data)
          axios.post('http://127.0.0.1:8000/api/login', element).then(
            function(resp) {
              const flag = resp.data.request['flag']
              const msg = resp.data.request['msg']
              console.log(msg)
              if (flag === 'success') {
                alert('登录成功')
                // _this.loading = true
                _this.loading = true
                login(data).then(res => {
                  _this.loading = false
                  setToken(res.token)
                  localStorage.setItem('username', msg['user_name'])
                  localStorage.setItem('password', msg['password'])
                  localStorage.setItem('email', msg['email'])
                  console.log(localStorage.getItem('username'))
                  _this.$router.push({ path: _this.redirect || '/' })
                }).catch(() => {
                  _this.loading = false
                })
              } else {
                if (flag === 'pwdError') {
                  alert('密码错误')
                } else if (flag === 'no') {
                  alert('用户不存在')
                }
              }
            }
          )
        }
      })
    },
    signup(){
      this.$router.push({ path: '/signup'})
    }
  }
}
</script>

<style lang="less">
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100vh;
  background-size: cover;
  .form-box {
    width: 320px;
    padding: 15px 30px 20px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 15px 30px 0 rgba(0, 0, 1, .1);
    .form-title {
      margin: 0 auto 35px;
      text-align: center;
      color: #707070;
      font-size: 18px;
      letter-spacing: 2px;
    }
  }
  .title{
    margin-top: 5px
  }
  .img{
    width: 100px
  }
}
</style>
