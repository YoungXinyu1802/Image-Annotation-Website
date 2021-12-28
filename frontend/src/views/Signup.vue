<template>
  <div class="login-wrapper" :style="'background-image:url('+ Background +')'">
    <div class="form-box">
      <div class="form-title">
        <img src="../assets/img/Logo2.png" alt="icon" class="img">
        <h3 class="title">注册</h3>
<!--        <p>数据集标注网站</p>-->
      </div>
      <el-form ref="signupForm" :model="signupForm" :rules="signupRules" label-width="0px" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="signupForm.username" type="text" auto-complete="off" placeholder="用户名" prefix-icon="el-icon-user" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="signupForm.email" type="text" auto-complete="off" placeholder="邮箱" prefix-icon="el-icon-message" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="signupForm.password" type="password" auto-complete="off" placeholder="密码" prefix-icon="el-icon-lock" @keyup.enter.native="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button :loading="loading" size="small" type="primary" style="width:100%;" @click.native.prevent="handleLogin">
            <span v-if="!loading">注 册</span>
            <span v-else>注 册 中...</span>
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-link type="primary" style = "float:right" @click="login('signupForm')">已有账号，返回登录</el-link>
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
    const validateUsername = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('用户名不能小于6位'))
      } else {
        callback()
      }
    }

    const validateEmail = (rule, value, callback) => {
      let reg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (!reg.test(value)) {
        callback(new Error('请输入正确邮箱格式'))
      } else {
        callback()
      }
    }

    const validatePwd = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码不能小于6位'))
      } else {
        callback()
      }
    }

    return {
      Background,
      signupForm: {
        username: '',
        email: '',
        password: '',
        // rememberMe: true
      },



      signupRules: {
        username: [
          { required: true, trigger: 'blur', message: '用户名不能为空' },
          { required: true, trigger: 'blur', validator: validateUsername }
        ],
        email: [
          { required: true, trigger: 'blur', message: '邮箱不能为空' },
          { required: true, trigger: 'blur', validator: validateEmail }
        ],
        password: [
          { required: true, trigger: 'blur', message: '密码不能为空' },
          {required: true, trigger: 'blur', validator: validatePwd}
        ]
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
      this.$refs.signupForm.validate(valid => {
        const data = {
          username: this.signupForm.username,
          email: this.signupForm.email,
          password: this.signupForm.password
        }
        if (valid) {
          const _this = this
          console.log(valid)
          var element = Qs.stringify({ 'username': this.signupForm.username, 'email': this.signupForm.email, 'password': this.signupForm.password })
          console.log(data)
          axios.post('http://127.0.0.1:8000/api/signup', element).then(
            function (resp) {
              const flag = resp.data.request['flag']
              const msg = resp.data.request['msg']
              if (flag === 'yes') {
                alert("注册成功！返回登录界面登录")
                _this.$router.push({path: '/login'})
              } else if (msg === 'usernameInvalid') {
                alert("用户名已存在")
              } else if (msg === "emailInvalid") {
                alert("邮箱已存在")
                param.resetFields
              } else {
                alert("注册失败")
              }
            }
          )
        }
      })
    },
    login(){
      this.$router.push({ path: '/login'})
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
